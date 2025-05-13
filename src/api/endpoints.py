from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from src.models.address import Address
from src.models.user import User
from src.models.user_event import UserEvent
from src.schemas.user_schema import AddressList, EventList, UserList
from src.tasks.process_csv import process_csv_file

from src.core.database import get_db
router = APIRouter()

@router.post("/upload-csv")
def upload_csv(file: UploadFile = File(...)):
    if file.content_type != "text/csv":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type. Only CSV files are allowed.")

    content = file.file.read()
    task = process_csv_file.delay(content)
    return {"message": "File received and processing started", "task_id": task.id}

@router.get("/users", response_model=UserList)
def users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.execute(select(User).offset(skip).limit(limit))
    return {"users": users.scalars().all()}

@router.get("/addresses", response_model=AddressList)
def addresses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    addresses = db.execute(select(Address).options(selectinload(Address.user)).offset(skip).limit(limit))
    return {"addresses": addresses.scalars().all()}

@router.get("/events", response_model=EventList)
def events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    events = db.execute(select(UserEvent).offset(skip).limit(limit))
    return {"events": events.scalars().all()}

@router.get("/health-chelk")
def health_check():
    return {"message": "OK", }

