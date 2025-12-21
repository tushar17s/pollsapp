# PollsApp — Secure Polling Web Application

PollsApp is a Django-based web application that allows users to create polls, vote securely, and view results with dynamic analytics.  
The project focuses on clean backend logic, data integrity, and proper separation of concerns rather than UI-heavy features.

This project was built to deeply understand Django ORM, authentication, authorization, and real-world backend workflows.

---

## Features

- User authentication (signup, login, logout)
- Poll creation with multiple options
- One-vote-per-user enforcement
- Dynamic result calculation (no derived data stored)
- Vote results visualization using Chart.js
- Comment system with owner-based moderation
- Hot poll highlighting based on vote count
- User-specific dashboard with analytics
- REST APIs built using Django REST Framework

---

## Tech Stack

- Backend: Django
- ORM: Django ORM (aggregation, annotations)
- Database: SQLite (PostgreSQL-ready)
- Frontend: HTML, CSS, Bootstrap
- Charts: Chart.js
- APIs: Django REST Framework

---

## Architecture & Design Decisions

- Business logic is handled in views, not templates
- Authorization checks are enforced at the view level
- Vote percentages are calculated dynamically to avoid stale data
- ORM aggregation (`annotate`, `count`, `exists`) is used for analytics
- Foreign key relationships are used to maintain data integrity
- REST APIs reuse the same models and logic as template-based views

---

## Setup Instructions (Local)


git clone <repository-url>
cd pollsapp
python -m venv myenv
source myenv/bin/activate   # Windows: myenv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

#  What I Learned

How Django handles authentication and request lifecycle

Proper use of ORM aggregation instead of manual data handling

Difference between objects and IDs in ForeignKey relationships

Why permissions should be enforced in views, not templates

How REST APIs coexist with template-rendered views

How to design features with security and scalability in mind

Future Improvements

Real-time voting updates using WebSockets

Advanced poll moderation features

Deployment with PostgreSQL

API authentication for external clients