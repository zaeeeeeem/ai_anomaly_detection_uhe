import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { AdminLayout } from '../components/admin/AdminLayout';
import { InteractionDetail } from '../components/admin/InteractionDetail';
import { adminService } from '../services/adminService';

export const AdminInteractionDetail = () => {
  const { interactionId } = useParams();
  const [detail, setDetail] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadDetail = async () => {
      setLoading(true);
      try {
        const data = await adminService.getInteractionDetail(interactionId);
        setDetail(data);
      } finally {
        setLoading(false);
      }
    };

    loadDetail();
  }, [interactionId]);

  return (
    <AdminLayout
      title="Interaction Detail"
      subtitle="Full 5-level analysis for this interaction"
      actions={
        <Link to={`/admin/review/${interactionId}`} className="admin-button">
          Review
        </Link>
      }
    >
      {loading ? (
        <div className="admin-card">Loading detail…</div>
      ) : (
        <InteractionDetail detail={detail} />
      )}
    </AdminLayout>
  );
};
