# payments/services/pricing.py
import requests
from datetime import datetime, timezone
from django.conf import settings

def get_price_per_gram_inr():
    
    authority = "mcx"
    currency = "INR"
    unit = "g"
    ts_dt = None

    key = getattr(settings, "GOLD_PRICE_API_KEY", "") or ""
    provider = (getattr(settings, "GOLD_PRICE_PROVIDER", "metalsdev") or "").lower()

    if provider == "metalsdev" and key:
        try:
            url = "https://api.metals.dev/v1/metal/authority"
            params = {"api_key": key, "authority": authority, "currency": currency, "unit": unit}
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            rates = data.get("rates") or {}
            price = float(rates.get("mcx_gold", 0.0))

            ts_str = data.get("timestamp")
            if ts_str:
                try:
                    ts_dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00")).astimezone(timezone.utc)
                except Exception:
                    ts_dt = None

            if price > 0:
                return price, {"authority": authority, "currency": currency, "unit": unit, "timestamp": ts_dt}
        except Exception as e:
            print("[Metals.dev] Error:", e)

    # Fallback
    fallback = float(getattr(settings, "GOLD_PRICE_FALLBACK", 9500.0))
    return fallback, {"authority": authority, "currency": currency, "unit": unit, "timestamp": ts_dt}
