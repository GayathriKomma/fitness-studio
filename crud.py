from sqlalchemy.orm import Session
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import models, schemas
from auth import get_password_hash, verify_password


IST = ZoneInfo("Asia/Kolkata")


def _to_ist(dt):
   
    return dt.astimezone(IST)


def get_user_by_email(db: Session, email: str):
   
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
  
    hashed = get_password_hash(user.password)
    db_user = models.User(name=user.name, email=user.email, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str):
   
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_class(db: Session, class_in: schemas.ClassCreate):
   
    dt_str = class_in.dateTime.replace("Z", "+00:00")
    dt = datetime.fromisoformat(dt_str)
    dt_ist = _to_ist(dt)
    cls = models.FitnessClass(
        name=class_in.name,
        date_time=dt_ist,
        instructor=class_in.instructor,
        available_slots=class_in.availableSlots,
    )
    db.add(cls)
    db.commit()
    db.refresh(cls)
    return cls


def get_upcoming_classes(db: Session):
  
    now_ist = _to_ist(datetime.now(timezone.utc))
    classes = (
        db.query(models.FitnessClass)
        .filter(models.FitnessClass.date_time >= now_ist)
        .order_by(models.FitnessClass.date_time)
        .all()
    )
    return classes


def create_booking(db: Session, user: models.User, booking_in: schemas.BookingCreate):
   
    try:
        cls = (
            db.query(models.FitnessClass)
            .filter(models.FitnessClass.id == booking_in.class_id)
            .with_for_update()
            .first()
        )
    except Exception:
      
        cls = db.query(models.FitnessClass).filter(models.FitnessClass.id == booking_in.class_id).first()

    if not cls:
        return None
    if cls.available_slots <= 0:
        return None

    cls.available_slots = cls.available_slots - 1
    booked_at = _to_ist(datetime.now(timezone.utc))
    booking = models.Booking(
        class_id=cls.id,
        user_id=user.id,
        client_name=booking_in.client_name,
        client_email=booking_in.client_email,
        booked_at=booked_at,
    )
    db.add(booking)
    db.add(cls)
    db.commit()
    db.refresh(booking)
    return booking


def get_bookings_for_user(db: Session, user_id: int):
 
    return db.query(models.Booking).filter(models.Booking.user_id == user_id).all()
