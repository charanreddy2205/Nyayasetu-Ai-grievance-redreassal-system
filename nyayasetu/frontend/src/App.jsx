import React, { lazy, Suspense } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';
import { Navbar } from './components/Navbar';
import { Footer } from './components/Footer';
import { Spinner } from './components/ui/Spinner';
import { Scale } from 'lucide-react';
import './styles/variables.css';
import './styles/globals.css';

// ── Lazy-loaded routes ────────────────────────────────────────
// Each heavy page is split into its own JS chunk so the initial
// bundle only contains auth + shell code.
const PublicDashboard   = lazy(() => import('./pages/PublicDashboard'));
const Login             = lazy(() => import('./pages/Login'));
const Register          = lazy(() => import('./pages/Register'));
const CitizenDashboard  = lazy(() => import('./pages/CitizenDashboard'));
const CitizenComplaints = lazy(() => import('./pages/CitizenComplaints'));
const OfficerDashboard  = lazy(() => import('./pages/OfficerDashboard'));
const OfficerComplaints = lazy(() => import('./pages/OfficerComplaints'));
const LodgeComplaint    = lazy(() => import('./pages/LodgeComplaint'));
const ComplaintDetail   = lazy(() => import('./pages/ComplaintDetail'));

// ── Route-level loading fallback ──────────────────────────────
const RouteFallback = () => (
  <div className="full-page-loading" aria-live="polite" aria-busy="true">
    <Spinner size={40} label="Loading page..." />
    <h1 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--primary-navy)', marginTop: 'var(--space-4)', marginBottom: 'var(--space-2)' }}>
      Loading NyayaSetu
    </h1>
    <span style={{ color: 'var(--text-muted)', fontSize: 'var(--font-size-sm)', marginTop: 'var(--space-3)' }}>
      Loading…
    </span>
  </div>
);

// ── Session-loading screen ────────────────────────────────────
const SessionLoader = () => (
  <div className="full-page-loading">
    <Scale size={44} aria-hidden="true" style={{ color: 'var(--primary-blue)', animation: 'spin 1s linear infinite' }} />
    <h1 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--primary-navy)', marginTop: 'var(--space-4)', marginBottom: 'var(--space-2)' }}>
      Initializing Portal Desk
    </h1>
    <span style={{ fontFamily: 'var(--font-sans)', fontWeight: 600, color: 'var(--primary-navy)', marginTop: 'var(--space-4)' }}>
      Initializing Portal Desk…
    </span>
  </div>
);

// ── Protected route wrapper ───────────────────────────────────
const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();
  if (loading) return <SessionLoader />;
  if (!user)   return <Navigate to="/login" replace />;
  return children;
};

// ── Role-based dashboard router ───────────────────────────────
const DashboardRouter = ({ view = 'dashboard' }) => {
  const { user } = useAuth();
  
  if (view === 'dashboard') {
    return user?.role === 'citizen' ? <CitizenDashboard /> : <OfficerDashboard />;
  } else if (view === 'complaints') {
    return user?.role === 'citizen' ? <CitizenComplaints /> : <OfficerComplaints />;
  }
  return null;
};

// ── Main app shell ────────────────────────────────────────────
const AppContent = () => {
  const { loading } = useAuth();
  if (loading) return <SessionLoader />;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      {/* Skip-to-main for keyboard / screen-reader users */}
      <a href="#main-content" className="skip-to-main">Skip to main content</a>

      <Navbar />

      <main id="main-content" style={{ flex: 1 }}>
        <Suspense fallback={<RouteFallback />}>
          <Routes>
            <Route path="/"                  element={<PublicDashboard />} />
            <Route path="/login"             element={<Login />} />
            <Route path="/register"          element={<Register />} />

            <Route path="/dashboard"         element={<ProtectedRoute><DashboardRouter view="dashboard" /></ProtectedRoute>} />
            <Route path="/complaints"        element={<ProtectedRoute><DashboardRouter view="complaints" /></ProtectedRoute>} />
            <Route path="/complaints/lodge"  element={<ProtectedRoute><LodgeComplaint /></ProtectedRoute>} />
            <Route path="/complaints/:id"    element={<ProtectedRoute><ComplaintDetail /></ProtectedRoute>} />

            {/* Catch-all */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Suspense>
      </main>

      <Footer />
    </div>
  );
};

// ── Root component ────────────────────────────────────────────
export const App = () => (
  <BrowserRouter>
    <ThemeProvider>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </ThemeProvider>
  </BrowserRouter>
);

export default App;
