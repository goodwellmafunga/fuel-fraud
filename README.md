# AI Fraud Monitoring System

An AI-powered fraud detection system designed to monitor transactions at fuel stations. The system uses machine learning models to flag fraudulent transactions and provides features for user management, transaction tracking, and reporting.

## Features

- **User Authentication**: Admins can manage users, and authenticated users can access their respective dashboards.
- **Transaction Management**: Users can submit transactions, view transaction history, and view flagged fraudulent transactions.
- **Station Management**: Admins can manage fuel stations including adding new stations and deleting them.
- **Fraud Detection**: Transactions are checked for fraud using a machine learning model. Flagged transactions are recorded in the system for further review.
- **Reports**: Generate and download CSV and PDF reports of flagged transactions.

## Getting Started

### Prerequisites

To run this project locally or on a server, ensure you have the following installed:

- Python 3.12 or above
- pip (Python package manager)
- Git (for version control)
- Flask (Web framework for Python)
- Gunicorn (WSGI HTTP Server for Python)
- SQLAlchemy (ORM for database management)
- Flask-Login (for user session management)
- Other dependencies mentioned in `requirements.txt`

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/goodwellmafunga/fuel-fraud.git
   cd ai-fraud-monitoring-system
