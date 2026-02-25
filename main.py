from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import schemas, models, crud
from schemas import UserCreate, ClassCreate, BookingCreate, UserOut, ClassOut, BookingOut
from models import User, FitnessClass, Booking
from crud import get_user_by_email, create_user, authenticate_user, create_class, get_upcoming_classes, create_booking, get_bookings_for_user
from database import session, engine
from auth import get_current_user, create_access_token



models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fitness Studio Booking API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
   
    db = session()
    try:
        yield db
    finally:
        db.close()


@app.post("/signup", response_model=schemas.UserOut)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    existing = crud.get_user_by_email(db, user.email)
    if existing:

        raise HTTPException(status_code=400, detail="A user with that email already exists")
    return crud.create_user(db, user)


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
      
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


@app.post("/classes", response_model=schemas.ClassOut)
def create_class(class_in: schemas.ClassCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    
    return crud.create_class(db, class_in)


@app.get("/classes", response_model=list[schemas.ClassOut])
def list_classes(db: Session = Depends(get_db)):

    return crud.get_upcoming_classes(db)


@app.post("/book", response_model=schemas.BookingOut)
def book_slot(booking_in: schemas.BookingCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
   
    booking = crud.create_booking(db, current_user, booking_in)
    if not booking:
        raise HTTPException(status_code=400, detail="Could not complete booking — the class may be full or does not exist")
    return booking


@app.get("/bookings", response_model=list[schemas.BookingOut])
def my_bookings(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):

    return crud.get_bookings_for_user(db, current_user.id)
 