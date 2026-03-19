# Stayease – Hotel Booking Backend System

## Overview

Stayease is a backend system for a hotel booking platform, built step-by-step as part of a backend development internship. The project focuses on scalability, clean architecture, and real-world backend practices.

---

## Tech Stack

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* Uvicorn
* Python-dotenv

---

## Project Structure

```bash
backend/
│
├── app/
│   ├── main.py
│   ├── db/
│   │   └── database.py
│   ├── models/
│   │   └── user_model.py
│   ├── schemas/
│   │   └── user_schema.py
│   ├── routes/
│   │   └── user_routes.py
│   ├── services/
│   │   └── user_service.py
│
├── stayease.db
├── .env
├── requirements.txt
```

---

# Tasks

## Task 01: Basic REST API (CRUD Operations)

### Objective

Build a REST API for user management using FastAPI with clean architecture.

### Features

* Create user
* Retrieve all users
* Retrieve user by ID
* Update user
* Delete user
* Email validation
* Duplicate email prevention
* Proper HTTP status handling

### Limitations

* In-memory storage
* No authentication
* No database

---

## Task 02: Database Integration

### Objective

Integrate a relational database for persistent storage using SQLAlchemy.

### Features

* SQLite database integration
* ORM-based data handling
* Persistent storage
* CRUD operations using database
* Email uniqueness enforced
* Environment-based configuration using `.env`

### Improvements from Task 01

* Replaced in-memory storage with database
* Introduced models and DB layer
* Added configuration management

### Limitations

* No database migrations
* SQLite (not production DB)
* No authentication

---

## Task 03: Authentication & Authorization (Upcoming)

* JWT authentication
* Password hashing
* Role-based access (Customer / Manager)

---

## Task 04: Caching (Upcoming)

* Redis integration
* Performance optimization

---

## Task 05: Hotel Booking System (Upcoming)

* Hotels, rooms, bookings
* Full backend system

---

## Conclusion

The project evolves incrementally from a basic CRUD API to a full backend system. Each task builds on the previous one, ensuring a structured and scalable development process.

