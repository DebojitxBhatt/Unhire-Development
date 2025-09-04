import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';
import arrow from "../assets/images/arrow.png";

const Navbar = () => (
    <nav className="navbar">
        <div className="navbar-left">
            <img src={arrow} alt="Unhire Logo" className="logo" />
        </div>
        <div className="navbar-center">
            <a href="#why-unhire" className="nav-link active">Why unhire?</a>
            <Link to="/services" className="nav-link services-link">Services</Link>
        </div>
        <div className="navbar-right">
            <a href="#team" className="nav-link meet-team-text">Meet team</a>
            <button className="join-now">Join now</button>
        </div>
    </nav>
);

export default Navbar;
