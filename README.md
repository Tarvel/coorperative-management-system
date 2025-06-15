# Cooperative Management System

**CMS** is a Django-based web app for managing cooperative financial operations. It allows members to deposit, withdraw, apply for loans, and track dividends. Admins can manage accounts, approve transactions, distribute dividends, and monitor overall performance.

## Features

### Member
- **Dashboard** with account summary
- **Deposits & Withdrawals** (with eligibility checks)
- **Transaction History** (sortable, paginated)
- **Loan Applications** (with validation)
- **Dividend Tracking**

### Admin
- **Admin Dashboard** with cooperative overview
- **Member Management**
- **Approve/Reject Transactions & Loans**
- **Loan Repayment Management**
- **Dividend Distribution**
- **Cooperative Reports** 

### General
- Role-based **Authentication**
- **Notifications** for key events
- **Responsive UI** (Tailwind CSS)
- **Pagination**

## Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, Tailwind CSS
- **Database:** SQLite (dev), PostgreSQL (prod)


## Project Structure
CMS/
├── .vscode/  # Editor config (e.g., linting settings)
├── CMS/         # Project settings & URLs
├── base/                # App logic (models, views, templates)
├── templates/
├── manage.py
└── requirements.txt
