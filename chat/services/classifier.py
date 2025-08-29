import os
import requests

# Fast path: cheap keyword check
_GOLD_KEYWORDS = {
    "gold", "digital gold", "24k", "24 karat", "hallmark", "sovereign gold bond",
    "sgb", "gold etf", "etf gold", "mmtc", "pamp", "safegold", "buy gold",
    "sell gold", "gold price", "redeem gold", "grams", "gram"
}

def _keyword_hit(text: str) -> bool:
    if not text:
        return False
    t = text.lower()
    if "gold" in t:
        return True
    return any(k in t for k in _GOLD_KEYWORDS)


_HF_ZS_MODEL = os.environ.get("HF_ZS_MODEL", "facebook/bart-large-mnli")
_HF_API_TOKEN = "Please Enter Your Hugging Face Token Here"  # Please refer Setup.md in repository

def _zero_shot_gold_relevance(text: str, threshold: float = 0.7) -> bool:
    """
    Classify if text is about (digital) gold investment using zero-shot labels.
    Returns True if 'gold_investment' score >= threshold.
    """
    if not _HF_API_TOKEN:
        return False

    url = f"https://api-inference.huggingface.co/models/{_HF_ZS_MODEL}"
    headers = {"Authorization": f"Bearer {_HF_API_TOKEN}"}
    payload = {
        "inputs": text,
        "parameters": {
            "candidate_labels": ["gold_investment", "not_about_gold"],
            "multi_label": False
        }
    }
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=12)
        resp.raise_for_status()
        data = resp.json()
        labels = data.get("labels") or []
        scores = data.get("scores") or []
        for lbl, sc in zip(labels, scores):
            if lbl == "gold_investment":
                return sc >= threshold
        return False
    except Exception:
        return False

def is_gold_related(text: str) -> bool:
    if _keyword_hit(text):
        return True
    return _zero_shot_gold_relevance(text)
