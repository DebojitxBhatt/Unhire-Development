import React from "react";
import devItImg from '../assets/images/dev-it.png';
import adminSupportImg from '../assets/images/admin-support.png';
import aiServicesImg from '../assets/images/ai-services.png';
import contentCopywritingImg from '../assets/images/content-copywriting.png';
import salesMarketingImg from '../assets/images/sales-marketing.png';
import creativeDesignImg from '../assets/images/creative-design.png';
import Footer from '../components/Footer';
import './Services.css';

const Services = () => (
    <>
        <div className="services-section">
            <div className="services-header">
                <h2 className="services-title">Services</h2>
                <button className="hire-now-btn">Hire now</button>
            </div>
            <div className="services-grid">
                <div className="service-card">
                    <img src={devItImg} alt="Development & IT" className="service-icon" />
                    <span className="service-title">Development & IT</span>
                </div>
                <div className="service-card">
                    <img src={adminSupportImg} alt="Admin and support" className="service-icon" />
                    <span className="service-title">Admin and support</span>
                </div>
                <div className="service-card">
                    <img src={aiServicesImg} alt="AI Services" className="service-icon" />
                    <span className="service-title">AI Services</span>
                </div>
                <div className="service-card">
                    <img src={contentCopywritingImg} alt="Content Creation & Copywriting" className="service-icon" />
                    <span className="service-title">Content Creation & Copywriting</span>
                </div>
                <div className="service-card">
                    <img src={salesMarketingImg} alt="Sales & Marketing" className="service-icon" />
                    <span className="service-title">Sales & Marketing</span>
                </div>
                <div className="service-card">
                    <img src={creativeDesignImg} alt="Creative and Design" className="service-icon" />
                    <span className="service-title">Creative and Design</span>
                </div>
            </div>
        </div>
        <Footer />
    </>
);

export default Services;
