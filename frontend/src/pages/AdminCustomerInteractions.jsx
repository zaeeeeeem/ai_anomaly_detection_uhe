import React, { useEffect, useState } from 'react';
import { AdminLayout } from '../components/admin/AdminLayout';
import { InteractionsList } from '../components/admin/InteractionsList';
import { CustomerSelector } from '../components/admin/CustomerSelector';
import { adminService } from '../services/adminService';
import { useAdmin } from '../hooks/useAdmin';

export const AdminCustomerInteractions = () => {
  const { users, selectedUser, setSelectedUser, loading, loadUsers } = useAdmin();
  const [interactions, setInteractions] = useState([]);
  const [loadingInteractions, setLoadingInteractions] = useState(false);

  useEffect(() => {
    loadUsers();
  }, [loadUsers]);

  useEffect(() => {
    const loadInteractions = async () => {
      if (!selectedUser) {
        setInteractions([]);
        return;
      }
      setLoadingInteractions(true);
      try {
        const data = await adminService.getUserInteractions(selectedUser.id);
        setInteractions(data);
      } finally {
        setLoadingInteractions(false);
      }
    };

    loadInteractions();
  }, [selectedUser]);

  return (
    <AdminLayout
      title="Customer Interactions"
      subtitle="Inspect interaction history for a specific customer"
    >
      <CustomerSelector
        users={users}
        selectedUser={selectedUser}
        onSelect={setSelectedUser}
      />
      <InteractionsList
        interactions={interactions}
        loading={loading || loadingInteractions}
        emptyMessage={
          selectedUser
            ? 'No interactions for this customer yet.'
            : 'Select a customer to view their interactions.'
        }
      />
    </AdminLayout>
  );
};
