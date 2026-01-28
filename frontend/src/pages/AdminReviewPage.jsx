import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { AdminLayout } from '../components/admin/AdminLayout';
import { InteractionDetail } from '../components/admin/InteractionDetail';
import { ReviewInterface } from '../components/admin/ReviewInterface';
import { adminService } from '../services/adminService';
import { reviewService } from '../services/reviewService';

export const AdminReviewPage = () => {
  const { interactionId } = useParams();
  const [detail, setDetail] = useState(null);
  const [feedback, setFeedback] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      try {
        const detailData = await adminService.getInteractionDetail(interactionId);
        setDetail(detailData);
        try {
          const feedbackData = await reviewService.getFeedback(interactionId);
          setFeedback(feedbackData);
        } catch (error) {
          setFeedback(null);
        }
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, [interactionId]);

  const handleSubmit = async (payload) => {
    setSubmitting(true);
    try {
      const data = await reviewService.submitFeedback(interactionId, {
        ...payload,
        interaction_id: interactionId,
      });
      setFeedback(data);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <AdminLayout
      title="Review Interaction"
      subtitle="Provide a human label and corrections if needed"
    >
      {loading ? (
        <div className="admin-card">Loading review…</div>
      ) : (
        <>
          <InteractionDetail detail={detail} />
          <ReviewInterface
            initialData={feedback}
            onSubmit={handleSubmit}
            submitting={submitting}
          />
        </>
      )}
    </AdminLayout>
  );
};
