import os
import requests


OPENROUTER_API_KEY = "Enter Your Open Router API key here." # Please go through Setup.md in repository
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


OPENROUTER_MODEL = os.environ.get("OPENROUTER_MODEL", "mistralai/mistral-7b-instruct:free")


def openrouter_generate_answer(question: str) -> tuple[str, str]:
    """
    Call OpenRouter to generate an answer for gold-related questions.
    Returns (answer, model_used).
    """
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",

        "HTTP-Referer": "http://localhost:8000",  
        "X-Title": "Gold AI Demo",
        "Content-Type": "application/json",
    }

    
    messages = [
        {
            "role": "system",
            "content": (
                "You are a gold-investment Q&A assistant. "
                "Only answer questions related to physical gold, digital gold, SGBs, gold ETFs, pricing mechanics, pros/cons, taxation basics, risks, and diversification. "
                "Be factual, concise, and add a short educational-not-financial-advice disclaimer. "
                "Do NOT fabricate live prices; if price is requested and unavailable, say so."
            ),
        },
        {"role": "user", "content": question},
    ]

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": messages,
        "max_tokens": 300,
        "temperature": 0.3,
    }

    try:
        resp = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=45)

        resp.raise_for_status()
        data = resp.json()

        choices = data.get("choices") or []
        if not choices or "message" not in choices[0] or "content" not in choices[0]["message"]:
            return "Sorry, I couldn’t generate an answer right now.", OPENROUTER_MODEL

        answer = choices[0]["message"]["content"]
        return answer, OPENROUTER_MODEL

    except requests.HTTPError as e:
        try:
            err_json = resp.json()
        except Exception:
            err_json = {"error": str(e)}
        print("[OpenRouter HTTPError]", resp.status_code, err_json)
        return "Sorry, something went wrong while contacting the model.", OPENROUTER_MODEL

    except Exception as e:
        print("[OpenRouter Exception]", str(e))
        return "Sorry, something went wrong while contacting the model.", OPENROUTER_MODEL


def get_answer(question: str, gold_related: bool) -> tuple[str, str]:
    if gold_related:
        return openrouter_generate_answer(question)
    else:
        return "Sorry, I am only trained to answer gold investment questions.", "policy"
