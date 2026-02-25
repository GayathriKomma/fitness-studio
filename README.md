# Fitness Studio Booking API (Basic)

This is a small FastAPI app for a fictional fitness studio. It provides endpoints to sign up, log in, create classes, book classes and view your bookings.

Summary:
- Python + FastAPI
- SQLite database (file: fitness.db)
- JWT token authentication

Quick start

1. Create a virtual environment and install requirements:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; python -m pip install -r requirements.txt
```

2. Seed sample data (optional):

```powershell
python seed.py
```

3. Run the app:

```powershell
uvicorn main:app --reload
```

API endpoints

- POST /signup
- POST /login
- POST /classes (auth)
- GET /classes
- POST /book (auth)
- GET /bookings (auth)

Notes
- Times are stored in IST (Asia/Kolkata). Provide ISO datetimes; example: 2025-06-15T10:00:00Z (UTC) and the service will convert to IST.
- This is a basic implementation for assignment/demo purposes.
