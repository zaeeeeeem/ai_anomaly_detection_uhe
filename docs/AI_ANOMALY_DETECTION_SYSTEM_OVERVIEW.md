# AI Anomaly Detection System — End‑to‑End Data Flow (Backend)

This document describes the **exact** backend behavior based on the current code under `backend/`. It walks through the system from the user prompt to Gemini response, then into the 5‑level anomaly pipeline, and finally to admin review. No assumptions are made beyond what the code implements.

---

## 0) Scope and Source of Truth

All details below are taken from these backend Python files:

- `backend/app/routers/chat.py`
- `backend/app/services/gemini_service.py`
- `backend/app/services/ollama_service.py`
- `backend/app/services/interaction_service.py`
- `backend/app/services/pipeline_orchestrator.py`
- `backend/app/services/analysis_agent.py`
- `backend/app/services/scoring_agent.py`
- `backend/app/services/explanation_agent.py`
- `backend/app/services/rag_service.py`
- `backend/app/utils/prompts.py`
- `backend/app/models/*.py`
- `backend/app/routers/admin.py`
- `backend/app/routers/interactions.py`
- `backend/app/routers/review.py`
- `backend/app/utils/admin_dependencies.py`
- `backend/app/utils/dependencies.py`
- `backend/app/config.py`
- `backend/app/database.py`
- `backend/scripts/ingest_documents.py`

---

## 1) User Prompt → LLM Response (Chat Request Path)

**Entry point:** `POST /api/chat/{conversation_id}/message` in `backend/app/routers/chat.py`.

### Step‑by‑step (exact behavior):

1. **Conversation ownership check**
   - The route verifies the conversation exists and belongs to the current user.

2. **Persist user message**
   - Creates a `Message` row (`role=MessageRole.USER`).

3. **Build conversation history**
   - Loads all messages in the conversation (ascending time) and converts them to a list of `{role, content}` (excluding the just‑saved user message).

4. **Generate AI response**
   - **If model_type is Gemini**: `gemini_service.generate_response()` is called.
   - **If model_type is Ollama**: `ollama_service.generate_response()` is called.

5. **Persist assistant message**
   - Saves a `Message` row (`role=MessageRole.ASSISTANT`) with the LLM response.

6. **Create the Level‑1 log record (InteractionLog)**
   - `interaction_service.log_interaction()` writes an `InteractionLog` row with:
     - `prompt`, `response`, `model_name`, `user_id`, `conversation_id`
     - `metadata_json` containing: `model_type`, `user_message_id`, `assistant_message_id`

7. **Schedule anomaly pipeline (async)**
   - If `settings.ENABLE_AUTO_ANALYSIS` is `True`, the pipeline is scheduled **as a background task** using:
     - `asyncio.create_task(anyio.to_thread.run_sync(pipeline_orchestrator.run_sync, interaction_id))`
   - This ensures **chat response is returned immediately**; pipeline runs in a background thread.

---

## 2) Level 1 — Interaction Logging (Always On)

**Model:** `InteractionLog` in `backend/app/models/interaction_log.py`

Fields stored:
- `id` (UUID)
- `prompt` (user text)
- `response` (assistant text)
- `model_name`
- `timestamp`
- `user_id`
- `conversation_id`
- `metadata_json` (model_type and message IDs)

Relationships:
- `analysis`, `scoring`, `explanation`, `feedback` (one‑to‑one)

This is created by `interaction_service.log_interaction()` immediately after the assistant response is saved.

---

## 3) Level 2 — Record Analysis (Topics + Risk Flags)

**Agent:** `AnalysisAgent` in `backend/app/services/analysis_agent.py`

### What it does:
- Builds a prompt from `LEVEL_2_ANALYSIS_PROMPT` (`backend/app/utils/prompts.py`).
- Sends the prompt to `gemini_service.generate_json()`.
- Expects strict JSON:
  - `topics` (list)
  - `risk_context_flags` (object)
  - `hallucination_hints` (object)

### Storage:
- Writes a `RecordAnalysis` row where `id == interaction.id` (`backend/app/models/record_analysis.py`).

### Notes:
- This is always run first inside the pipeline.

---

## 4) Level 3 — Scoring (Quantitative Risk + Flag Decision)

**Agent:** `ScoringAgent` in `backend/app/services/scoring_agent.py`

### What it does:
- Builds a prompt from `LEVEL_3_SCORING_PROMPT`.
- Sends to `gemini_service.generate_json()`.
- Expects JSON with:
  - `scores` (e.g., safety_risk, factuality_risk, overall_anomaly_score)
  - `flags` (same structure as Level 2 flags)

### Flag decision:
- `overall_anomaly_score >= settings.ANOMALY_THRESHOLD` marks `is_flagged=True`.

### Storage:
- Writes a `ScoringRecord` row where `id == interaction.id`.

---

## 5) Level 4 — RAG‑Based Explanation (Flagged Only)

**Agent:** `ExplanationAgent` in `backend/app/services/explanation_agent.py`

### Trigger:
- Runs only if `ScoringRecord.is_flagged == True`.

### What it does:
1. **Retrieve docs** using `rag_service.query()` on combined prompt + response.
2. **Format retrieved context** into a prompt block.
3. **Call Gemini JSON** using `LEVEL_4_EXPLANATION_PROMPT`.
4. **Normalize risk_type** to lowercase (`triage|dosing|disclaimer|self_harm|other`).
5. If no citations returned, it falls back to RAG hits.

### Storage:
- Writes `ExplanationRecord` with:
  - `risk_type` (enum: triage/dosing/disclaimer/self_harm/other)
  - `explanation` (text)
  - `citations` (JSON list)

---

## 6) Level 5 — Human Review (Admin‑Only)

**API:** `POST /api/review/{interaction_id}` in `backend/app/routers/review.py`

### What it does:
- Admin can set:
  - `human_label` (SAFE/UNSAFE/BORDERLINE)
  - `corrected_response` (optional)
  - `comments` (optional)
  - `reviewer_id` (defaults to admin ID)

### Storage:
- Writes or updates a `FeedbackRecord` where `id == interaction_id`.

---

## 7) RAG Knowledge Base (How It’s Built)

**Service:** `backend/app/services/rag_service.py`
- Uses `chromadb.PersistentClient` with `collection = medical_guidelines`.
- Embeddings come from `SentenceTransformer(settings.EMBEDDING_MODEL)`.

**Ingestion Script:** `backend/scripts/ingest_documents.py`
- Reads files in `backend/documents/medical_guidelines/`.
- Splits into overlapping chunks (default: 500 chars, overlap 50).
- Writes chunks into Chroma with `doc_id`, `chunk_id`, and metadata.

**Query:**
- Returns `top_k` results with `doc_id`, `chunk_id`, `score`, `text`.

---

## 8) Gemini + JSON Behavior (Technical Details)

**Gemini JSON calls** are made via `gemini_service.generate_json()`:
- Forces a JSON‑only prompt prefix: “Return ONLY valid JSON. Do not include markdown fences.”
- Attempts to parse raw JSON; if invalid, extracts the first JSON block via regex.
- If a requested JSON model is unsupported, it retries with `gemini-2.5-flash-lite`.

**Gemini standard responses** use `gemini_service.generate_response()` and a medical system prompt (text‑only).

---

## 9) Admin Views and Access Control

**Admin‑only access** enforced in `backend/app/utils/admin_dependencies.py`.

Available endpoints:
- `GET /api/admin/users`
- `GET /api/admin/interactions`
- `GET /api/admin/interactions/flagged`
- `GET /api/admin/interactions/user/{user_id}`
- `GET /api/admin/metrics`

**Detail view:**
- `GET /api/interactions/{interaction_id}` returns all 5 levels in one response.

---

## 10) Database Cascade Behavior

The system enforces cascading deletes for cleanup:
- Deleting a conversation deletes its `interaction_logs`.
- Deleting an interaction deletes its analysis, scoring, explanation, and feedback records.

This is implemented via `ondelete="CASCADE"` foreign keys and Alembic migrations.

---

## 11) Full Data Flow Summary (One‑Line Sequence)

User prompt → Chat router saves user message → Gemini/Ollama response → assistant message saved → InteractionLog created → pipeline scheduled in background thread → Level 2 analysis → Level 3 scoring → Level 4 explanation (if flagged) → Level 5 human review (admin action).

---

## 12) Configuration Switches (Actual Code)

From `backend/app/config.py`:
- `ENABLE_AUTO_ANALYSIS` (default True)
- `ANOMALY_THRESHOLD` (default 0.7)
- `GEMINI_JSON_MODEL` (default gemini‑2.5‑flash‑lite)
- `CHROMA_PERSIST_DIR`, `EMBEDDING_MODEL`

---

This is the exact backend behavior as of the current codebase.
