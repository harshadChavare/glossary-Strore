from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DB_URL = "mysql+pymysql://Harshad:Harshad@localhost/groccery"  # mysql
# database.py

# postgres
# DB_URL = "postgresql://postgres:123@localhost:5432/groccery"  # Change this line
DB_URL="postgresql://postgres:LeBGGFcDbWgSEMBAKgOUjIABxJyzncQU@shortline.proxy.rlwy.net:51896/railway"

# DATABASE_URL = "postgresql://postgres:123@localhost:5432/dbname"


# Example:
# DB_URL = "postgresql://Harshad:Harshad@localhost:5432/groccery"


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
