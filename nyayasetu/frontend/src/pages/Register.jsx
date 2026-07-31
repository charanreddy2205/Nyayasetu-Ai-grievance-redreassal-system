import React, { useState, useId } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Lock, User, Mail, UserPlus, AlertCircle, Eye, EyeOff } from 'lucide-react';
import { Button } from '../components/ui/Button';
import './Login.css';

const FieldError = ({ message, id }) =>
  message ? (
    <span id={id} role="alert" style={{ fontSize: 'var(--font-size-xs)', color: '#ef4444', marginTop: '0.25rem', display: 'block' }}>
      {message}
    </span>
  ) : null;

export const Register = () => {
  const { register, user } = useAuth();
  const navigate = useNavigate();
  const formErrorId = useId();

  const [fields, setFields] = useState({
    username: '', firstName: '', lastName: '',
    email: '', password: '', confirmPassword: '',
  });
  const [fieldErrors, setFieldErrors] = useState({});
  const [formError, setFormError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  React.useEffect(() => {
    if (user) navigate('/dashboard', { replace: true });
  }, [user, navigate]);

  const set = (key) => (e) => setFields(prev => ({ ...prev, [key]: e.target.value }));

  const validate = () => {
    const errors = {};
    if (!fields.username)       errors.username = 'Username is required.';
    if (!fields.firstName)      errors.firstName = 'First name is required.';
    if (!fields.lastName)       errors.lastName = 'Last name is required.';
    if (!fields.email)          errors.email = 'Email is required.';
    else if (!/\S+@\S+\.\S+/.test(fields.email)) errors.email = 'Enter a valid email address.';
    if (!fields.password)       errors.password = 'Password is required.';
    else if (fields.password.length < 8) errors.password = 'Password must be at least 8 characters.';
    if (fields.password !== fields.confirmPassword) errors.confirmPassword = 'Passwords do not match.';
    return errors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setFormError('');
    const errors = validate();
    setFieldErrors(errors);
    if (Object.keys(errors).length > 0) return;

    setLoading(true);
    const res = await register(fields.username, fields.firstName, fields.lastName, fields.email, fields.password);
    if (res.success) {
      navigate('/dashboard', { replace: true });
    } else {
      setFormError(res.error || 'Registration failed. Please try again.');
      setLoading(false);
    }
  };

  const inputStyle = (key) => ({
    paddingLeft: fieldErrors[key] ? undefined : undefined,
    borderColor: fieldErrors[key] ? 'var(--border-error)' : undefined,
  });

  return (
    <div className="login-page-wrapper">
      <div className="login-card-container" style={{ maxWidth: 520 }}>
        <div className="login-card-header">
          <div className="shield-icon-container" style={{ backgroundColor: 'var(--green-light)', color: 'var(--green)' }} aria-hidden="true">
            <UserPlus size={32} />
          </div>
          <h1 className="login-title">Create Account</h1>
          <p className="login-subtitle">Register to lodge and track grievances.</p>
        </div>

        {formError && (
          <div id={formErrorId} role="alert" aria-live="assertive" className="login-error-alert">
            <AlertCircle size={18} aria-hidden="true" />
            <span>{formError}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="login-form-element" noValidate aria-describedby={formError ? formErrorId : undefined}>
          {/* Username */}
          <div className="form-group-login">
            <label className="form-label-login" htmlFor="reg-username">Username</label>
            <div className="form-input-wrapper">
              <User className="input-field-icon" size={18} aria-hidden="true" />
              <input id="reg-username" type="text" className="form-input-login"
                placeholder="Choose a username" value={fields.username}
                onChange={set('username')} disabled={loading}
                autoComplete="username" aria-required="true"
                aria-invalid={!!fieldErrors.username}
                aria-describedby={fieldErrors.username ? 'err-username' : undefined}
                style={inputStyle('username')}
              />
            </div>
            <FieldError message={fieldErrors.username} id="err-username" />
          </div>

          {/* First + Last Name */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            <div className="form-group-login">
              <label className="form-label-login" htmlFor="reg-first">First Name</label>
              <input id="reg-first" type="text" className="form-input-login"
                placeholder="First name" value={fields.firstName}
                onChange={set('firstName')} disabled={loading}
                autoComplete="given-name" aria-required="true"
                aria-invalid={!!fieldErrors.firstName}
                style={{ paddingLeft: '1rem', ...inputStyle('firstName') }}
              />
              <FieldError message={fieldErrors.firstName} id="err-first" />
            </div>
            <div className="form-group-login">
              <label className="form-label-login" htmlFor="reg-last">Last Name</label>
              <input id="reg-last" type="text" className="form-input-login"
                placeholder="Last name" value={fields.lastName}
                onChange={set('lastName')} disabled={loading}
                autoComplete="family-name" aria-required="true"
                aria-invalid={!!fieldErrors.lastName}
                style={{ paddingLeft: '1rem', ...inputStyle('lastName') }}
              />
              <FieldError message={fieldErrors.lastName} id="err-last" />
            </div>
          </div>

          {/* Email */}
          <div className="form-group-login">
            <label className="form-label-login" htmlFor="reg-email">Email Address</label>
            <div className="form-input-wrapper">
              <Mail className="input-field-icon" size={18} aria-hidden="true" />
              <input id="reg-email" type="email" className="form-input-login"
                placeholder="you@example.com" value={fields.email}
                onChange={set('email')} disabled={loading}
                autoComplete="email" aria-required="true"
                aria-invalid={!!fieldErrors.email}
                aria-describedby={fieldErrors.email ? 'err-email' : undefined}
                style={inputStyle('email')}
              />
            </div>
            <FieldError message={fieldErrors.email} id="err-email" />
          </div>

          {/* Password */}
          <div className="form-group-login">
            <label className="form-label-login" htmlFor="reg-password">Password</label>
            <div className="form-input-wrapper" style={{ position: 'relative' }}>
              <Lock className="input-field-icon" size={18} aria-hidden="true" />
              <input id="reg-password" type={showPassword ? 'text' : 'password'}
                className="form-input-login" placeholder="Min 8 characters"
                value={fields.password} onChange={set('password')} disabled={loading}
                autoComplete="new-password" aria-required="true"
                aria-invalid={!!fieldErrors.password}
                aria-describedby={fieldErrors.password ? 'err-password' : undefined}
                style={{ paddingRight: '2.5rem', ...inputStyle('password') }}
              />
              <button type="button" onClick={() => setShowPassword(p => !p)}
                aria-label={showPassword ? 'Hide password' : 'Show password'}
                style={{ position: 'absolute', right: 10, top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text-muted)', padding: 4 }}>
                {showPassword ? <EyeOff size={16} aria-hidden="true" /> : <Eye size={16} aria-hidden="true" />}
              </button>
            </div>
            <FieldError message={fieldErrors.password} id="err-password" />
          </div>

          {/* Confirm Password */}
          <div className="form-group-login">
            <label className="form-label-login" htmlFor="reg-confirm">Confirm Password</label>
            <div className="form-input-wrapper">
              <Lock className="input-field-icon" size={18} aria-hidden="true" />
              <input id="reg-confirm" type="password" className="form-input-login"
                placeholder="Re-enter password" value={fields.confirmPassword}
                onChange={set('confirmPassword')} disabled={loading}
                autoComplete="new-password" aria-required="true"
                aria-invalid={!!fieldErrors.confirmPassword}
                aria-describedby={fieldErrors.confirmPassword ? 'err-confirm' : undefined}
                style={inputStyle('confirmPassword')}
              />
            </div>
            <FieldError message={fieldErrors.confirmPassword} id="err-confirm" />
          </div>

          <Button
            type="submit"
            variant="success"
            size="md"
            loading={loading}
            style={{ width: '100%', justifyContent: 'center', marginTop: '0.5rem' }}
          >
            {loading ? 'Creating Account…' : 'Register Account'}
          </Button>
        </form>

        <div className="login-card-footer">
          <p className="registration-prompt-text">
            Already have an account?{' '}
            <Link to="/login" className="register-now-link">Sign In Here</Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Register;
