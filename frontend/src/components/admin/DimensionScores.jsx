import React from 'react';
import './DimensionScores.css';

export const DimensionScores = ({ scores }) => {
  if (!scores) return null;

  const dimensions = [
    { key: 'quality', label: 'Quality', inverse: true },
    { key: 'hallucination', label: 'Hallucination', inverse: false },
    { key: 'alignment', label: 'Alignment', inverse: true },
    { key: 'safety', label: 'Safety', inverse: false },
    { key: 'confidence', label: 'Confidence', inverse: true }
  ];

  const getScoreColor = (score, inverse) => {
    const effectiveScore = inverse ? (1 - score) : score;
    if (effectiveScore >= 0.7) return 'high';
    if (effectiveScore >= 0.4) return 'medium';
    return 'low';
  };

  const getScorePercentage = (score) => {
    return Math.round(score * 100);
  };

  return (
    <div className="dimension-scores">
      <h4>Detection Layer Scores</h4>
      <div className="scores-grid">
        {dimensions.map(({ key, label, inverse }) => {
          const score = scores[key];
          if (score === undefined) return null;

          const percentage = getScorePercentage(score);
          const colorClass = getScoreColor(score, inverse);

          return (
            <div key={key} className="score-item">
              <div className="score-header">
                <span className="score-label">{label}</span>
                <span className={`score-value ${colorClass}`}>
                  {percentage}%
                </span>
              </div>
              <div className="score-bar">
                <div
                  className={`score-fill ${colorClass}`}
                  style={{ width: `${percentage}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
