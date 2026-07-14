# Trekking Management System

A Flask-based web application for managing trekking operations with separate dashboards for Admin, Staff, and Trekker users. The application provides trek management, booking management, staff assignment, and user authentication.

## Features

- Role-based authentication using Flask-Login
- Admin, Staff, and Trekker dashboards
- Trek CRUD operations
- Staff assignment to treks
- Trek booking and cancellation
- Booking history
- Trek history
- Booking status management
- Trek status management
- Search, filter, and pagination
- Slot availability management

## Tech Stack

- Python
- Flask
- SQLAlchemy
- SQLite
- HTML
- CSS
- Bootstrap 5
- Jinja2

## Installation

```bash
git clone <repository-url>
cd trekking-management-system

python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt

python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

## Project Structure

```
trekking-management-system/
│
├── app/
│   ├── models/
│   ├── routes/
│   ├── templates/
│   ├── static/
│   └── __init__.py
│
├── instance/
├── app.py
├── requirements.txt
└── README.md
```

## User Roles

### Admin
- Manage users
- Manage staff
- Manage treks
- Manage bookings
- Assign staff to treks

### Staff
- View assigned treks
- Update trek status

### Trekker
- Browse available treks
- Book and cancel treks
- View booking history

## Database

The application uses SQLite with SQLAlchemy ORM.

Main entities:

- Login
- User
- Staff
- Trek
- Booking

## License

This project was developed for educational purposes.
