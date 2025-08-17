from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = "mysql+pymysql://Harshad:Harshad@localhost/groccery"  # Replace with your real password

engine = create_engine(DB_URL)
# SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)


Base = declarative_base()

# ✅ THIS FUNCTION IS REQUIRED
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
