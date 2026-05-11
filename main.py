import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
METALS_API_KEY = os.getenv("METALS_API_KEY")

API_URL = "https://api.metals.dev/v1/latest"


def get_gold_price():
    params = {
        "api_key": METALS_API_KEY,
        "currency": "SGD",
        "unit": "g"
    }

    response = requests.get(API_URL, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()

    if data.get("status") != "success":
        raise Exception(f"API error: {data}")

    price = data["metals"]["gold"]
    return round(float(price), 2)


def ai_analysis(price):
    if price >= 150:
        return "🚀 金價高位，短期市場偏強，但追高風險也比較大。"
    elif price >= 140:
        return "📈 金價偏強，可以等回調再買，適合分批觀察。"
    elif price >= 130:
        return "⚖️ 金價正常區間，長期儲金可以小量分批。"
    else:
        return "📉 金價偏低，可以留意買入機會。"


def send_telegram(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        raise Exception("Missing Telegram secrets")

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    response = requests.post(url, data=payload, timeout=30)
    response.raise_for_status()


def main():
    if not METALS_API_KEY:
        raise Exception("Missing METALS_API_KEY")

    sg_time = datetime.now(
        ZoneInfo("Asia/Singapore")
    ).strftime("%Y-%m-%d %H:%M:%S")

    price = get_gold_price()
    analysis = ai_analysis(price)

    message = f"""🪙 Gold Price Alert

Gold Spot Price:
SGD {price}/gram

AI Analysis:
{analysis}

⏰ Singapore Time:
{sg_time}
"""

    send_telegram(message)


if __name__ == "__main__":
    main()
