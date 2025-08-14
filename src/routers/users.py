from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError
from datetime import timedelta
from src.configs.config import get_db
from src.schemas.users import UserCreate, UserResponse,LoginRequest
from src.utils.token import create_access_token, hash_password, verify_password
from src.services.tables import Tables

router = APIRouter()
table = Tables()


@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # Check if username already exists
        query = select(table.users).where(table.users.c.username == user.username)
        existing_user = db.execute(query).fetchone()

        if existing_user:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "Username already exists"}
            )

        # Hash password
        hashed_pw = hash_password(user.password)

        # Insert new user
        insert_stmt = insert(table.users).values(
            username=user.username,
            password_hash=hashed_pw
        ).returning(table.users)

        result = db.execute(insert_stmt)
        db.commit()

        new_user = result.fetchone()

        # Generate token
        access_token_expires = timedelta(minutes=60)
        token = create_access_token(user_id=new_user.id)



        # Return structured response
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "id": new_user.id,
                "username": new_user.username,
                "created_at": str(new_user.created_at),
                "token": token
            }
        )

    except SQLAlchemyError as db_err:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Database error occurred. Please try again later."}
        )
    except Exception as err:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": f"Unexpected error occurred: {str(err)}"}
        )


@router.post("/login", response_model=UserResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    try:
        # Find user by username
        query = select(table.users).where(table.users.c.username == login_data.username)
        user = db.execute(query).fetchone()

        if not user:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid username or password"}
            )

        # Verify password
        if not verify_password(login_data.password, user.password_hash):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid username or password"}
            )

        # Create access token
        access_token_expires = timedelta(minutes=60)
        token = create_access_token(user_id=user.id)



        # Return user info and token
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "id": user.id,
                "username": user.username,
                "created_at": str(user.created_at),
                "token": token
            }
        )

    except SQLAlchemyError:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Database error occurred. Please try again later."}
        )
    except Exception as err:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": f"Unexpected error occurred: {str(err)}"}
        )