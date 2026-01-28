import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import './InteractionDetail.css';

const formatTimestamp = (timestamp) => {
  if (!timestamp) return '—';
  const date = new Date(timestamp);
  if (Number.isNaN(date.getTime())) return timestamp;
  return date.toLocaleString();
};

const renderList = (items) => {
  if (!items?.length) return <span className="pill muted">None</span>;
  return items.map((item) => (
    <span key={item} className="pill">
      {item}
    </span>
  ));
};

const renderFlags = (flags = {}) => {
  const entries = Object.entries(flags);
  if (!entries.length) return <span className="muted">No flags available.</span>;
  return (
    <div className="flag-grid">
      {entries.map(([key, value]) => (
        <div key={key} className="flag-row">
          <span className="flag-key">{key.replace(/_/g, ' ')}</span>
          <span className={`flag-value ${value ? 'on' : 'off'}`}>
            {String(value)}
          </span>
        </div>
      ))}
    </div>
  );
};

const PipelineStage = ({ level, title, icon, status, isOpen, onToggle, children, hasData }) => {
  return (
    <div className={`pipeline-stage ${isOpen ? 'open' : 'closed'} ${!hasData ? 'no-data' : ''}`}>
      <div className="stage-connector" />

      <button className="stage-header" onClick={onToggle} type="button">
        <div className="stage-header-left">
          <div className="stage-icon">
            {icon}
            <div className="stage-level">L{level}</div>
          </div>
          <div className="stage-title-group">
            <h3 className="stage-title">{title}</h3>
            {status && <span className="stage-status">{status}</span>}
          </div>
        </div>
        <div className="stage-header-right">
          {hasData && (
            <div className={`stage-indicator ${isOpen ? 'processing' : 'complete'}`}>
              {isOpen ? (
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <polyline points="18 15 12 9 6 15" />
                </svg>
              ) : (
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <polyline points="6 9 12 15 18 9" />
                </svg>
              )}
            </div>
          )}
          {!hasData && (
            <span className="stage-badge no-data-badge">No Data</span>
          )}
        </div>
      </button>

      {isOpen && hasData && (
        <div className="stage-content">
          {children}
        </div>
      )}
    </div>
  );
};

export const InteractionDetail = ({ detail }) => {
  const [openStages, setOpenStages] = useState({ 1: true });

  const toggleStage = (level) => {
    setOpenStages(prev => ({ ...prev, [level]: !prev[level] }));
  };

  if (!detail) {
    return (
      <div className="detail-loading">
        <div className="loading-spinner-detail"></div>
        <p>Loading interaction detail…</p>
      </div>
    );
  }

  const { interaction, analysis, scoring, explanation, feedback } = detail;

  return (
    <div className="interaction-detail-modern">
      {/* Pipeline Header */}
      <div className="pipeline-header">
        <div className="pipeline-header-content">
          <div className="pipeline-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 2L2 7l10 5 10-5-10-5z" />
              <path d="M2 17l10 5 10-5" />
              <path d="M2 12l10 5 10-5" />
            </svg>
          </div>
          <div>
            <h2>ML Processing Pipeline</h2>
            <p>Multi-stage analysis and anomaly detection system</p>
          </div>
        </div>
      </div>

      <div className="pipeline-stages">
        {/* Level 1 - Interaction Log */}
        <PipelineStage
          level={1}
          title="Interaction Log"
          status="Data Ingestion"
          icon={
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
              <polyline points="14 2 14 8 20 8" />
              <line x1="16" y1="13" x2="8" y2="13" />
              <line x1="16" y1="17" x2="8" y2="17" />
              <polyline points="10 9 9 9 8 9" />
            </svg>
          }
          isOpen={openStages[1]}
          onToggle={() => toggleStage(1)}
          hasData={true}
        >
          <div className="stage-meta-grid">
            <div className="meta-item">
              <span className="meta-label">Interaction ID</span>
              <span className="meta-value">{interaction.id}</span>
            </div>
            <div className="meta-item">
              <span className="meta-label">Timestamp</span>
              <span className="meta-value">{formatTimestamp(interaction.timestamp)}</span>
            </div>
            <div className="meta-item">
              <span className="meta-label">Model</span>
              <span className="meta-value">{interaction.model_name}</span>
            </div>
          </div>

          <div className="message-exchange">
            <div className="message-box user-message-box">
              <div className="message-box-header">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                  <circle cx="12" cy="7" r="4" />
                </svg>
                <span>User Prompt</span>
              </div>
              <div className="message-box-content">{interaction.prompt}</div>
            </div>

            <div className="message-box assistant-message-box">
              <div className="message-box-header">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M12 2L2 7l10 5 10-5-10-5z" />
                  <path d="M2 17l10 5 10-5" />
                  <path d="M2 12l10 5 10-5" />
                </svg>
                <span>Assistant Response</span>
              </div>
              <div className="message-box-content markdown-body">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {interaction.response}
                </ReactMarkdown>
              </div>
            </div>
          </div>
        </PipelineStage>

        {/* Level 2 - Record Analysis */}
        <PipelineStage
          level={2}
          title="Record Analysis"
          status="Feature Extraction"
          icon={
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="3" />
              <path d="M12 1v6m0 6v6M5.64 5.64l4.24 4.24m4.24 4.24l4.24 4.24M1 12h6m6 0h6M5.64 18.36l4.24-4.24m4.24-4.24l4.24-4.24" />
            </svg>
          }
          isOpen={openStages[2]}
          onToggle={() => toggleStage(2)}
          hasData={!!analysis}
        >
          {analysis && (
            <>
              <div className="analysis-section">
                <div className="analysis-header">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z" />
                    <line x1="7" y1="7" x2="7.01" y2="7" />
                  </svg>
                  <span>Extracted Topics</span>
                </div>
                <div className="pill-row">{renderList(analysis.topics)}</div>
              </div>

              <div className="analysis-section">
                <div className="analysis-header">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
                    <line x1="12" y1="9" x2="12" y2="13" />
                    <line x1="12" y1="17" x2="12.01" y2="17" />
                  </svg>
                  <span>Risk Context Flags</span>
                </div>
                {renderFlags(analysis.risk_context_flags)}
              </div>

              <div className="analysis-section">
                <div className="analysis-header">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <circle cx="12" cy="12" r="10" />
                    <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3" />
                    <line x1="12" y1="17" x2="12.01" y2="17" />
                  </svg>
                  <span>Hallucination Hints</span>
                </div>
                {renderFlags(analysis.hallucination_hints)}
              </div>
            </>
          )}
        </PipelineStage>

        {/* Level 3 - Scoring */}
        <PipelineStage
          level={3}
          title="Risk Scoring"
          status="ML Model Inference"
          icon={
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="18" y1="20" x2="18" y2="10" />
              <line x1="12" y1="20" x2="12" y2="4" />
              <line x1="6" y1="20" x2="6" y2="14" />
            </svg>
          }
          isOpen={openStages[3]}
          onToggle={() => toggleStage(3)}
          hasData={!!scoring}
        >
          {scoring && (
            <>
              <div className="score-grid-modern">
                {Object.entries(scoring.scores || {}).map(([key, value]) => {
                  const percentage = Math.min(1, value) * 100;
                  const isHigh = value > 0.7;
                  return (
                    <div key={key} className={`score-card-modern ${isHigh ? 'high-risk' : ''}`}>
                      <div className="score-card-header">
                        <span className="score-label-modern">{key.replace(/_/g, ' ')}</span>
                        <span className="score-value-modern">{Number(value).toFixed(3)}</span>
                      </div>
                      <div className="score-bar-modern">
                        <div
                          className="score-bar-fill"
                          style={{ width: `${percentage}%` }}
                        />
                      </div>
                      <div className="score-percentage">{percentage.toFixed(1)}%</div>
                    </div>
                  );
                })}
              </div>

              <div className="analysis-section">
                <div className="analysis-header">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
                  </svg>
                  <span>Detection Flags</span>
                </div>
                {renderFlags(scoring.flags)}
              </div>

              <div className={`flag-status-modern ${scoring.is_flagged ? 'flagged' : 'safe'}`}>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  {scoring.is_flagged ? (
                    <>
                      <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
                      <line x1="12" y1="9" x2="12" y2="13" />
                      <line x1="12" y1="17" x2="12.01" y2="17" />
                    </>
                  ) : (
                    <>
                      <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
                      <polyline points="22 4 12 14.01 9 11.01" />
                    </>
                  )}
                </svg>
                <span>{scoring.is_flagged ? 'Flagged for Human Review' : 'Passed — No Anomaly Detected'}</span>
              </div>
            </>
          )}
        </PipelineStage>

        {/* Level 4 - Explanation */}
        <PipelineStage
          level={4}
          title="Explainability Layer"
          status="RAG Generation"
          icon={
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
            </svg>
          }
          isOpen={openStages[4]}
          onToggle={() => toggleStage(4)}
          hasData={!!explanation}
        >
          {explanation && (
            <>
              <div className="explanation-risk-type">
                <span className="risk-type-label">Identified Risk Type</span>
                <span className="risk-type-pill">{explanation.risk_type}</span>
              </div>

              <div className="explanation-text-box">
                <div className="explanation-text-header">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <circle cx="12" cy="12" r="10" />
                    <line x1="12" y1="16" x2="12" y2="12" />
                    <line x1="12" y1="8" x2="12.01" y2="8" />
                  </svg>
                  <span>Explanation</span>
                </div>
                <p className="explanation-text">{explanation.explanation}</p>
              </div>

              <div className="citation-section">
                <div className="citation-header">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
                    <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
                  </svg>
                  <span>Retrieved Context Citations</span>
                </div>
                <div className="citation-list-modern">
                  {explanation.citations.map((citation, index) => (
                    <div key={`${citation.doc_id}-${index}`} className="citation-card">
                      <div className="citation-meta">
                        <span className="citation-doc">Doc: {citation.doc_id}</span>
                        <span className="citation-chunk">Chunk: {citation.chunk_id}</span>
                      </div>
                      <div className="citation-score">
                        <span>Relevance</span>
                        <span className="citation-score-value">{(citation.score * 100).toFixed(1)}%</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}
        </PipelineStage>

        {/* Level 5 - Human Review */}
        <PipelineStage
          level={5}
          title="Human Review"
          status="Quality Assurance"
          icon={
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
              <circle cx="9" cy="7" r="4" />
              <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
              <path d="M16 3.13a4 4 0 0 1 0 7.75" />
            </svg>
          }
          isOpen={openStages[5]}
          onToggle={() => toggleStage(5)}
          hasData={!!feedback}
        >
          {feedback && (
            <>
              <div className="review-label-box">
                <span className="review-label-text">Human Label</span>
                <span className="review-label-value">{feedback.human_label}</span>
              </div>

              {feedback.corrected_response && (
                <div className="review-section">
                  <div className="review-section-header">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <polyline points="20 6 9 17 4 12" />
                    </svg>
                    <span>Corrected Response</span>
                  </div>
                  <div className="review-text-box">{feedback.corrected_response}</div>
                </div>
              )}

              {feedback.comments && (
                <div className="review-section">
                  <div className="review-section-header">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
                    </svg>
                    <span>Reviewer Comments</span>
                  </div>
                  <div className="review-text-box">{feedback.comments}</div>
                </div>
              )}
            </>
          )}
        </PipelineStage>
      </div>
    </div>
  );
};
