import React, { useState, useEffect } from 'react';
import './ReviewInterface.css';

const LABELS = ['SAFE', 'UNSAFE', 'BORDERLINE'];

export const ReviewInterface = ({ onSubmit, submitting, initialData }) => {
  const [humanLabel, setHumanLabel] = useState(
    initialData?.human_label || 'SAFE'
  );
  const [correctedResponse, setCorrectedResponse] = useState(
    initialData?.corrected_response || ''
  );
  const [comments, setComments] = useState(initialData?.comments || '');
  const [isSubmitted, setIsSubmitted] = useState(!!initialData);
  const [isEditing, setIsEditing] = useState(false);

  // Update submitted state when initialData changes
  useEffect(() => {
    if (initialData) {
      setIsSubmitted(true);
      setHumanLabel(initialData.human_label || 'SAFE');
      setCorrectedResponse(initialData.corrected_response || '');
      setComments(initialData.comments || '');
    }
  }, [initialData]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    await onSubmit({
      human_label: humanLabel,
      corrected_response: correctedResponse || null,
      comments: comments || null,
    });
    setIsSubmitted(true);
    setIsEditing(false);
  };

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleCancel = () => {
    setIsEditing(false);
    // Reset to original values
    if (initialData) {
      setHumanLabel(initialData.human_label || 'SAFE');
      setCorrectedResponse(initialData.corrected_response || '');
      setComments(initialData.comments || '');
    }
  };

  const isLocked = isSubmitted && !isEditing;

  return (
    <div className="review-interface">
      {isSubmitted && !isEditing && (
        <div className="review-submitted-banner">
          <div className="review-submitted-content">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
              <polyline points="22 4 12 14.01 9 11.01" />
            </svg>
            <div>
              <h4>Review Submitted</h4>
              <p>This interaction has been reviewed. You can edit your review if needed.</p>
            </div>
          </div>
          <button type="button" className="review-edit-button" onClick={handleEdit}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
            </svg>
            Edit Review
          </button>
        </div>
      )}

      <form className={`review-form ${isLocked ? 'review-locked' : ''}`} onSubmit={handleSubmit}>
        <div className="review-group">
          <label>Human label</label>
          <div className="label-toggle">
            {LABELS.map((label) => (
              <button
                type="button"
                key={label}
                className={`label-option ${humanLabel === label ? 'active' : ''}`}
                onClick={() => !isLocked && setHumanLabel(label)}
                disabled={isLocked}
              >
                {label}
              </button>
            ))}
          </div>
        </div>

        <div className="review-group">
          <label htmlFor="corrected-response">Corrected response (optional)</label>
          <textarea
            id="corrected-response"
            value={correctedResponse}
            onChange={(event) => setCorrectedResponse(event.target.value)}
            rows={4}
            disabled={isLocked}
            placeholder={isLocked ? '' : 'Enter a corrected response if the original was unsafe or incorrect...'}
          />
        </div>

        <div className="review-group">
          <label htmlFor="comments">Reviewer comments (optional)</label>
          <textarea
            id="comments"
            value={comments}
            onChange={(event) => setComments(event.target.value)}
            rows={3}
            disabled={isLocked}
            placeholder={isLocked ? '' : 'Add any additional notes or context about your review...'}
          />
        </div>

        {!isLocked && (
          <div className="review-actions">
            {isEditing && (
              <button type="button" className="review-cancel" onClick={handleCancel}>
                Cancel
              </button>
            )}
            <button className="review-submit" type="submit" disabled={submitting}>
              {submitting ? (
                <>
                  <svg className="review-submit-spinner" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M21 12a9 9 0 1 1-6.219-8.56" />
                  </svg>
                  Submitting…
                </>
              ) : isEditing ? (
                'Update Review'
              ) : (
                'Submit Review'
              )}
            </button>
          </div>
        )}
      </form>
    </div>
  );
};
