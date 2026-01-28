import React, { useState, useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';
import { InteractionDetailSkeleton } from '../../components/common/LoadingStates';
import { EmptyCitations, NoReviewYet } from '../../components/common/EmptyStates';
import { ApiError, NotFoundError } from '../../components/common/ErrorStates';
import { DimensionScores } from '../../components/admin/DimensionScores';
import { adminService } from '../../services/adminService';
import './InteractionDetail.css';

const InteractionDetail = () => {
  const { id } = useParams();
  const [interaction, setInteraction] = useState(null);
  const [detailedAnalysis, setDetailedAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchInteraction = async () => {
      try {
        setLoading(true);

        // Fetch the actual interaction data
        const data = await adminService.getInteractionDetail(id);

        // Fetch detailed analysis from enhanced endpoint
        try {
          const analysis = await adminService.getDetailedAnalysis(id);
          setDetailedAnalysis(analysis);
        } catch (err) {
          console.log('No enhanced analysis available:', err);
        }

        // Map API response to component format
        const mappedInteraction = {
          id: data.interaction.id,
          timestamp: new Date(data.interaction.timestamp).toLocaleString(),
          model: data.interaction.model_name,
          user_id: `user_${data.interaction.user_id}`,
          user_input: data.interaction.prompt,
          ai_response: data.interaction.response,
          topics: data.analysis?.topics || [],
          flags: data.analysis?.flags || {},
          scores: data.scoring ? {
            toxicity: data.scoring.toxicity_score || 0,
            medical_accuracy: data.scoring.medical_accuracy_score || 0,
            safety_risk: data.scoring.overall_risk_score || 0
          } : {},
          overall_score: data.scoring?.overall_risk_score || 0,
          status: data.scoring?.is_flagged ? 'flagged' : 'safe',
          explanation: data.explanation?.explanation_text || '',
          citations: data.explanation?.citations || [],
          review: data.feedback ? {
            status: data.feedback.review_status,
            reviewer: data.feedback.reviewer_name || 'Unknown',
            timestamp: new Date(data.feedback.reviewed_at).toLocaleString(),
            corrected_response: data.feedback.corrected_response,
            comments: data.feedback.comments
          } : null
        };

        setInteraction(mappedInteraction);
        setError(null);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    fetchInteraction();
  }, [id]);

  // Helper to get score level
  const getScoreLevel = (score) => {
    if (score < 0.3) return 'low';
    if (score < 0.7) return 'medium';
    return 'high';
  };

  // Loading state
  if (loading) {
    return <InteractionDetailSkeleton />;
  }

  // Error state
  if (error) {
    if (error?.status === 404) {
      return <NotFoundError resourceName="Interaction" onGoBack={() => window.history.back()} />;
    }
    return <ApiError error={error} onRetry={() => window.location.reload()} />;
  }

  // No data state
  if (!interaction) {
    return <NotFoundError resourceName="Interaction" onGoBack={() => window.history.back()} />;
  }

  return (
    <div className="interaction-detail">
      {/* Header */}
      <div className="interaction-detail-header">
        <h1>Interaction Detail</h1>
        <span className="interaction-id">{interaction.id}</span>
      </div>

      {/* Level 1: Interaction Log */}
      <div className="level-section">
        <div className="level-header">
          <div className="level-number">1</div>
          <div className="level-title">
            <h3>Interaction Log</h3>
            <p>Original user query and AI response</p>
          </div>
        </div>
        <div className="level-content">
          <div className="interaction-log-grid">
            <div className="interaction-meta-item">
              <span className="interaction-meta-label">Timestamp</span>
              <span className="interaction-meta-value mono">{interaction.timestamp}</span>
            </div>
            <div className="interaction-meta-item">
              <span className="interaction-meta-label">Model</span>
              <span className="interaction-meta-value mono">{interaction.model}</span>
            </div>
            <div className="interaction-meta-item">
              <span className="interaction-meta-label">User ID</span>
              <span className="interaction-meta-value mono">{interaction.user_id}</span>
            </div>
          </div>

          <div className="interaction-content-box">
            <div className="interaction-content-label">
              <span className="interaction-content-label-icon">👤</span>
              User Input
            </div>
            <div className="interaction-content-text">{interaction.user_input}</div>
          </div>

          <div className="interaction-content-box">
            <div className="interaction-content-label">
              <span className="interaction-content-label-icon">🤖</span>
              AI Response
            </div>
            <div className="interaction-content-text">{interaction.ai_response}</div>
          </div>
        </div>
      </div>

      {/* Level 2: Enhanced Detection (if available) */}
      {detailedAnalysis && detailedAnalysis.anomaly_score && (
        <div className="level-section">
          <div className="level-header">
            <div className="level-number">2</div>
            <div className="level-title">
              <h3>Multi-Dimensional Detection</h3>
              <p>Enhanced anomaly detection across 5 dimensions</p>
            </div>
          </div>
          <div className="level-content">
            {/* Anomaly Classification */}
            <div className="detection-summary">
              <div className="detection-summary-row">
                <span className="detection-summary-label">Classification:</span>
                <span className={`detection-category ${detailedAnalysis.anomaly_score.anomaly_category.toLowerCase()}`}>
                  {detailedAnalysis.anomaly_score.anomaly_category.replace(/_/g, ' ')}
                </span>
              </div>
              <div className="detection-summary-row">
                <span className="detection-summary-label">Final Score:</span>
                <span className="detection-summary-value">
                  {(detailedAnalysis.anomaly_score.final_anomaly_score * 100).toFixed(1)}%
                </span>
              </div>
              <div className="detection-summary-row">
                <span className="detection-summary-label">Status:</span>
                <span className={`detection-status ${detailedAnalysis.anomaly_score.is_anomaly ? 'flagged' : 'safe'}`}>
                  {detailedAnalysis.anomaly_score.is_anomaly ? '🚩 Flagged' : '✓ Safe'}
                </span>
              </div>
            </div>

            {/* Dimension Scores */}
            <DimensionScores scores={{
              quality: detailedAnalysis.anomaly_score.quality_anomaly_score,
              hallucination: detailedAnalysis.anomaly_score.hallucination_anomaly_score,
              alignment: detailedAnalysis.anomaly_score.alignment_anomaly_score,
              safety: detailedAnalysis.anomaly_score.safety_anomaly_score,
              confidence: detailedAnalysis.anomaly_score.confidence_anomaly_score
            }} />

            {/* Detection Layer Details */}
            <div className="detection-layers">
              {detailedAnalysis.quality_analysis && (
                <details className="detection-layer-details">
                  <summary className="detection-layer-summary">
                    <strong>Response Quality Analysis</strong>
                    <span className="detection-layer-score">
                      Score: {(detailedAnalysis.quality_analysis.overall_quality_score * 100).toFixed(1)}%
                    </span>
                  </summary>
                  <div className="detection-layer-content">
                    {detailedAnalysis.quality_analysis.quality_issues.length > 0 && (
                      <div className="detection-subsection">
                        <h5>Issues Detected:</h5>
                        <ul>
                          {detailedAnalysis.quality_analysis.quality_issues.map((issue, idx) => (
                            <li key={idx}>{issue}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                    {detailedAnalysis.quality_analysis.strengths.length > 0 && (
                      <div className="detection-subsection">
                        <h5>Strengths:</h5>
                        <ul>
                          {detailedAnalysis.quality_analysis.strengths.map((strength, idx) => (
                            <li key={idx}>{strength}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </details>
              )}

              {detailedAnalysis.hallucination_detection && (
                <details className="detection-layer-details">
                  <summary className="detection-layer-summary">
                    <strong>Hallucination Detection</strong>
                    <span className="detection-layer-score">
                      Risk: {(detailedAnalysis.hallucination_detection.hallucination_risk_score * 100).toFixed(1)}%
                    </span>
                  </summary>
                  <div className="detection-layer-content">
                    <div className="detection-subsection">
                      <h5>Claims Analysis:</h5>
                      <p>Extracted: {detailedAnalysis.hallucination_detection.extracted_claims.length}</p>
                      <p>Verified: {detailedAnalysis.hallucination_detection.verified_claims.length}</p>
                      <p>Unverified: {detailedAnalysis.hallucination_detection.unverified_claims.length}</p>
                    </div>
                    {detailedAnalysis.hallucination_detection.hallucination_markers.length > 0 && (
                      <div className="detection-subsection">
                        <h5>Hallucination Markers:</h5>
                        <ul>
                          {detailedAnalysis.hallucination_detection.hallucination_markers.map((marker, idx) => (
                            <li key={idx}>{marker}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                    <div className="detection-subsection">
                      <h5>Recommended Action:</h5>
                      <p>{detailedAnalysis.hallucination_detection.recommended_action}</p>
                    </div>
                  </div>
                </details>
              )}

              {detailedAnalysis.context_alignment && (
                <details className="detection-layer-details">
                  <summary className="detection-layer-summary">
                    <strong>Context Alignment</strong>
                    <span className="detection-layer-score">
                      Score: {(detailedAnalysis.context_alignment.overall_alignment_score * 100).toFixed(1)}%
                    </span>
                  </summary>
                  <div className="detection-layer-content">
                    <div className="detection-subsection">
                      <h5>Response Category:</h5>
                      <p>{detailedAnalysis.context_alignment.response_category}</p>
                    </div>
                    {detailedAnalysis.context_alignment.alignment_issues.length > 0 && (
                      <div className="detection-subsection">
                        <h5>Alignment Issues:</h5>
                        <ul>
                          {detailedAnalysis.context_alignment.alignment_issues.map((issue, idx) => (
                            <li key={idx}>{issue}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                    {detailedAnalysis.context_alignment.explanation && (
                      <div className="detection-subsection">
                        <h5>Explanation:</h5>
                        <p>{detailedAnalysis.context_alignment.explanation}</p>
                      </div>
                    )}
                  </div>
                </details>
              )}

              {detailedAnalysis.safety_assessment && (
                <details className="detection-layer-details">
                  <summary className="detection-layer-summary">
                    <strong>Safety Assessment</strong>
                    <span className="detection-layer-score">
                      Risk: {(detailedAnalysis.safety_assessment.safety_risk_score * 100).toFixed(1)}%
                    </span>
                  </summary>
                  <div className="detection-layer-content">
                    <div className="detection-subsection">
                      <h5>Risk Category:</h5>
                      <p>{detailedAnalysis.safety_assessment.risk_category}</p>
                    </div>
                    {detailedAnalysis.safety_assessment.safety_issues.length > 0 && (
                      <div className="detection-subsection">
                        <h5>Safety Issues:</h5>
                        <ul>
                          {detailedAnalysis.safety_assessment.safety_issues.map((issue, idx) => (
                            <li key={idx}>
                              <strong>{issue.type}:</strong> {issue.description}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </details>
              )}

              {detailedAnalysis.confidence_calibration && (
                <details className="detection-layer-details">
                  <summary className="detection-layer-summary">
                    <strong>Confidence Calibration</strong>
                    <span className="detection-layer-score">
                      Quality: {(detailedAnalysis.confidence_calibration.calibration_quality * 100).toFixed(1)}%
                    </span>
                  </summary>
                  <div className="detection-layer-content">
                    <div className="detection-subsection">
                      <h5>Confidence Analysis:</h5>
                      <p>Expressed Confidence: {(detailedAnalysis.confidence_calibration.confidence_score * 100).toFixed(1)}%</p>
                      <p>Appropriate Level: {(detailedAnalysis.confidence_calibration.appropriate_confidence * 100).toFixed(1)}%</p>
                    </div>
                    {detailedAnalysis.confidence_calibration.issues.length > 0 && (
                      <div className="detection-subsection">
                        <h5>Calibration Issues:</h5>
                        <ul>
                          {detailedAnalysis.confidence_calibration.issues.map((issue, idx) => (
                            <li key={idx}>{issue}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </details>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Level 2/3: Record Analysis (Legacy) */}
      <div className="level-section">
        <div className="level-header">
          <div className="level-number">{detailedAnalysis ? '3' : '2'}</div>
          <div className="level-title">
            <h3>Record Analysis</h3>
            <p>Detected topics and safety flags</p>
          </div>
        </div>
        <div className="level-content">
          <div className="topics-grid">
            {interaction.topics.map((topic, idx) => (
              <span key={idx} className="topic-tag">
                🏷️ {topic.replace(/_/g, ' ')}
              </span>
            ))}
          </div>

          <div className="flags-section">
            <div className="flags-section-title">Safety Flags</div>
            <div className="flags-grid">
              {Object.entries(interaction.flags).map(([key, value]) => (
                <div key={key} className={`flag-item ${value ? 'flagged' : ''}`}>
                  <div className={`flag-icon ${value ? 'flag-icon-true' : 'flag-icon-false'}`}>
                    {value ? '✓' : '✗'}
                  </div>
                  <span className="flag-label">{key.replace(/_/g, ' ')}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Level 3/4: Scoring */}
      <div className="level-section">
        <div className="level-header">
          <div className="level-number">{detailedAnalysis ? '4' : '3'}</div>
          <div className="level-title">
            <h3>Scoring</h3>
            <p>Automated risk assessment scores</p>
          </div>
        </div>
        <div className="level-content">
          <div className="scores-grid">
            {Object.entries(interaction.scores).map(([key, value]) => {
              const level = getScoreLevel(value);
              return (
                <div key={key} className="score-card">
                  <div className={`score-card-value ${level}`}>
                    {(value * 100).toFixed(0)}%
                  </div>
                  <div className="score-card-bar">
                    <div 
                      className={`score-card-bar-fill ${level}`}
                      style={{ width: `${value * 100}%` }}
                    />
                  </div>
                  <div className="score-card-label">
                    {key.replace(/_/g, ' ')}
                  </div>
                </div>
              );
            })}
          </div>

          <div className={`overall-score ${interaction.status}`}>
            <div className="overall-score-label">Overall Risk Score</div>
            <div className="overall-score-value">
              {(interaction.overall_score * 100).toFixed(0)}%
            </div>
            <div className={`overall-score-status ${interaction.status}`}>
              {interaction.status === 'flagged' && '🚩 Flagged for Review'}
              {interaction.status === 'safe' && '✓ Safe'}
              {interaction.status === 'borderline' && '⚠️ Borderline'}
            </div>
          </div>
        </div>
      </div>

      {/* Level 4/5: Explanation */}
      <div className="level-section">
        <div className="level-header">
          <div className="level-number">{detailedAnalysis ? '5' : '4'}</div>
          <div className="level-title">
            <h3>Explanation</h3>
            <p>AI-generated analysis and relevant citations</p>
          </div>
        </div>
        <div className="level-content">
          <div className="explanation-content">
            <div className="explanation-text">{interaction.explanation}</div>
          </div>

          <div className="citations-section-title">Relevant Citations</div>
          <div className="citations-list">
            {interaction.citations && interaction.citations.length > 0 ? (
              interaction.citations.map((citation, idx) => (
                <div key={idx} className="citation-item">
                  <div className="citation-icon">📄</div>
                  <div className="citation-content">
                    <div className="citation-title">{citation.title}</div>
                    <div className="citation-meta">{citation.source}</div>
                  </div>
                  <div className="citation-score">
                    {(citation.relevance * 100).toFixed(0)}%
                  </div>
                </div>
              ))
            ) : (
              <EmptyCitations />
            )}
          </div>
        </div>
      </div>

      {/* Level 5/6: Human Review */}
      <div className="level-section">
        <div className="level-header">
          <div className="level-number">{detailedAnalysis ? '6' : '5'}</div>
          <div className="level-title">
            <h3>Human Review</h3>
            <p>Expert verification and corrections</p>
          </div>
        </div>
        <div className="level-content">
          {interaction.review ? (
            <>
              <div className="review-status">
                <div className={`review-label-badge ${interaction.review.status}`}>
                  {interaction.review.status === 'safe' && '✓ Approved - Safe'}
                  {interaction.review.status === 'unsafe' && '✗ Rejected - Unsafe'}
                  {interaction.review.status === 'borderline' && '⚠️ Needs Revision'}
                </div>
                <div className="review-meta">
                  <div className="review-reviewer">
                    Reviewed by {interaction.review.reviewer}
                  </div>
                  <div className="review-timestamp">{interaction.review.timestamp}</div>
                </div>
              </div>

              {interaction.review.corrected_response && (
                <div className="review-content-section">
                  <h4>Corrected Response</h4>
                  <div className="review-corrected-response">
                    {interaction.review.corrected_response}
                  </div>
                </div>
              )}

              {interaction.review.comments && (
                <div className="review-content-section">
                  <h4>Reviewer Comments</h4>
                  <div className="review-comments">
                    {interaction.review.comments}
                  </div>
                </div>
              )}
            </>
          ) : (
            <NoReviewYet />
          )}
        </div>
      </div>

      {/* Back Button */}
      <div style={{ marginTop: 'var(--space-8)', textAlign: 'center' }}>
        <Link 
          to="/admin/interactions"
          className="btn btn-outline"
        >
          ← Back to Interactions
        </Link>
      </div>
    </div>
  );
};

export default InteractionDetail;
