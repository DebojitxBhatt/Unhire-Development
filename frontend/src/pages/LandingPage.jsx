import heroGraphic from '../assets/images/hero-graphic.png';
import howItWorksImg from '../assets/images/how-it-works.png';
import timeExecutionImg from '../assets/images/time-execution.png';
import claimDeliverImg from '../assets/images/claim-deliver.png';
import clientsApprovalImg from '../assets/images/clients-approval.png';
import devItImg from '../assets/images/dev-it.png';
import adminSupportImg from '../assets/images/admin-support.png';
import aiServicesImg from '../assets/images/ai-services.png';
import contentCopywritingImg from '../assets/images/content-copywriting.png';
import salesMarketingImg from '../assets/images/sales-marketing.png';
import creativeDesignImg from '../assets/images/creative-design.png';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { useNavigate } from 'react-router-dom';
import './LandingPage.css';


const LandingPage = () => {
    const navigate = useNavigate();
    return (
        <div className="landing-page">
            <Navbar />

            <main className="hero-section">
                <div className="hero-left">
                    <p className="hero-subtitle">Skip the job grind – discover a faster, smarter way to work together.</p>
                    <h1 className="hero-title">Unhire</h1>
                    <p className="hero-description">
                        A freelance platform that guarantees on-time delivery, every time. No missed deadlines, no excuses just reliable talent committed to your success
                    </p>
                    <div className="hero-buttons">
                        <button className="signup">Sign up</button>
                        <button className="login">login</button>
                    </div>
                </div>
                <div className="hero-right">
                    <img src={heroGraphic} alt="Hero Graphic" className="hero-image" />
                </div>
            </main>
            <section className="how-it-works-section">
                <h2 className="how-it-works-title">How it works</h2>
                <div className="how-it-works-content">
                    <div className="how-it-works-image">
                        <img src={howItWorksImg} alt="Post a Job" className="post-job-image" />
                    </div>
                    <div className="how-it-works-details">
                        <span className="how-it-works-subtitle">A next-generation freelance platform</span>
                        <h3 className="how-it-works-heading">Post a Job</h3>
                        <p className="how-it-works-description">
                            Clients post clear, detailed tasks with set deadlines ensuring smooth communication, timely delivery, and results you can count on
                        </p>
                        <button className="post-job-btn">post</button>
                    </div>
                </div>
            </section>

            {/* Time execution section */}
            <section className="time-execution-section">
                <div className="time-execution-content">
                    <div className="time-execution-image">
                        <img src={timeExecutionImg} alt="Time execution" className="time-execution-img" />
                    </div>
                    <div className="time-execution-details">
                        <span className="time-execution-subtitle">Deadlines or Depart.</span>
                        <h3 className="time-execution-heading">Time execution</h3>
                        <p className="time-execution-description">
                            Missed deadlines lead to removal from the platform. We protect clients by ensuring only reliable, committed freelancers stay.
                        </p>
                        <button className="time-execution-btn">join</button>
                    </div>
                </div>
            </section>

            {/* Claim and deliver section */}
            <section className="claim-deliver-section">
                <div className="claim-deliver-content">
                    <div className="claim-deliver-image">
                        <img src={claimDeliverImg} alt="Claim and Deliver" className="claim-deliver-img" />
                    </div>
                    <div className="claim-deliver-details">
                        <span className="claim-deliver-subtitle">you are the judge of your satisfaction</span>
                        <h3 className="claim-deliver-heading">claim and deliver</h3>
                        <p className="claim-deliver-description">
                            Freelancers claim your project, submit a draft, and you’re the judge—approve only when the work meets your highest standards.
                        </p>
                        <button className="claim-deliver-btn">start now</button>
                    </div>
                </div>
            </section>

            {/* Clients Approval section */}
            <section className="clients-approval-section">
                <div className="clients-approval-content">
                    <div className="clients-approval-image">
                        <img src={clientsApprovalImg} alt="Clients Approval" className="clients-approval-img" />
                    </div>
                    <div className="clients-approval-details">
                        <span className="clients-approval-subtitle">Rejections lower freelancer ratings.</span>
                        <h3 className="clients-approval-heading">Clients Approval</h3>
                        <p className="clients-approval-description">
                            Frequent rejections reduce a freelancer’s approval rating so you can feel confident you’re working with only the most reliable professionals
                        </p>
                        <button className="clients-approval-btn">join</button>
                    </div>
                </div>
            </section>

            {/* Why unhire section */}
            <section id="why-unhire" className="why-unhire-section">
                <h2 className="why-unhire-title">Why unhire?</h2>
                <div className="why-unhire-cards">
                    <div className="why-unhire-card">
                        <h3 className="why-unhire-card-title">Quality over Quantity</h3>
                        <p className="why-unhire-card-desc">
                            Freelancers grab tasks instantly, skipping the delays and back-and-forth so work starts right away.
                        </p>
                    </div>
                    <div className="why-unhire-card">
                        <h3 className="why-unhire-card-title">Constructive partnership</h3>
                        <p className="why-unhire-card-desc">
                            We vet freelancers and remove those who fail to meet our performance standards.
                        </p>
                    </div>
                </div>
            </section>

            {/* Transparent workflow card */}
            <section className="workflow-section">
                <div className="workflow-card">
                    <h3 className="workflow-card-title">Transparent workflow</h3>
                    <p className="workflow-card-desc">
                        Clients and freelancers collaborate through a real-time dashboard with a clear, shared project timeline.
                    </p>
                </div>
            </section>

            {/* Call to action section */}
            <section className="cta-section">
                <h2 className="cta-title">Ready to experience Unhire? want to get results in hours?</h2>
                <button className="cta-btn" onClick={() => navigate('/join-now')}>join</button>
            </section>
            <Footer />
        </div>
    );
}


export default LandingPage;
