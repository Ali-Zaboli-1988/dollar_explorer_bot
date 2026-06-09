# dollar_fetcher.py
import requests
import json
from datetime import datetime
from sqlalchemy.orm import Session
from models import DollarRate
from config import NAVASAN_API_KEY, NAVASAN_BASE_URL
from database import SessionLocal

def fetch_current_dollar_rate() -> dict | None:
    """
    دریافت نرخ فعلی دلار از API نوسان
    خروجی: {'rate': float, 'change': int, 'timestamp': int, 'date': str}
    """
    url = f"{NAVASAN_BASE_URL}?api_key={NAVASAN_API_KEY}&item=USD"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # ساختار پاسخ نوسان: {'usd': {'value': '...', 'change': ..., 'timestamp': ..., 'date': ...}}
        usd_data = data.get("usd")
        if not usd_data:
            print("USD data not found in response")
            return None
        
        return {
            "rate": float(usd_data["value"]),
            "change": usd_data.get("change"),
            "timestamp": usd_data.get("timestamp"),
            "date": usd_data.get("date")  # فرمت: "1404-03-13 05:58"
        }
    except Exception as e:
        print(f"Error fetching dollar rate: {e}")
        return None

def save_dollar_rate(db: Session, rate_info: dict) -> bool:
    """ذخیره نرخ دلار در دیتابیس (تنها یک رکورد به ازای هر روز)"""
    try:
        # تبدیل تاریخ شمسی به میلادی برای ذخیره در دیتابیس
        date_str = rate_info["date"].split()[0]  -> "1404-03-13"
        # برای سادگی فعلاً همان تاریخ شمسی را به عنوان datetime ذخیره می‌کنیم
        # (بعداً در صورت نیاز تبدیل دقیق انجام می‌شود)
        from datetime import datetime as dt
        published_at = dt.strptime(rate_info["date"], "%Y-%m-%d %H:%M")
        
        # بررسی وجود رکورد برای همین روز
        existing = db.query(DollarRate).filter(DollarRate.date == published_at).first()
        if existing:
            # به‌روزرسانی نرخ (اگر API نرخ جدیدتر بدهد)
            existing.rate = rate_info["rate"]
            existing.change = rate_info["change"]
            existing.timestamp = rate_info["timestamp"]
        else:
            new_rate = DollarRate(
                date=published_at,
                rate=rate_info["rate"],
                change=rate_info["change"],
                timestamp=rate_info["timestamp"]
            )
            db.add(new_rate)
        db.commit()
        return True
    except Exception as e:
        print(f"Error saving dollar rate: {e}")
        db.rollback()
        return False

def update_dollar_rate():
    """تابع اصلی که از کرون جاب فراخوانی می‌شود: نرخ فعلی را می‌گیرد و ذخیره می‌کند"""
    db = SessionLocal()
    rate_info = fetch_current_dollar_rate()
    if rate_info:
        save_dollar_rate(db, rate_info)
        print(f"Dollar rate updated: {rate_info['rate']} at {rate_info['date']}")
    else:
        print("Failed to fetch dollar rate")
    db.close()
