# Stayease — Hotel Booking System (Backend API)

---

## 🚀 Overview

Stayease is a production-style backend system for a hotel booking platform, built using FastAPI.
It demonstrates clean architecture, secure authentication, and performance optimization using Redis caching.

The project simulates a real-world booking system where users can browse hotels, search rooms with filters, and make bookings with availability validation.

---

## ✨ Core Features

🔐 Authentication & Authorization: 
-JWT-based authentication (OAuth2 + custom login)
-Password hashing using bcrypt
-Role-based access control (Admin / User)
-Ownership-based permissions (users can only modify their own data)

🏨 Hotel & Room Management
-Create, update, delete hotels (admin-controlled)
-Add and manage rooms under hotels
-Room attributes:
-Type
-Capacity
-Amenities
-Price
-Availability

🔍 Smart Room Search
-Filter rooms by:
-Location
-Room type
-Price range
-Availability (check-in / check-out)
-Prevents overlapping bookings using date logic

📅 Booking System
-Book available rooms
-Automatic price calculation based on duration
-Prevents double booking using conflict detection
-Booking lifecycle:
-Confirmed
-Cancelled

⚡Redis Caching (Performance Optimization)
-Cached endpoint: /rooms/search
-TTL-based caching (60 seconds)
-Cache invalidation on:
-Room creation
-Booking creation
-Booking cancellation

---

## 📌 Verified behavior

First request → CACHE MISS
Subsequent request → CACHE HIT

---

## 🏗 Architecture

Follows a clean layered structure:

backend/
│
├── app/
│   ├── core/        # Security, dependencies, Redis
│   ├── db/          # Database setup
│   ├── models/      # SQLAlchemy models
│   ├── schemas/     # Pydantic schemas
│   ├── routes/      # API endpoints
│   ├── services/    # Business logic layer
│   └── main.py

Flow:

Route → Service → Model → Database

---

## 🧠 Tech Stack

-Python
-FastAPI
-SQLAlchemy
-SQLite
-Pydantic
-JWT (python-jose)
-Passlib (bcrypt)
-Redis
-Uvicorn
-python-dotenv

---

## ⚙️ Setup Instructions

1. Clone the repository
git clone https://github.com/peauli-ghosh/stayease-hotel-booking-system.git
cd stayease-hotel-booking-system/backend

2. Create virtual environment
python -m venv venv
venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Setup environment variables

Create .env file:

DATABASE_URL=sqlite:///./stayease.db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

5. Start Redis

Make sure Redis is running locally:

redis-server

6. Run the server
uvicorn app.main:app --reload

7. Open API Docs
http://127.0.0.1:8000/docs

---

## 📌 Key Endpoints

-Auth
-POST /auth/login
-GET /auth/me
-Hotels
-POST /hotels
-GET /hotels
-GET /hotels/search
-Rooms
-POST /rooms
-GET /rooms/search
-Bookings
-POST /bookings
-PUT /bookings/{id}/cancel
-GET /bookings/me

---

## ⚡Performance Note

Redis caching significantly reduces response time for repeated search queries by avoiding redundant database operations.

---

## 🔮 Future Improvements

-Replace SQLite with PostgreSQL
-Add pagination for search endpoints
-Introduce rate limiting
-Dockerize the application
-Add automated tests
-Implement advanced cache invalidation (key-based instead of flush)

---

## 📌 Conclusion

This project demonstrates:

-Real-world backend design patterns
-Secure authentication & authorization
-Efficient database handling
-Performance optimization with caching

---

## 👤 Author

**Peauli Ghosh**

[GitHub](www.github.com/peauli-ghosh) • 
[LinkedIn](www.linkedin.com/in/peauli-ghosh)