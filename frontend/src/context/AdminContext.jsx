import React, { createContext, useCallback, useMemo, useState } from 'react';
import { adminService } from '../services/adminService';

export const AdminContext = createContext(null);

export const AdminProvider = ({ children }) => {
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [loading, setLoading] = useState(false);

  const loadUsers = useCallback(async () => {
    setLoading(true);
    try {
      const data = await adminService.getUsers();
      setUsers(data);
    } finally {
      setLoading(false);
    }
  }, []);

  const value = useMemo(
    () => ({
      users,
      selectedUser,
      setSelectedUser,
      loading,
      loadUsers,
    }),
    [users, selectedUser, loading, loadUsers]
  );

  return <AdminContext.Provider value={value}>{children}</AdminContext.Provider>;
};
