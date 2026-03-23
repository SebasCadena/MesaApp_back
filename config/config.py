import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker

load_dotenv(override=True)

DATABASE_URL = os.getenv("DB_URL")

if not DATABASE_URL:
    raise ValueError("La variable DB_URL no esta definida en .env")

if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


@event.listens_for(engine, "connect")
def _set_search_path(dbapi_connection, connection_record):
    # Neon pooler may not preserve a default schema; enforce public per connection.
    with dbapi_connection.cursor() as cursor:
        cursor.execute("SET search_path TO public")


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()