import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone, timedelta

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ.get("CHAT_ID", "@Gram_Price_Today")
IQD_FALLBACK_RATE = 1310
BAGHDAD = timezone(timedelta(hours=3))


def get_json(url, data=None):
    req = urllib.request.Request(
        url,
        data=data,
        headers={"User-Agent": "TON-Price-Bot/1.0"}
    )
    with urllib.request.urlopen(req, timeout=25) as response:
        return json.loads(response.read().decode("utf-8"))


def get_ton_price():
    # Binance spot price first; CoinGecko is a fallback.
    try:
        result = get_json(
            "https://api.binance.com/api/v3/ticker/price?symbol=TONUSDT"
        )
        price = float(result["price"])
        if price > 0:
            return price
    except Exception as exc:
        print(f"Binance price lookup failed: {exc}")

    result = get_json(
        "https://api.coingecko.com/api/v3/simple/price"
        "?ids=the-open-network&vs_currencies=usd"
    )
    price = float(result["the-open-network"]["usd"])
    if price <= 0:
        raise RuntimeError("The TON price returned an invalid value")
    return price


def get_iqd_rate():
    try:
        result = get_json("https://open.er-api.com/v6/latest/USD")
        if result.get("result") == "success":
            rate = float(result["rates"]["IQD"])
            if rate > 0:
                return rate, "سعر صرف مباشر"
    except Exception as exc:
        print(f"IQD rate lookup failed; using fallback: {exc}")
    return float(IQD_FALLBACK_RATE), "سعر صرف تقريبي احتياطي"


def get_24h_change():
    try:
        result = get_json(
            "https://api.binance.com/api/v3/ticker/24hr?symbol=TONUSDT"
        )
        return float(result["priceChangePercent"])
    except Exception as exc:
        print(f"24h change lookup failed: {exc}")
        return None


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = urllib.parse.urlencode({
        "chat_id": CHAT_ID,
        "text": message,
        "disable_web_page_preview": "true",
    }).encode("utf-8")
    result = get_json(url, data=payload)
    if not result.get("ok"):
        raise RuntimeError(f"Telegram API returned an error: {result}")
    print(f"Telegram message sent. Message ID: {result['result']['message_id']}")


def main():
    price = get_ton_price()
    iqd_rate, rate_note = get_iqd_rate()
    change = get_24h_change()
    now = datetime.now(BAGHDAD).strftime("%Y-%m-%d | %I:%M %p")

    change_text = (
        f"{change:+.2f}%"
        if change is not None else "غير متاح حالياً"
    )

    message = (
        "💎 TON | تحديث السعر\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"💵 السعر بالدولار: ${price:.4f}\n"
        f"🇮🇶 السعر بالدينار: {price * iqd_rate:,.0f} د.ع\n"
        f"📊 التغير خلال 24 ساعة: {change_text}\n"
        f"💱 ملاحظة الصرف: {rate_note}\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"🕒 آخر تحديث: {now}\n"
        "📡 المصدر: Binance / CoinGecko\n"
        "⚠️ الأسعار تقريبية وقد تتغير بسرعة."
    )
    send_telegram_message(message)


if __name__ == "__main__":
    main()
