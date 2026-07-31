import React from 'react';
import './Footer.css';

export const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="portal-footer">
      <div className="footer-top">
        <div className="footer-container">
          <div className="footer-grid">
            <div className="footer-info-col">
              <div className="footer-title">NyayaSetu</div>
              <p className="footer-desc">
                Integrated Grievance Redressal and Administrative Monitoring Project. A prototype designed to demonstrate transparent and AI-driven resolution workflows.
              </p>
            </div>
            
            <div className="footer-links-col">
              <div className="footer-section-title">Project Links</div>
              <ul className="footer-links-list">
                <li><a href="https://india.gov.in" target="_blank" rel="noopener noreferrer">National Portal of India</a></li>
                <li><a href="https://digitalindia.gov.in" target="_blank" rel="noopener noreferrer">Digital India Portal</a></li>
              </ul>
            </div>

            <div className="footer-contact-col">
              <div className="footer-section-title">Prototype Info</div>
              <p className="footer-contact-text">
                For project inquiries or demonstration details:<br />
                <strong>Email:</strong> project-nyayasetu@domain.com<br />
                <strong>Status:</strong> Development Prototype
              </p>
            </div>
          </div>
        </div>
      </div>
      
      <div className="footer-bottom">
        <div className="footer-container bottom-flex">
          <p className="copyright-text">
            &copy; {currentYear} NyayaSetu Project. Developed for demonstration purposes.
          </p>
          <div className="national-infonetics">
            <span className="badge-digital">Prototype Showcase</span>
          </div>
        </div>
      </div>
    </footer>
  );
};
