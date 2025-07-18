from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, EmailStr
from typing import Optional

from auth.deps import get_db
from auth.jwt_handler import create_access_token, get_password_hash, verify_password
from auth.models import User
from memory.hybrid_memory import hybrid_memory
from utils.logger import logger

router = APIRouter(prefix="/auth", tags=["authentication"])

# Pydantic models
class UserSignup(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    username: str


@router.post("/signup", response_model=TokenResponse)
async def signup(user_data: UserSignup, db: AsyncSession = Depends(get_db)):
    """Create a new user account."""
    print(f"🔵 [SIGNUP API] Request received - Username: {user_data.username}, Email: {user_data.email}")
    try:
        # Check if user already exists
        print(f"🟡 [SIGNUP API] Checking if user already exists...")
        stmt = select(User).where(
            (User.username == user_data.username) | (User.email == user_data.email)
        )
        result = await db.execute(stmt)
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            print(f"❌ [SIGNUP API] User already exists - Username: {user_data.username}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already registered"
            )
        
        # Create new user
        print(f"🟡 [SIGNUP API] Creating new user...")
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        print(f"✅ [SIGNUP API] User created in database: {new_user.id}")
        
        # Initialize user in memory systems
        print(f"🟡 [SIGNUP API] Initializing user in memory systems...")
        try:
            await hybrid_memory.create_user_memory(
                user_id=str(new_user.id),
                email=user_data.email,
                first_name=user_data.first_name or "",
                last_name=user_data.last_name or ""
            )
            print(f"✅ [SIGNUP API] Memory systems initialized for user: {new_user.username}")
            logger.info(f"Initialized memory systems for user: {new_user.username}")
        except Exception as e:
            print(f"⚠️ [SIGNUP API] Failed to initialize memory systems: {e}")
            logger.warning(f"Failed to initialize memory systems for user {new_user.username}: {e}")
            # Don't fail signup if memory initialization fails
        
        # Create access token
        print(f"🟡 [SIGNUP API] Creating access token...")
        access_token = create_access_token(data={"sub": new_user.id})
        
        print(f"✅ [SIGNUP API] Signup successful - User: {new_user.username}, ID: {new_user.id}")
        logger.info(f"New user created: {new_user.username}")
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user_id=str(new_user.id),
            username=str(new_user.username)
        )
        
    except HTTPException:
        print(f"❌ [SIGNUP API] HTTP Exception raised")
        await db.rollback()
        raise
    except Exception as e:
        print(f"❌ [SIGNUP API] Error: {e}")
        await db.rollback()
        logger.error(f"Signup error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    """Authenticate user and return JWT token."""
    print(f"🔵 [LOGIN API] Request received - Username: {user_data.username}")
    try:
        # Find user by username
        print(f"🟡 [LOGIN API] Finding user in database...")
        stmt = select(User).where(User.username == user_data.username)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user or not verify_password(user_data.password, str(user.hashed_password)):
            print(f"❌ [LOGIN API] Authentication failed - Username: {user_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        print(f"🟡 [LOGIN API] Creating access token...")
        access_token = create_access_token(data={"sub": user.id})
        
        print(f"✅ [LOGIN API] Login successful - User: {user.username}, ID: {user.id}")
        logger.info(f"User logged in: {user.username}")
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user_id=str(user.id),
            username=str(user.username)
        )
        
    except HTTPException:
        print(f"❌ [LOGIN API] HTTP Exception raised")
        raise
    except Exception as e:
        print(f"❌ [LOGIN API] Error: {e}")
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        ) 