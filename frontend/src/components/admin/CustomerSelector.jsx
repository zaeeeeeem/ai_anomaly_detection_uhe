import React from 'react';
import './CustomerSelector.css';

export const CustomerSelector = ({ users, selectedUser, onSelect }) => {
  return (
    <div className="customer-selector">
      <label htmlFor="customer-select">Select customer</label>
      <select
        id="customer-select"
        value={selectedUser?.id || ''}
        onChange={(event) => {
          const id = event.target.value;
          const user = users.find((item) => String(item.id) === id);
          onSelect(user || null);
        }}
      >
        <option value="">Choose a customer</option>
        {users.map((user) => (
          <option key={user.id} value={user.id}>
            {user.full_name || user.username} ({user.email})
          </option>
        ))}
      </select>
    </div>
  );
};
