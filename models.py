# models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Index
from sqlalchemy.sql import func
from database import Base

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    summary = Column(Text, nullable=True)          # خلاصه خبر
    source = Column(String(200), nullable=False)   # نام منبع
    url = Column(String(500), unique=True, nullable=False)  # لینک یکتا برای جلوگیری از تکراری
    category = Column(String(50), nullable=False)  # economic, social, political, general, tech
    lang = Column(String(10), default="fa")        # fa یا en
    sentiment_score = Column(Float, nullable=True) # امتیاز -1 تا +1
    published_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # ایندکس برای جستجوی سریع بر اساس تاریخ و دسته
    __table_args__ = (
        Index('idx_news_published_category', 'published_at', 'category'),
    )

class DollarRate(Base):
    __tablename__ = "dollar_rates"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, unique=True, nullable=False, index=True)  # هر روز فقط یک رکورد
    rate = Column(Float, nullable=False)          # نرخ دلار به تومان
    change = Column(Integer, nullable=True)       # تغییر نسبت به روز قبل (مثلاً -25)
    timestamp = Column(Integer, nullable=True)    # یونیکس تایم از API
    created_at = Column(DateTime, server_default=func.now())

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    prediction_date = Column(DateTime, nullable=False, index=True)  # روزی که پیش‌بینی برای آن است
    days_ahead = Column(Integer, nullable=False)   # 1, 7, یا 30
    predicted_rate = Column(Float, nullable=False)
    lower_bound = Column(Float, nullable=True)     # بازه اطمینان پایین
    upper_bound = Column(Float, nullable=True)     # بازه اطمینان بالا
    created_at = Column(DateTime, server_default=func.now())
