import React, { useState, useId } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Shield, Lock, User, AlertCircle, Eye, EyeOff } from 'lucide-react';
import { Button } from '../components/ui/Button';
import './Login.css';

export const Login = () => {
  const { login, user } = useAuth();
  const navigate = useNavigate();
  const errorId = useId();

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  React.useEffect(() => {
    if (user) navigate('/dashboard', { replace: true });
  }, [user, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!username || !password) {
      setError('Please fill in all fields.');
      return;
    }
    setError('');
    setLoading(true);
    const res = await login(username, password);
    if (res.success) {
      navigate('/dashboard', { replace: true });
    } else {
      setError(res.error || 'Invalid credentials');
      setLoading(false);
    }
  };

  return (
    <div className="login-page-wrapper">
      <div className="login-card-container">
        <div className="login-card-header">
          <div className="shield-icon-container" aria-hidden="true">
            <Shield size={32} className="shield-login-icon" />
          </div>
          <h1 className="login-title">Login</h1>
          <p className="login-subtitle">
            Enter your credentials to access the NyayaSetu grievance platform.
          </p>
        </div>

        {/* Accessible error alert */}
        {error && (
          <div
            id={errorId}
            role="alert"
            aria-live="assertive"
            className="login-error-alert"
          >
            <AlertCircle size={18} aria-hidden="true" />
            <span>{error}</span>
          </div>
        )}

        <form
          onSubmit={handleSubmit}
          className="login-form-element"
          noValidate
          aria-describedby={error ? errorId : undefined}
        >
          {/* Username */}
          <div className="form-group-login">
            <label className="form-label-login" htmlFor="login-username">
              Username
            </label>
            <div className="form-input-wrapper">
              <User className="input-field-icon" size={18} aria-hidden="true" />
              <input
                id="login-username"
                type="text"
                className="form-input-login"
                placeholder="Username"
                value={username}
                onChange={e => setUsername(e.target.value)}
                disabled={loading}
                autoComplete="username"
                aria-required="true"
                aria-invalid={!!error}
                aria-describedby={error ? errorId : undefined}
              />
            </div>
          </div>

          {/* Password with show/hide toggle */}
          <div className="form-group-login">
            <label className="form-label-login" htmlFor="login-password">
              Password
            </label>
            <div className="form-input-wrapper" style={{ position: 'relative' }}>
              <Lock className="input-field-icon" size={18} aria-hidden="true" />
              <input
                id="login-password"
                type={showPassword ? 'text' : 'password'}
                className="form-input-login"
                placeholder="Password"
                value={password}
                onChange={e => setPassword(e.target.value)}
                disabled={loading}
                autoComplete="current-password"
                aria-required="true"
                aria-invalid={!!error}
                style={{ paddingRight: '2.5rem' }}
              />
              <button
                type="button"
                onClick={() => setShowPassword(prev => !prev)}
                aria-label={showPassword ? 'Hide password' : 'Show password'}
                style={{
                  position: 'absolute', right: 10, top: '50%',
                  transform: 'translateY(-50%)', background: 'none',
                  border: 'none', cursor: 'pointer', color: 'var(--text-muted)', padding: 4,
                }}
              >
                {showPassword ? <EyeOff size={16} aria-hidden="true" /> : <Eye size={16} aria-hidden="true" />}
              </button>
            </div>
          </div>

          <Button
            type="submit"
            variant="primary"
            size="md"
            loading={loading}
            disabled={loading}
            style={{ width: '100%', justifyContent: 'center', marginTop: '0.5rem' }}
          >
            {loading ? 'Authenticating…' : 'Sign In'}
          </Button>
        </form>

        <div className="login-card-footer">
          <p className="registration-prompt-text">
            New citizen user?{' '}
            <Link to="/register" className="register-now-link">
              Register New Account
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
