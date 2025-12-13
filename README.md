# 🗳️ Dynamic Polling & Voting Web Application  
A full-stack polling platform built with **Django**, **PostgreSQL**, and **Chart.js**, allowing users to create polls, vote securely, and view results with real-time graphical analytics.

---

## 🚀 Features

### 🔐 Authentication System
- User signup, login, logout
- Session-based authentication
- Access control for poll creation & voting
- Unauthorized users restricted from voting

### 📊 Poll Creation
- Create polls with multiple dynamic options
- Add category, description, visibility, and expiry date
- JavaScript-based dynamic option fields

### 🗳️ Secure Voting System
- One vote per user (duplicate-vote prevention)
- URL validation to prevent poll/option tampering
- Real-time vote recording

### 📈 Results & Analytics
- Vote count per option using Django ORM (`annotate`)
- Percentage calculations for each option
- Interactive charts using **Chart.js**:
  - Pie Chart
  - Bar Chart
- Total votes summary

### 🧩 REST API (Django REST Framework)
- `/api/polls/` — List all polls  
- `/api/polls/<id>/` — Poll details  
- `/api/polls/<id>/vote/` — Submit vote  
- `/api/polls/<id>/results/` — Poll results  

### ⚙️ Admin Dashboard
- Manage users, polls, options, votes
- View analytics & stats
- Category filters & monthly poll insights

### 🔧 Deployment & DB
- SQLite for development, PostgreSQL for production
- Environment variable-based configuration
- Deployed on Render / Railway (optional)

---

## 🛠️ Tech Stack

**Backend:** Django, Django REST Framework  
**Frontend:** HTML, CSS, Bootstrap, JavaScript, Chart.js  
**Database:** PostgreSQL / SQLite  
**Tools:** Git, GitHub, VS Code, Postman  

---

## 📂 Project Structure

