import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ChatProvider } from './context/ChatContext';
import { AdminProvider } from './context/AdminContext';
import { useAuth } from './hooks/useAuth';
import { Login } from './pages/Login';
import { Signup } from './pages/Signup';
import { Chat } from './pages/Chat';
import { NotFound } from './pages/NotFound';
import { LoadingSpinner } from './components/common/LoadingSpinner';
import { AdminHome } from './pages/AdminHome';
import { AdminAllInteractions } from './pages/AdminAllInteractions';
import { AdminCustomerInteractions } from './pages/AdminCustomerInteractions';
import { AdminFlaggedReview } from './pages/AdminFlaggedReview';
import { AdminInteractionDetail } from './pages/AdminInteractionDetail';
import { AdminReviewPage } from './pages/AdminReviewPage';
import InteractionDetail from './pages/admin/InteractionDetail';

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <LoadingSpinner size="large" text="Loading..." />;
  }

  return isAuthenticated ? children : <Navigate to="/login" replace />;
};

const PublicRoute = ({ children }) => {
  const { isAuthenticated, loading, user } = useAuth();

  if (loading) {
    return <LoadingSpinner size="large" text="Loading..." />;
  }

  if (!isAuthenticated) {
    return children;
  }

  return user?.role === 'admin' ? (
    <Navigate to="/admin/home" replace />
  ) : (
    <Navigate to="/chat" replace />
  );
};

const AdminRoute = ({ children }) => {
  const { user, loading, isAuthenticated } = useAuth();

  if (loading) {
    return <LoadingSpinner size="large" text="Loading..." />;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return user?.role === 'admin' ? children : <Navigate to="/chat" replace />;
};

const RootRedirect = () => {
  const { user, loading, isAuthenticated } = useAuth();

  if (loading) {
    return <LoadingSpinner size="large" text="Loading..." />;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return user?.role === 'admin' ? (
    <Navigate to="/admin/home" replace />
  ) : (
    <Navigate to="/chat" replace />
  );
};

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AdminProvider>
          <ChatProvider>
            <Routes>
              <Route
                path="/login"
                element={
                  <PublicRoute>
                    <Login />
                  </PublicRoute>
                }
              />
              <Route
                path="/signup"
                element={
                  <PublicRoute>
                    <Signup />
                  </PublicRoute>
                }
              />

              <Route
                path="/chat"
                element={
                  <ProtectedRoute>
                    <Chat />
                  </ProtectedRoute>
                }
              />

              <Route
                path="/admin/home"
                element={
                  <AdminRoute>
                    <AdminHome />
                  </AdminRoute>
                }
              />
              <Route
                path="/admin/interactions/:id"
                element={
                  <AdminRoute>
                    <InteractionDetail />
                  </AdminRoute>
                }
              />
              <Route
                path="/admin/all-interactions"
                element={
                  <AdminRoute>
                    <AdminAllInteractions />
                  </AdminRoute>
                }
              />
              <Route
                path="/admin/customer-interactions"
                element={
                  <AdminRoute>
                    <AdminCustomerInteractions />
                  </AdminRoute>
                }
              />
              <Route
                path="/admin/flagged-review"
                element={
                  <AdminRoute>
                    <AdminFlaggedReview />
                  </AdminRoute>
                }
              />
              <Route
                path="/admin/interaction/:interactionId"
                element={
                  <AdminRoute>
                    <AdminInteractionDetail />
                  </AdminRoute>
                }
              />
              <Route
                path="/admin/review/:interactionId"
                element={
                  <AdminRoute>
                    <AdminReviewPage />
                  </AdminRoute>
                }
              />

              <Route path="/" element={<RootRedirect />} />
              <Route path="*" element={<NotFound />} />
            </Routes>
          </ChatProvider>
        </AdminProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
