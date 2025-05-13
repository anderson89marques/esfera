from datetime import datetime
from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.core.database import Base
from src.models.user import User
from src.models.user_event import UserEvent
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


@pytest.fixture(scope="session")
def db():
    engine = create_engine('sqlite:///:memory:', echo=False)
    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        yield session
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)

def test_root(client):
    response = client.get("/health-chelk")
    assert response.status_code == 200
    assert response.json() == {"message": "OK"}

def test_upload_file(client, db):
    # Mock the Celery task
    with patch('src.tasks.process_csv.process_csv_file.delay') as mock_task:
        mock_task.return_value.id = 'test_task_id'

        csv_content = "column1,column2,column3\nvalue1,value2,value3"
        response = client.post(
            "/upload-csv/",
            files={"file": ("test.csv", csv_content.encode(), "text/csv")}
        )

        assert response.status_code == 200
        assert response.json() == {
            "message": "File received and processing started",
            "task_id": "test_task_id"
        }

        # Verify that the Celery task was called
        mock_task.assert_called_once()

def test_process_event(db):
    from src.tasks.process_csv import user_created_event

    events = [{"user_id": i, "event_timestamp": datetime.now()} for i in range(1,4)]
    user_created_event(db=db, users=events)

    # Verify that the data was saved to the database
    csv_data = db.query(UserEvent).all()
    assert len(csv_data) == 3
    assert events[0]["user_id"] == 1
    assert events[1]["user_id"] == 2 
    assert events[2]["user_id"] == 3 


def test_process_user_address(db):
     from src.tasks.process_csv import process_csv_chunk

     # Mock the Celery task
     with patch('src.tasks.process_csv.user_created_event.delay') as mock_task:
         mock_task.return_value.id = 'test_task_id'

         rows = [{
             "user_id": i,
             "name": f"name-{i}",
             "email": f"name{i}@test.com",
             "created_at": datetime.now().strftime(format='%Y-%m-%dT%H:%M:%S'),
             "address_id": i,
             "street": f"rua-{i}",
             "city": f"cidade-{i}",
             "state": f"state-{i}",
             "zipcode": f"cep-{i}",
             "country": f"pais-{i}",
             } for i in range(1,4)]

         process_csv_chunk(db=db, chunk=rows)

        # Verify that the data was saved to the database
         users = db.query(User).all()
         assert len(users) == 3
         assert users[0].user_id == '1'
         assert users[1].user_id == '2'
         assert users[2].user_id == '3'

         # Verify that the Celery task was called
         mock_task.assert_called_once()

