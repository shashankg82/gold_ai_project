from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .models import ChatLog
from .services.classifier import is_gold_related
from .services.llm import get_answer   # unified answer function


@login_required
def chat_page(request):
    """Render the chat page with last 10 chats"""
    recent = ChatLog.objects.filter(user=request.user)[:10]
    return render(request, "chat/chat.html", {"recent": recent})


@login_required
@require_POST
def chat_ask(request):
    """Handle a new chat query via AJAX"""
    question = (request.POST.get("question") or "").strip()

    if not question:
        return JsonResponse(
            {"ok": False, "error": "Please enter a question."}, status=400
        )

    # Step 1: classify (gold-related or not)
    related = is_gold_related(question)

    # Step 2: get answer (either LLM or refusal message)
    answer, model_used = get_answer(question, related)

    # Step 3: log interaction
    log = ChatLog.objects.create(
        user=request.user,
        question=question,
        answer=answer,
        is_gold_related=related,
        model_used=model_used,
    )

    # Step 4: return JSON for frontend
    return JsonResponse({
        "ok": True,
        "is_gold_related": related,
        "answer": answer,
        "offer_purchase": related,  # Only offer Buy option if gold-related
        "log_id": log.id,
    })
