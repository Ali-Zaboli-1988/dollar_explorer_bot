# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

# ساخت موتور اتصال به دیتابیس
engine = create_engine(DATABASE_URL)

# جلسه برای ارتباط با دیتابیس
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# کلاس پایه برای مدل‌ها
Base = declarative_base()

# تابع برای گرفتن جلسه دیتابیس (در endpoints استفاده می‌شه)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
