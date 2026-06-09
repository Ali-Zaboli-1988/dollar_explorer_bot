# config.py
import os
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی از فایل .env (برای لوکال)
load_dotenv()

# ---------- تنظیمات ربات تلگرام ----------
BOT_TOKEN = os.getenv("BOT_TOKEN", "8739194909:AAE_iJymQHYFs9yMDykrSQjiv1XWfSkXgNI")
BOT_USERNAME = "dollar_explorer_bot"
WEBHOOK_DOMAIN = os.getenv("WEBHOOK_DOMAIN", "https://your-app.onrender.com")
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_DOMAIN}{WEBHOOK_PATH}"

# ---------- تنظیمات API نوسان ----------
NAVASAN_API_KEY = os.getenv("NAVASAN_API_KEY", "freeFGpzjUacmoTt3fn9ZgAeigqwAWmW")
NAVASAN_BASE_URL = "http://api.navasan.tech/latest/"

# ---------- لیست منابع RSS (۳۱ منبع) ----------
RSS_FEEDS = [
    # خبرگزاری مهر
    {"url": "https://www.mehrnews.com/rss/tp/763", "category": "social"},
    {"url": "https://www.mehrnews.com/rss/tp/473", "category": "economic"},
    {"url": "https://www.mehrnews.com/rss/tp/122", "category": "social"},
    {"url": "https://www.mehrnews.com/rss", "category": "general"},
    
    # همشهری آنلاین
    {"url": "https://www.hamshahrionline.ir/rss/tp/55", "category": "social"},
    {"url": "https://www.hamshahrionline.ir/rss/tp/207?tp=207", "category": "economic"},
    {"url": "https://www.hamshahrionline.ir/rss", "category": "general"},
    
    # فردای اقتصاد
    {"url": "https://www.fardayeeghtesad.com/rss/tp/61", "category": "social"},
    {"url": "https://www.fardayeeghtesad.com/rss/tp/20", "category": "economic"},
    
    # اقتصاد ۲۴
    {"url": "https://eghtesaad24.ir/fa/rss/allnews", "category": "general"},
    {"url": "https://eghtesaad24.ir/fa/rss/2", "category": "economic"},
    {"url": "https://eghtesaad24.ir/fa/rss/6", "category": "economic"},
    
    # اقتصاد آنلاین
    {"url": "https://www.eghtesadonline.com/rss", "category": "economic"},
    
    # اقتصاد ایران
    {"url": "https://iraneconomist.com/fa/rss/allnews", "category": "general"},
    {"url": "https://iraneconomist.com/fa/rss/1", "category": "general"},
    {"url": "https://iraneconomist.com/fa/rss/3", "category": "economic"},
    
    # خبر آنلاین
    {"url": "https://www.khabaronline.ir/rss", "category": "general"},
    
    # انتخاب
    {"url": "https://entekhab.ir/fa/rss/1", "category": "general"},
    {"url": "https://entekhab.ir/fa/rss/allnews", "category": "general"},
    
    # ایبنا
    {"url": "https://www.ibna.ir/rss/tp/10?tp=10", "category": "political"},
    
    # اطلاعات
    {"url": "https://www.ettelaat.com/rss/tp/5", "category": "economic"},
    {"url": "https://www.ettelaat.com/rss/tp/4", "category": "social"},
    
    # ایرنا
    {"url": "https://www.irna.ir/rss", "category": "general"},
    
    # ایسنا
    {"url": "https://www.isna.ir/rss", "category": "general"},
    
    # ابنا
    {"url": "https://fa.abna24.com/rss/tp/1021", "category": "social"},
    
    # یورونیوز فارسی
    {"url": "https://parsi.euronews.com/rss", "category": "political"},
    
    # خبرگزاری پانا
    {"url": "https://pana.ir/rss", "category": "general"},
    
    # بلاگ پایتون (منبع انگلیسی)
    {"url": "https://blog.python.org/rss", "category": "tech", "lang": "en"},
    
    # خبرورزشی
    {"url": "https://www.khabarvarzeshi.com/rss", "category": "sport"},
    
    # TechCrunch (انگلیسی)
    {"url": "https://techcrunch.com/feed", "category": "tech", "lang": "en"},
    
    # Lifehacker (انگلیسی)
    {"url": "https://lifehacker.com/rss", "category": "tech", "lang": "en"},
]

# ---------- تنظیمات دیتابیس ----------
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/dollar_db")

# ---------- تنظیمات مدل پیش‌بینی ----------
PREDICTION_LAGS = [1, 2, 3, 7]  # روزهای گذشته برای ویژگی‌ها
FORECAST_DAYS = [1, 7, 30]      # پیش‌بینی فردا، هفته بعد، ماه بعد

# ---------- تنظیمات کرون جاب ----------
CRON_SCHEDULE = "0 8 * * *"     # هر روز ساعت ۸ صبح (Tehran Time)
TIMEZONE = "Asia/Tehran"

# ---------- تنظیمات Uptime ----------
HEALTH_CHECK_PATH = "/health"
