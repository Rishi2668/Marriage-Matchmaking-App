# User Profile Management API

A FastAPI application for managing user profiles with matching capabilities.

## Features

- Create, read, update, and delete user profiles
- Find potential matches based on configurable criteria
- Email validation
- SQLite database for data storage

## Project Structure

- `main.py`: API endpoints and business logic
- `models.py`: SQLAlchemy database models
- `schemas.py`: Pydantic schemas for data validation
- `database.py`: Database configuration
- `requirements.txt`: Project dependencies

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd Marriage-Matchmaking-App-main
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

Start the application with Uvicorn:
```
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API Endpoints

### User Management

- `POST /users/`: Create a new user
- `GET /users/`: List all users
- `GET /users/{user_id}`: Get a specific user
- `PUT /users/{user_id}`: Update a user
- `DELETE /users/{user_id}`: Delete a user

### Matching

- `GET /users/{user_id}/matches`: Find potential matches

The matching endpoint supports the following query parameters:
- `filter_by_city` (default: false): Filter matches by same city
- `filter_by_interests` (default: false): Filter matches by shared interests

Example URL patterns:
- `/users/1/matches` - Basic matching (only opposite gender)
- `/users/1/matches?filter_by_city=true` - Match by city and opposite gender
- `/users/1/matches?filter_by_interests=true` - Match by interests and opposite gender
- `/users/1/matches?filter_by_city=true&filter_by_interests=true` - Match by city, interests, and opposite gender



