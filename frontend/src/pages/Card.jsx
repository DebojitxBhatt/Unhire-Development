import React from 'react';
import './Card.css';
import check from "../components/icons/check.png";
import time from "../components/icons/time.png";
import approval from "../components/icons/approval.png";

function Card({ title, imageURL, description }) {
    return (
        <div className="card">
            {/* Card Section: Post a Project */}
            <div className="card-container">
                <div className="image-container">
                    <img src={projectIcon} alt="Post a Project" />
                </div>
                <div className="card-content">
                    <div className="card-title">
                        <h3>Post a Project</h3>
                    </div>
                    <div className="card-description">
                        <p>Clients submit detailed tasks with deadlines and deliverables</p>
                    </div>
                </div>
            </div>

            {/* Card Section: Claim & Deliver */}
            <div className="card-container">
                <div className="image-container">
                    <img src={check} alt="Claim & Deliver" />
                </div>
                <div className="card-content">
                    <div className="card-title">
                        <h3>Claim & Deliver</h3>
                    </div>
                    <div className="card-description">
                        <p>Freelancers claim tasks and submit drafts before final delivery.</p>
                    </div>
                </div>
            </div>

            {/* Card Section: Timed Execution */}
            <div className="card-container">
                <div className="image-container">
                    <img src={time} alt="Timed Execution" />
                </div>
                <div className="card-content">
                    <div className="card-title">
                        <h3>Timed Execution</h3>
                    </div>
                    <div className="card-description">
                        <p>Deadlines are enforced. Missed timelines = removal from platform.</p>
                    </div>
                </div>
            </div>

            {/* Card Section: Client Approval */}
            <div className="card-container">
                <div className="image-container">
                    <img src={approval} alt="Client Approval" />
                </div>
                <div className="card-content">
                    <div className="card-title">
                        <h3>Client Approval</h3>
                    </div>
                    <div className="card-description">
                        <p>Clients approve or reject submissions. Rejections reduce freelancer standing.</p>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Card;
