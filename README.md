# Unhire — Freelance Marketplace That Guarantees Delivery

**Unhire** is a freelance platform built to eliminate unreliable deliveries, missed deadlines, and communication issues between clients and freelancers. Our system emphasizes accountability, structured execution timelines, and performance-based participation. If you've been burned by freelance platforms before, Unhire is the solution.

**Landing Page**
<img width="1040" height="724" alt="landing" src="https://github.com/user-attachments/assets/2fbaa9a5-4056-4482-8302-03c17fd7ff22" />


<img width="1041" height="607" alt="Screenshot 2025-07-22 at 18 10 55" src="https://github.com/user-attachments/assets/965c529b-8fa6-4567-a90b-8409c7645828" />

---

## 📌 Problem Statement

In today’s freelance market, clients often struggle to find qualified professionals who can execute tasks precisely and on time. Many end up hiring unverified freelancers who either miss deadlines or fail to meet expectations, leading to frustration, delays, and wasted resources.

## 🎯 Our Solution

Unhire matches clients with pre-vetted, qualified freelancers and ensures accountability through:

- Strict draft and final submission timelines
- A structured warning and rejection system
- First-come-first-serve task claiming
- A transparent review and auto-removal system for underperformers

---

## ✨ Key Features

- Timed task submissions (draft & final phases)
- Draft approval before final submission
- Auto-removal of freelancers with repeated failures
- Role-based dashboards for clients, freelancers, and admins
- Real-time notifications (email & in-app)
- Performance tracking and client feedback system
- Secure authentication (JWT-based)

---

## ⚙️ Tech Stack

Frontend: React, Tailwind CSS, shadcn/ui
Backend: Django, Django REST Framework
Database: MySQL or PostgreSQL
Authentication: JWT
DevOps: Docker (for local setup)

---

## 📊 System Design Summary

- Architecture: Monolithic backend + React SPA frontend
- Authentication: Token-based (JWT)
- Core Modules:

  - User roles & registration
  - Task lifecycle (create → claim → draft → review → final)
  - Warning/strike system
  - Notifications & reviews
  - Admin moderation dashboard

---

## ✅ Functional Requirements

- Users can register/login as Client, Freelancer, or Admin
- Clients can post tasks with clear requirements and timelines
- Freelancers can view and claim available tasks
- Each task goes through a draft and final submission stage
- Clients must approve or reject drafts with feedback
- Final submissions are expected within deadline after draft approval
- Freelancers receive automatic warnings for missed deadlines or rejected final submissions
- Freelancers are removed after receiving 3 warnings
- Clients and freelancers can leave reviews
- Admins can mediate disputes and manage users

---

## 📈 Non-Functional Requirements

- Fast API responses under 300ms
- 99.9% platform uptime
- Scalable to 10,000+ concurrent users
- Fully responsive and mobile-ready
- Secure access via HTTPS and token-based auth
- Maintainable, modular codebase

---

## 🧪 Manual Setup

### Backend (Django)

1. Navigate to the backend directory: `cd backend`
2. Create a virtual environment: `python -m venv env`
3. Activate it:

   - macOS/Linux: `source env/bin/activate`
   - Windows: `env\Scripts\activate`

4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Start the server: `python manage.py runserver`

### Frontend (React)

1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Start development server: `npm start`

Access:

- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend API: [http://localhost:8000/api/](http://localhost:8000/api/)

---

## 🔮 Future Roadmap

- In-app messaging between clients and freelancers
- Escrow payment and automated invoicing
- AI-based skill matching and pricing
- Freelancer performance analytics
- Badging system for top performers
- Auto-reschedule and task reassignment system

---

## 🤝 Contributing

We welcome contributions! To get started:

1. Fork this repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m "feat: added XYZ"`)
4. Push to your branch (`git push origin feature/your-feature`)
5. Submit a pull request

Style guides:

- React: Use Prettier formatting and ESLint
- Python: Follow PEP8 conventions

---

## 👥 Teams and Contact

**Project Lead**: \[Abdul Rahman]
Email: [abdu@evu.com](mailto:abdul@evu.com)
GitHub: [https://github.com/Abdul17rahman/unhire](https://github.com/Abdul17rahman/unhire)

**Co-Lead**: \[Danyellez Ramires]
Email: [danyellez@evu.com](mailto:danyellez@evu.com)
GitHub: [https://github.com/Danellyz/unhire](https://github.com/Danellyz/unhire)

\[Rajnil Prasad]
Email: [rajnil@evu.com](mailto:rajnil@evu.com)
GitHub: [https://github.com/rajnilprasad/unhire](https://github.com/rajnilprasad/unhire)

Website: [https://unhire.com](https://unhire.com) _(coming soon)_

For urgent collaboration or access:

- Message us on [LinkedIn](https://www.linkedin.com/company/90839042/admin/dashboard/)

---

## 📄 License

This project is a product of EVU Ventures under the MIT License.

---

**© 2025 Unhire** — Changing the freelance experience one task at a time.
