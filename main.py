
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_
from database import SessionLocal, engine, Base
import models, schemas
import re
import json
from sqlalchemy import func
app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def validate_email(email: str) -> bool:
    
    """Validate email format using regex pattern"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        if not validate_email(user.email):
            raise HTTPException(status_code=400, detail="Invalid email format")

        existing_user = db.query(models.User).filter(models.User.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        db_user = models.User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, db: Session = Depends(get_db)):
    try:
        return db.query(models.User).offset(skip).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    try:
        db_user = db.query(models.User).filter(models.User.id == user_id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")

        if user.email is not None:
            if not validate_email(user.email):
                raise HTTPException(status_code=400, detail="Invalid email format")
            existing_user = db.query(models.User).filter(models.User.email == user.email).first()
            if existing_user and existing_user.id != user_id:
                raise HTTPException(status_code=400, detail="Email already registered")

        update_data = user.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)

        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        db_user = db.query(models.User).filter(models.User.id == user_id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        db.delete(db_user)
        db.commit()
        return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/users/{user_id}/matches", response_model=list[schemas.User])
def find_matches(
    user_id: int,
    filter_by_city: bool = False,  
    filter_by_interests: bool = False,  
    db: Session = Depends(get_db)
):
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        opposite_gender = "female" if user.gender.lower() == "male" else "male"

        matches_query = db.query(models.User).filter(
            models.User.id != user_id,
            models.User.gender.ilike(opposite_gender)
        )

        
        if filter_by_city:
            matches_query = matches_query.filter(models.User.city.ilike(user.city))

        potential_matches = matches_query.all()

        matches_with_scores = []
        for match in potential_matches:
            user_interests = set(i.lower().strip() for i in (user.interests or []))  # Normalize
            match_interests = set(i.lower().strip() for i in (match.interests or []))  # Normalize
            shared_interests = user_interests.intersection(match_interests)

       
            if not filter_by_interests or shared_interests:
                matches_with_scores.append((match, len(shared_interests)))

      
        matches_with_scores.sort(key=lambda x: x[1], reverse=True)
        top_matches = [match for match, _ in matches_with_scores]

        return top_matches
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
