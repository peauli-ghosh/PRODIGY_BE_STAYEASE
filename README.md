# Stayease – Hotel Booking Backend System

## Overview

Stayease is a backend system for a hotel booking platform, built step-by-step as part of a backend development internship. The project focuses on scalability, clean architecture, security, and real-world backend practices.

---

## Tech Stack

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* Uvicorn
* Python-dotenv
* JWT (python-jose)
* Passlib (bcrypt)

---

## Project Structure

```bash
backend/
│
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── security.py
│   │   └── deps.py
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

---

## Task 03: Authentication & Authorization ✅

### Objective

Secure the backend using authentication and authorization mechanisms.

### Features

#### 🔐 Authentication

* JWT-based authentication
* Login system:

  * OAuth2 login (`/login`) for Swagger
  * Custom login (`/auth/login`) for frontend
* Password hashing using bcrypt
* Token-based session handling

#### 🛡 Authorization

* Role-based access control (Admin / Customer)
* Ownership-based restrictions:

  * Users can only update/delete their own profile
* Admin rules:

  * Can delete customers
  * Cannot delete other admins
  * Cannot update other users

#### 🔒 Security Enhancements

* Password never exposed in API responses
* Role normalization (case-insensitive handling)
* Protected routes using dependency injection
* Proper HTTP error handling (401 / 403 / 404)

#### ⚙️ System Design

* Clean separation of concerns:

  * Routes → Services → Models
* Dependency-based authentication system
* Stateless authentication using JWT

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

The project evolves from a basic CRUD API to a secure, scalable backend system. With authentication, role-based access control, and persistent storage implemented, the foundation is now strong enough to build full business logic such as hotel and booking management.
