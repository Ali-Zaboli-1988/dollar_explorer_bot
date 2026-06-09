# news_fetcher.py
import feedparser
import hashlib
from datetime import datetime
from sqlalchemy.orm import Session
from models import News
from sentiment import analyze_sentiment
from config import RSS_FEEDS

def fetch_news_from_feed(feed_url: str, category: str, lang: str = "fa"):
    """
    دریافت اخبار از یک RSS فید
    بازگشت: لیستی از دیکشنری‌های خبر
    """
    articles = []
    try:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:20]:  # حداکثر ۲۰ خبر از هر فید
            title = entry.get("title", "").strip()
            summary = entry.get("summary", entry.get("description", "")).strip()
            link = entry.get("link", "")
            published = entry.get("published_parsed")
            if published:
                pub_date = datetime.fromtimestamp(datetime.timestamp(datetime(*published[:6])))
            else:
                pub_date = datetime.now()
            
            if not title and not summary:
                continue
            
            # یک شناسه یکتا بر اساس لینک یا ترکیب عنوان
            unique_id = hashlib.md5(link.encode()).hexdigest() if link else hashlib.md5(title.encode()).hexdigest()
            
            articles.append({
                "title": title,
                "summary": summary[:1000],
                "source": feed_url,
                "url": link,
                "category": category,
                "lang": lang,
                "published_at": pub_date,
                "unique_id": unique_id
            })
    except Exception as e:
        print(f"Error fetching {feed_url}: {e}")
    return articles

def fetch_all_news(db: Session):
    """
    دریافت تمام اخبار از همه منابع RSS (۳۱ منبع)
    ذخیره در دیتابیس پس از تحلیل احساسات
    """
    all_articles = []
    for feed in RSS_FEEDS:
        url = feed["url"]
        category = feed.get("category", "general")
        lang = feed.get("lang", "fa")
        
        # فقط دسته‌های اقتصادی، اجتماعی، سیاسی را نگه دار
        if category not in ["economic", "social", "political"]:
            continue
        
        articles = fetch_news_from_feed(url, category, lang)
        all_articles.extend(articles)
        print(f"Fetched {len(articles)} from {url}")
    
    # تحلیل احساسات و ذخیره در دیتابیس
    saved_count = 0
    for art in all_articles:
        # بررسی تکراری نبودن
        existing = db.query(News).filter(News.url == art["url"]).first()
        if existing:
            continue
        
        # متن کامل برای تحلیل: عنوان + خلاصه
        full_text = art["title"] + " " + art["summary"]
        sentiment_score = analyze_sentiment(full_text, art["lang"])
        
        news_item = News(
            title=art["title"],
            summary=art["summary"],
            source=art["source"],
            url=art["url"],
            category=art["category"],
            lang=art["lang"],
            sentiment_score=sentiment_score,
            published_at=art["published_at"]
        )
        db.add(news_item)
        saved_count += 1
    
    db.commit()
    print(f"Saved {saved_count} new news items with sentiment scores.")
    return saved_count

# تابعی که توسط کرون جاب روزانه فراخوانی می‌شود
def update_news():
    from database import SessionLocal
    db = SessionLocal()
    try:
        fetch_all_news(db)
    finally:
        db.close()
