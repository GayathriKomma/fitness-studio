from database import SessionLocal, engine
import models
from auth import get_password_hash
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo


def seed():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
       
        if not db.query(models.User).filter(models.User.email == "demo@studio.com").first():
            user = models.User(name="Demo User", email="demo@studio.com", hashed_password=get_password_hash("password123"))
            db.add(user)

        ist = ZoneInfo("Asia/Kolkata")
        now = datetime.now(timezone.utc).astimezone(ist)
      
        if not db.query(models.FitnessClass).count():
            c1 = models.FitnessClass(name="Yoga Flow", date_time=(now + timedelta(days=1)), instructor="John Doe", available_slots=20)
            c2 = models.FitnessClass(name="HIIT Session", date_time=(now + timedelta(days=2)), instructor="Jane Smith", available_slots=10)
            db.add_all([c1, c2])

        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
    print("Seeded database")
