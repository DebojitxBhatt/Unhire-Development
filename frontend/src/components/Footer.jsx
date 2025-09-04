import React from "react";
import "./Footer.css";

const Footer = () => (
    <footer className="footer-section">
        <div className="footer-content">
            <div className="footer-copyright">
                Copyright © 2025 Unhire Company .Evu. All rights reserved.
            </div>
            <div className="footer-links">
                <a href="#" className="footer-link">Terms and Conditions</a>
                <a href="#" className="footer-link">Meet the Team</a>
            </div>
            <div className="footer-social">
                <span>Follow us</span>
                <a href="#" className="footer-social-icon"><img src="/public/assets/icons/twitter.png" alt="Twitter" /></a>
                <a href="#" className="footer-social-icon"><img src="/public/assets/icons/instagram.png" alt="Instagram" /></a>
                <a href="#" className="footer-social-icon"><img src="/public/assets/icons/linkedin.png" alt="LinkedIn" /></a>
            </div>
        </div>
    </footer>
);

export default Footer;
