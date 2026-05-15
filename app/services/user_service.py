from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories import UserRepository
from app.security.auth import get_password_hash, verify_password, create_access_token
from app.schemas import UserCreate
from datetime import timedelta

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def register_user(self, user: UserCreate):
        # Check if user already exists
        if self.user_repo.get_by_username(user.username):
            raise HTTPException(status_code=400, detail="Username already registered")
        if self.user_repo.get_by_email(user.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_password = get_password_hash(user.password)
        return self.user_repo.create(user, hashed_password)

    def authenticate_user(self, username: str, password: str):
        user = self.user_repo.get_by_username(username)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user

    def create_access_token(self, user):
        access_token_expires = timedelta(minutes=30)
        return create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )