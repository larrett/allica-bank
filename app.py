from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_
from datetime import datetime
from loguru import logger
from starlette.requests import Request
from starlette.responses import JSONResponse

from database import db_instance
from exceptions import UserNotFoundException
from models.user import UserRead, UserCreate, User

app = FastAPI()


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP Exception: {exc.detail} | Path: {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail, "status": "error", "path": request.url.path},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {str(exc)} | Path: {request.url.path}")
    return JSONResponse(
        status_code=500,
        content={
            "message": "An internal server error occurred",
            "status": "error",
            "path": request.url.path,
        },
    )


@app.exception_handler(UserNotFoundException)
async def user_not_found_handler(request: Request, exc: UserNotFoundException):
    logger.warning(f"User Not Found: {exc.message} | Path: {request.url.path}")
    return JSONResponse(
        status_code=404,
        content={"message": exc.message, "status": "error", "path": request.url.path},
    )


def get_db():
    db_session = db_instance.get_connection()
    try:
        yield db_session
    finally:
        db_session.close()


@app.post("/users/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Attempting to create a user: {user.dict()}")
    try:
        date_of_birth = datetime.strptime(user.date_of_birth, "%Y-%m-%d").date()
        db_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            date_of_birth=date_of_birth,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logger.info(f"User created successfully: {db_user}")
        return UserRead.from_orm(db_user)
    except ValueError:
        logger.error(f"Invalid date format: {user.date_of_birth}")
        raise HTTPException(
            status_code=400, detail="Invalid date format. Use 'YYYY-MM-DD'."
        )
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred")


from sqlalchemy.sql import true

@app.get("/users/", response_model=list[UserRead])
def get_users(
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        date_of_birth: Optional[str] = None,
        db: Session = Depends(get_db),
):
    logger.info(
        f"Fetching users with filters: first_name={first_name}, last_name={last_name}, date_of_birth={date_of_birth}"
    )
    try:
        date_parsed = (
            datetime.strptime(date_of_birth, "%Y-%m-%d").date() if date_of_birth else None
        )

        filters = [
            User.first_name == first_name if first_name is not None else true(),
            User.last_name == last_name if last_name is not None else true(),
            User.date_of_birth == date_parsed if date_parsed is not None else true(),
        ]

        users = db.query(User).filter(and_(*filters)).all()

        if not users:
            raise UserNotFoundException("No users found matching the provided filters.")

        logger.info(f"Found {len(users)} user(s).")
        return [UserRead.from_orm(user) for user in users]

    except ValueError:
        logger.error(f"Invalid date format: {date_of_birth}")
        raise HTTPException(
            status_code=400, detail="Invalid date format. Use 'YYYY-MM-DD'."
        )
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred")
