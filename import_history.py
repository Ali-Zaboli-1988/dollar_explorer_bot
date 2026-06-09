# import_history.py
import json
from datetime import datetime
from database import SessionLocal
from models import DollarRate

def import_dollar_history(json_path: str = "prices.json"):
    db = SessionLocal()
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    records = data["USD"]
    count = 0
    for rec in records:
        # فقط داده‌هایی که منبعشان "Navasan" یا "manual" است را وارد می‌کنیم
        # تبدیل datetime_miladi به شیء datetime
        try:
            dt_miladi = datetime.strptime(rec["datetime_miladi"], "%Y-%m-%d %H:%M")
        except:
            print(f"Invalid date format: {rec['datetime_miladi']}")
            continue
        
        # بررسی نکنیم تکراری نباشد
        existing = db.query(DollarRate).filter(DollarRate.date == dt_miladi).first()
        if not existing:
            new_rate = DollarRate(
                date=dt_miladi,
                rate=rec["price"],
                change=None,   # در JSON ما change نداریم
                timestamp=int(dt_miladi.timestamp())
            )
            db.add(new_rate)
            count += 1
    
    db.commit()
    db.close()
    print(f"Imported {count} historical dollar rates.")

if __name__ == "__main__":
    import_dollar_history()
