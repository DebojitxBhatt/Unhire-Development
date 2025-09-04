import React from "react";
import recruiterImg from '../assets/images/recruiter.png';
import freelancerImg from '../assets/images/freelancer.png';
import Footer from '../components/Footer';
import './JoinNow.css';

const JoinNow = () => (
    <div className="join-now-page">
        <h2 className="join-now-title">choose an Account</h2>
        <div className="join-now-options">
            <div className="join-now-card">
                <img src={recruiterImg} alt="Recruiter" className="join-now-img" />
                <button className="join-now-btn recruiter-btn">Recruiter</button>
            </div>
            <div className="join-now-card">
                <img src={freelancerImg} alt="Freelancer" className="join-now-img" />
                <button className="join-now-btn freelancer-btn">Freelancer</button>
            </div>
        </div>
        <Footer />
    </div>
);

export default JoinNow;
