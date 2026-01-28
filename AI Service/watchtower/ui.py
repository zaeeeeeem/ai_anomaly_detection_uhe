from __future__ import annotations

from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .config import BASE_DIR
from .log_agent import LogAgent
from .orchestrator import WatchtowerOrchestrator
from .schemas import FeedbackRecord
from .storage import SQLiteStore


class WatchtowerUI:
    def __init__(
        self,
        store: Optional[SQLiteStore] = None,
        log_agent: Optional[LogAgent] = None,
        orchestrator: Optional[WatchtowerOrchestrator] = None,
    ) -> None:
        self.store = store or SQLiteStore()
        self.log_agent = log_agent or LogAgent(store=self.store)
        self.orchestrator = orchestrator or WatchtowerOrchestrator(store=self.store)
        self.plots_dir = BASE_DIR / "data" / "plots"
        self.plots_dir.mkdir(parents=True, exist_ok=True)

    def run(self) -> None:
        while True:
            self._print_menu()
            choice = input("Select an option: ").strip()
            if choice == "1":
                self._ingest_log()
            elif choice == "2":
                self._run_analysis()
            elif choice == "3":
                self._view_anomalies()
            elif choice == "4":
                self._analytics_dashboard()
            elif choice == "5":
                self._feedback_labeling()
            elif choice in {"q", "quit", "exit", "0"}:
                print("Exiting Watchtower UI.")
                break
            else:
                print("Invalid option. Try again.")

    def _print_menu(self) -> None:
        print("\n" + "=" * 60)
        print("AI Misbehavior Watchtower")
        print("=" * 60)
        print("1) Ingest log")
        print("2) Run analysis")
        print("3) View anomalies")
        print("4) Analytics dashboard")
        print("5) Feedback labeling")
        print("0) Exit")

    def _ingest_log(self) -> None:
        print("\nIngest Interaction Log")
        prompt = input("Prompt: ").strip()
        response = input("Response: ").strip()
        model_name = input("Model name [unknown]: ").strip() or "unknown"
        user_id = input("User id [anonymous]: ").strip() or "anonymous"
        conversation_id = input("Conversation id [default]: ").strip() or "default"
        tags_raw = input("Tags (comma-separated) [medical]: ").strip() or "medical"
        tags = [tag.strip() for tag in tags_raw.split(",") if tag.strip()]

        interaction_id = self.log_agent.log_interaction(
            prompt=prompt,
            response=response,
            metadata={"source": "local_ui", "tags": tags},
            model_name=model_name,
            user_id=user_id,
            conversation_id=conversation_id,
        )
        print(f"Logged interaction: {interaction_id}")

    def _run_analysis(self) -> None:
        print("\nRun Analysis")
        threshold = self._read_float("Anomaly threshold [0.75]: ", default=0.75)
        mode = input("Mode [shadow|intercept] (default shadow): ").strip().lower() or "shadow"
        batch_size = self._read_int("Batch size [100]: ", default=100)
        filters: Dict[str, Any] = {}
        user_id = input("Filter by user id (optional): ").strip()
        if user_id:
            filters["user_id"] = user_id

        processed = 0
        flagged = 0
        intercepted = 0
        for result in self.orchestrator.run(
            filters=filters or None,
            batch_size=batch_size,
            anomaly_threshold=threshold,
            mode=mode,
        ):
            processed += 1
            scores = result.get("scores")
            effective_score = None
            if scores:
                effective_score = scores.scores.get(
                    "final_score", scores.scores.get("overall_anomaly_score", 0.0)
                )
            if effective_score is not None and effective_score >= threshold:
                flagged += 1
            if result.get("intercepted"):
                intercepted += 1
                if mode == "intercept":
                    print(f"Intercepted interaction: {result['log'].id}")
        summary = f"Processed: {processed} | Flagged: {flagged}"
        if mode == "intercept":
            summary += f" | Intercepted: {intercepted}"
        print(summary)

    def _view_anomalies(self) -> None:
        threshold = self._read_float("Anomaly threshold [0.75]: ", default=0.75)
        logs = self.store.load_logs(limit=200)
        rows = []
        for log in logs:
            scoring = self.store.get_scoring_record(log.id)
            if not scoring:
                continue
            overall = scoring.scores.get("final_score", scoring.scores.get("overall_anomaly_score", 0.0))
            if overall < threshold:
                continue
            flags = [k for k, v in scoring.flags.items() if v]
            rows.append(
                (
                    log.timestamp,
                    log.prompt[:50].replace("\n", " "),
                    log.response[:50].replace("\n", " "),
                    round(overall, 3),
                    ",".join(flags[:3]),
                    log.id,
                )
            )
        if not rows:
            print("No anomalies found.")
            return
        print("\nTimestamp | Prompt | Response | Score | Flags | Interaction ID")
        print("-" * 90)
        for row in rows:
            print(" | ".join(str(item) for item in row))

        selected = input("\nEnter interaction id for details (or blank to return): ").strip()
        if selected:
            self._show_interaction_detail(selected)

    def _show_interaction_detail(self, interaction_id: str) -> None:
        log = self.store.get_interaction(interaction_id)
        if not log:
            print("Interaction not found.")
            return
        analysis = self.store.get_analysis_record(interaction_id)
        scoring = self.store.get_scoring_record(interaction_id)
        explanations = self.store.list_explanations(interaction_id)

        print("\nInteraction Detail")
        print(f"Timestamp: {log.timestamp}")
        print(f"Prompt: {log.prompt}")
        print(f"Response: {log.response}")
        if scoring:
            print(f"Scores: {scoring.scores}")
            print(f"Flags: {scoring.flags}")
        if analysis:
            print(f"Topics: {analysis.topics}")
            print(f"Risk context: {analysis.risk_context_flags}")
        if explanations:
            for explanation in explanations:
                print(f"Explanation ({explanation.risk_type}): {explanation.explanation}")
                print(f"Citations: {explanation.citations}")

    def _analytics_dashboard(self) -> None:
        scoring_records = self.store.list_scoring_records()
        if not scoring_records:
            print("No scoring records available.")
            return

        overall_scores = [
            record.scores.get("overall_anomaly_score", 0.0) for record in scoring_records
        ]
        flag_counts = Counter()
        dates = Counter()
        for record in scoring_records:
            for key, value in record.flags.items():
                if value:
                    flag_counts[key] += 1
            interaction = self.store.get_interaction(record.interaction_id)
            if interaction:
                date_key = self._safe_date(interaction.timestamp)
                if date_key:
                    dates[date_key] += 1

        self._plot_histogram(overall_scores)
        self._plot_flag_counts(flag_counts)
        self._plot_time_series(dates)

    def _feedback_labeling(self) -> None:
        interaction_id = input("Interaction id: ").strip()
        if not interaction_id:
            print("Interaction id is required.")
            return
        label = input("Label [SAFE|UNSAFE|BORDERLINE]: ").strip().upper()
        if label not in {"SAFE", "UNSAFE", "BORDERLINE"}:
            print("Invalid label.")
            return
        corrected = input("Corrected response (optional): ").strip() or None
        comments = input("Comments (optional): ").strip() or None

        record = FeedbackRecord(
            interaction_id=interaction_id,
            human_label=label,
            corrected_response=corrected,
            comments=comments,
            timestamp=datetime.utcnow().isoformat(),
            reviewer_id=None,
        )
        self.store.insert_feedback(record)
        print("Feedback saved.")

    def _plot_histogram(self, scores: List[float]) -> None:
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("matplotlib not available. Skipping plots.")
            return

        path = self.plots_dir / "anomaly_histogram.png"
        plt.figure(figsize=(6, 4))
        plt.hist(scores, bins=10, color="#4C72B0")
        plt.title("Overall Anomaly Score Distribution")
        plt.xlabel("Score")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.savefig(path)
        plt.close()
        print(f"Saved histogram: {path}")

    def _plot_flag_counts(self, counts: Counter) -> None:
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            return

        if not counts:
            print("No flags recorded.")
            return

        path = self.plots_dir / "flag_counts.png"
        labels, values = zip(*counts.most_common())
        plt.figure(figsize=(7, 4))
        plt.bar(labels, values, color="#55A868")
        plt.title("Flag Counts")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(path)
        plt.close()
        print(f"Saved flag counts: {path}")

    def _plot_time_series(self, dates: Counter) -> None:
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            return
        if not dates:
            print("No dated records.")
            return

        path = self.plots_dir / "anomalies_over_time.png"
        sorted_dates = sorted(dates.items())
        labels = [item[0] for item in sorted_dates]
        values = [item[1] for item in sorted_dates]
        plt.figure(figsize=(7, 4))
        plt.plot(labels, values, marker="o", color="#C44E52")
        plt.title("Anomalies Over Time")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(path)
        plt.close()
        print(f"Saved time series: {path}")

    @staticmethod
    def _safe_date(timestamp: str) -> Optional[str]:
        try:
            return datetime.fromisoformat(timestamp).date().isoformat()
        except ValueError:
            return None

    @staticmethod
    def _read_int(prompt: str, default: int) -> int:
        raw = input(prompt).strip()
        if not raw:
            return default
        try:
            return int(raw)
        except ValueError:
            return default

    @staticmethod
    def _read_float(prompt: str, default: float) -> float:
        raw = input(prompt).strip()
        if not raw:
            return default
        try:
            return float(raw)
        except ValueError:
            return default
