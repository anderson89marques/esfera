from io import StringIO
import functools
import csv
from celery import Celery
from celery.utils.log import get_task_logger
from src.core.database import SessionLocal
from src.models.user import User
from src.models.address import Address
from src.models.user_event import UserEvent
from src.core.config import settings
from datetime import datetime
from sqlalchemy.orm import Session

logger = get_task_logger(__name__)
celery_app = Celery('tasks', broker=settings.REDIS_URL)

def db_session_decorator():
    """
    This decorator give us flexibility to test and run the tasks 
    selecting for example a test database session instead of a real one.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            db: Session = None
            try:
                if not kwargs.get('db'):
                    db = SessionLocal()
                    kwargs['db'] = db 
                print("db", kwargs.get('db'))
                value = func(*args, **kwargs)
                return value
            except Exception as e:
                logger.debug("db rollback")
                db.rollback()
                logger.exception(e)
            finally:
                logger.debug("db_session closed")
                db.close()

        return wrapper
    return decorator

@celery_app.task
@db_session_decorator()
def process_csv_chunk(db: Session, chunk: list):
    logger.info("Processing files chunks")
    try:
        users = []
        addresses = []
        for row in chunk:
            user = User(
                user_id=row['user_id'],
                name=row['name'],
                email=row['email'],  # Generate an email
                created_at=datetime.strptime(row['created_at'], '%Y-%m-%dT%H:%M:%S'),
            )
            address = Address(
                address_id=row['address_id'],
                 street=row['street'],
                 city=row['city'],
                 state=row['state'],
                 zipcode=row['zipcode'],
                 country=row['country'],
                 user=user
            )
            users.append(user)
            addresses.append(address)
        db.add_all(users)
        db.add_all(addresses)
        db.commit()

        # Raise UserCreated event
        user_created_event.delay(users=[{"user_id": user.user_id, "event_timestamp": user.created_at} for user in users])
    except Exception as e:
        logger.error("Erro1r %s", e)

@celery_app.task
@db_session_decorator()
def process_csv_file(content: str, **kwargs):
    logger.info("Processing file...")
    try:
        csv_content = content.decode('utf-8')
        csv_file = StringIO(csv_content)
        csv_reader = csv.DictReader(csv_file)
        chunk = []
        for i, row in enumerate(csv_reader, 1):
            chunk.append(row)
            if i % 400 == 0:
                process_csv_chunk.delay(chunk=chunk)
                chunk = []
    
        if chunk:
            process_csv_chunk.delay(chunk=chunk)
    except Exception as e:
        logger.error("Error process file: %s", e)

@celery_app.task
@db_session_decorator()
def user_created_event(db: Session, users: list):
    logger.info("Processing Events...")
    try:
        db.bulk_insert_mappings(UserEvent, users)
        db.commit()
        logger.info("Total users created %d" % len(users))
    except Exception as e:
        logger.error("Error event: ", e)

