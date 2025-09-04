import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import Services from './pages/Services';
import JoinNow from './pages/JoinNow';
import './App.css';
import Card from './pages/Card';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/services" element={<Services />} />
        <Route path="/join-now" element={<JoinNow />} />
      </Routes>
    </Router>
  );
}

export default App;
