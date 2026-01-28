import React, { useEffect, useState } from 'react';
import { AdminLayout } from '../components/admin/AdminLayout';
import { InteractionsList } from '../components/admin/InteractionsList';
import { adminService } from '../services/adminService';

export const AdminAllInteractions = () => {
  const [interactions, setInteractions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      try {
        const data = await adminService.getAllInteractions();
        setInteractions(data);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  return (
    <AdminLayout
      title="All Interactions"
      subtitle="Complete audit trail across all customers"
    >
      <InteractionsList
        interactions={interactions}
        loading={loading}
        emptyMessage="No interactions logged yet."
      />
    </AdminLayout>
  );
};
