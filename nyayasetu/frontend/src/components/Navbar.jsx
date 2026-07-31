import React, { useState, useCallback } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useThemeContext } from '../context/ThemeContext';
import {
  Scale, LayoutDashboard, PlusCircle, FileText,
  LogOut, LogIn, Menu, X, User, Sun, Moon
} from 'lucide-react';
import './Navbar.css';

export const Navbar = () => {
  const { user, logout } = useAuth();
  const { isDark, toggleTheme } = useThemeContext();
  const navigate = useNavigate();
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleLogout = useCallback(async () => {
    await logout();
    navigate('/');
    setMobileMenuOpen(false);
  }, [logout, navigate]);

  const closeMobile = useCallback(() => setMobileMenuOpen(false), []);

  const isActive = (path) => location.pathname === path;

  const navLinkProps = (path) => ({
    to: path,
    className: `nav-link-item ${isActive(path) ? 'active' : ''}`,
    'aria-current': isActive(path) ? 'page' : undefined,
  });

  const mobileNavLinkProps = (path) => ({
    to: path,
    className: `mobile-link-item ${isActive(path) ? 'active' : ''}`,
    'aria-current': isActive(path) ? 'page' : undefined,
    onClick: closeMobile,
  });

  return (
    <header className="navbar-header">
      {/* India National Tricolor Decorative Ribbon */}
      <div className="tricolor-ribbon" aria-hidden="true">
        <div className="orange-stripe" />
        <div className="white-stripe" />
        <div className="green-stripe" />
      </div>

      <nav
        className="navbar-container"
        role="navigation"
        aria-label="Main navigation"
      >
        <Link to="/" className="navbar-brand" aria-label="NyayaSetu home">
          <div className="brand-logo">
            <Scale className="logo-icon" size={28} aria-hidden="true" />
          </div>
          <div className="brand-text">
            <span className="brand-title">NYAYA SETU</span>
            <span className="brand-subtitle">Grievance Redressal Prototype</span>
          </div>
        </Link>

        {/* Desktop Navigation */}
        <div className="desktop-nav">
          <ul className="nav-links" role="list">
            <li>
              <Link {...navLinkProps('/')}>Home</Link>
            </li>

            {user && (
              user.role === 'citizen' ? (
                <>
                  <li>
                    <Link {...navLinkProps('/dashboard')}>
                      <LayoutDashboard size={16} aria-hidden="true" className="link-icon" />
                      Dashboard
                    </Link>
                  </li>
                  <li>
                    <Link {...navLinkProps('/complaints')}>
                      <FileText size={16} aria-hidden="true" className="link-icon" />
                      My Complaints
                    </Link>
                  </li>
                  <li>
                    <Link {...navLinkProps('/complaints/lodge')} className={`nav-link-item lodge-btn ${isActive('/complaints/lodge') ? 'active' : ''}`}>
                      <PlusCircle size={16} aria-hidden="true" className="link-icon" />
                      Lodge Grievance
                    </Link>
                  </li>
                </>
              ) : (
                <>
                  <li>
                    <Link {...navLinkProps('/dashboard')}>
                      <LayoutDashboard size={16} aria-hidden="true" className="link-icon" />
                      Officer Dashboard
                    </Link>
                  </li>
                  <li>
                    <Link {...navLinkProps('/complaints')}>
                      <FileText size={16} aria-hidden="true" className="link-icon" />
                      Assigned Grievances
                    </Link>
                  </li>
                </>
              )
            )}
          </ul>

          <div className="auth-section">
            {/* Dark / Light mode toggle */}
            <button
              onClick={toggleTheme}
              className="theme-toggle-btn"
              aria-label={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
              title={isDark ? 'Light mode' : 'Dark mode'}
            >
              {isDark ? <Sun size={18} /> : <Moon size={18} />}
            </button>

            {user ? (
              <div className="user-profile-badge">
                <div className="user-info">
                  <User size={15} className="user-badge-icon" aria-hidden="true" />
                  <span className="username-text" title={user.username}>
                    {user.firstName} {user.lastName}
                  </span>
                  <span className="role-tag">{user.role}</span>
                </div>
                <button
                  onClick={handleLogout}
                  className="logout-btn-nav"
                  aria-label="Logout"
                  title="Logout"
                >
                  <LogOut size={15} aria-hidden="true" />
                </button>
              </div>
            ) : (
              <Link to="/login" className="login-btn-nav" aria-label="Login or Register">
                <LogIn size={15} className="link-icon" aria-hidden="true" />
                Login / Register
              </Link>
            )}
          </div>
        </div>

        {/* Mobile hamburger */}
        <button
          className="mobile-menu-toggle"
          onClick={() => setMobileMenuOpen(prev => !prev)}
          aria-label={mobileMenuOpen ? 'Close menu' : 'Open menu'}
          aria-expanded={mobileMenuOpen}
          aria-controls="mobile-nav-menu"
        >
          {mobileMenuOpen ? <X size={24} aria-hidden="true" /> : <Menu size={24} aria-hidden="true" />}
        </button>
      </nav>

      {/* Mobile Navigation */}
      {mobileMenuOpen && (
        <div id="mobile-nav-menu" className="mobile-nav-menu" role="dialog" aria-label="Mobile navigation">
          <ul className="mobile-nav-links" role="list">
            <li><Link {...mobileNavLinkProps('/')}>Home</Link></li>

            {user ? (
              <>
                {user.role === 'citizen' ? (
                  <>
                    <li><Link {...mobileNavLinkProps('/dashboard')}>Dashboard</Link></li>
                    <li><Link {...mobileNavLinkProps('/complaints')}>My Complaints</Link></li>
                    <li>
                      <Link
                        to="/complaints/lodge"
                        className={`mobile-link-item lodge-mobile-btn ${isActive('/complaints/lodge') ? 'active' : ''}`}
                        onClick={closeMobile}
                      >
                        Lodge Grievance
                      </Link>
                    </li>
                  </>
                ) : (
                  <>
                    <li><Link {...mobileNavLinkProps('/dashboard')}>Officer Dashboard</Link></li>
                    <li><Link {...mobileNavLinkProps('/complaints')}>Assigned Grievances</Link></li>
                  </>
                )}

                <li className="mobile-user-info-section">
                  <div className="mobile-user-details">
                    <User size={17} aria-hidden="true" />
                    <span>{user.firstName} {user.lastName} ({user.role})</span>
                  </div>
                  <button
                    onClick={handleLogout}
                    className="mobile-logout-btn"
                    aria-label="Logout"
                  >
                    <LogOut size={15} aria-hidden="true" className="link-icon" />
                    Logout
                  </button>
                </li>

                <li>
                  <button
                    onClick={() => { toggleTheme(); closeMobile(); }}
                    className="mobile-theme-btn"
                    aria-label={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
                    style={{
                      display: 'flex', alignItems: 'center', gap: '0.5rem',
                      width: '100%', padding: '0.6rem 1rem',
                      background: 'none', border: 'none',
                      color: 'var(--text-body)', cursor: 'pointer', fontSize: 'var(--font-size-sm)',
                    }}
                  >
                    {isDark ? <Sun size={16} aria-hidden="true" /> : <Moon size={16} aria-hidden="true" />}
                    {isDark ? 'Light Mode' : 'Dark Mode'}
                  </button>
                </li>
              </>
            ) : (
              <li>
                <Link to="/login" className="mobile-login-btn" onClick={closeMobile}>
                  <LogIn size={15} aria-hidden="true" className="link-icon" />
                  Login / Register
                </Link>
              </li>
            )}
          </ul>
        </div>
      )}
    </header>
  );
};

export default Navbar;
