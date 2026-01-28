import React from 'react';
import { AuthLayout } from '../components/auth/AuthLayout';
import { SignupForm } from '../components/auth/SignupForm';

export const Signup = () => {
  return (
    <AuthLayout
      title="Create Account"
      subtitle="Join MediGuard AI for advanced anomaly detection"
    >
      <SignupForm />
    </AuthLayout>
  );
};
