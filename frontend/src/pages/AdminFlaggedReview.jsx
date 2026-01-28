import React, { useEffect, useState } from 'react';
import { AdminLayout } from '../components/admin/AdminLayout';
import { FlaggedItemsList } from '../components/admin/FlaggedItemsList';
import { adminService } from '../services/adminService';

export const AdminFlaggedReview = () => {
  const [interactions, setInteractions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      try {
        const data = await adminService.getFlaggedInteractions();
        setInteractions(data);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  return (
    <AdminLayout
      title="Flagged for Review"
      subtitle="High-risk interactions awaiting human review"
    >
      <FlaggedItemsList interactions={interactions} loading={loading} />
    </AdminLayout>
  );
};
