# sentiment.py
from textblob import TextBlob
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import re

# بارگذاری مدل فارسی (یک بار در زمان اجرا)
try:
    fa_tokenizer = AutoTokenizer.from_pretrained("HooshvareLab/bert-fa-sentiment")
    fa_model = AutoModelForSequenceClassification.from_pretrained("HooshvareLab/bert-fa-sentiment")
    FA_MODEL_LOADED = True
except Exception as e:
    print(f"Failed to load Persian sentiment model: {e}")
    FA_MODEL_LOADED = False

def normalize_persian_text(text: str) -> str:
    """نرمال‌سازی ساده متن فارسی"""
    text = re.sub(r'[^\w\s\u0600-\u06FF]', ' ', text)  # حذف علائم نگارشی غیرفارسی
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def analyze_sentiment_fa(text: str) -> float:
    """
    تحلیل احساسات متن فارسی با مدل BERT
    خروجی: عددی بین -1 (منفی) تا +1 (مثبت)
    """
    if not FA_MODEL_LOADED or not text:
        return 0.0
    
    try:
        text = normalize_persian_text(text[:512])  # محدودیت طول
        inputs = fa_tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            outputs = fa_model(**inputs)
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=1).numpy()[0]
        # معمولاً مدل سه کلاس دارد: منفی، خنثی، مثبت
        # امتیاز نهایی: -1 * prob(negative) + 0 * prob(neutral) + 1 * prob(positive)
        if len(probabilities) >= 3:
            sentiment_score = -1 * probabilities[0] + probabilities[2]  # فرض: [neg, neu, pos]
        else:
            sentiment_score = (probabilities[1] - probabilities[0]) if len(probabilities)==2 else 0.0
        return float(sentiment_score)
    except Exception as e:
        print(f"Sentiment analysis error: {e}")
        return 0.0

def analyze_sentiment_en(text: str) -> float:
    """
    تحلیل احساسات متن انگلیسی با TextBlob
    خروجی: -1 تا +1
    """
    try:
        blob = TextBlob(text)
        return blob.sentiment.polarity
    except:
        return 0.0

def analyze_sentiment(text: str, lang: str = "fa") -> float:
    """تابع اصلی تحلیل احساسات بر اساس زبان"""
    if lang == "fa":
        return analyze_sentiment_fa(text)
    else:
        return analyze_sentiment_en(text)
