from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Transaction
from .services.pricing import get_price_per_gram_inr
from django.core.paginator import Paginator
from django.utils.dateparse import parse_date

@login_required
def buy_page(request):
    
    price, meta = get_price_per_gram_inr()
    ctx = {
        "price_per_gram_inr": round(price, 2),
        "as_of": meta.get("timestamp"),  # can be None
        # keep meta only in server memory for this render; we don't expose authority in the template
    }
    return render(request, "payments/buy.html", ctx)


@login_required
@require_POST
@csrf_protect
def mock_charge(request):
   
    amt_str = (request.POST.get("amount") or "").strip()
    try:
        amount = float(amt_str)
    except Exception:
        return render(request, "payments/buy.html", {
            "error": "Invalid amount.",
            **_price_ctx()
        }, status=400)

    if amount < 10:
        return render(request, "payments/buy.html", {
            "error": "Minimum amount is ₹10.",
            **_price_ctx()
        }, status=400)

    price, meta = get_price_per_gram_inr()
    grams = round(amount / price, 4) if price > 0 else 0.0
    ts = meta.get("timestamp")

    tx = Transaction.objects.create(
        user=request.user,
        amount_inr=amount,
        grams=grams,
        price_per_gram_inr=round(price, 2),
        price_authority=meta.get("authority", "mcx"),  # stored for audit; not shown on frontend
        price_currency=meta.get("currency", "INR"),
        price_unit=meta.get("unit", "g"),
        price_timestamp=ts if ts else None,
        status="SUCCESS",
    )

    return redirect("buy_success", tx_id=tx.id)


@login_required
def buy_success(request, tx_id: int):
    """
    Simple receipt page for the mock transaction.
    """
    tx = get_object_or_404(Transaction, id=tx_id, user=request.user)
    return render(request, "payments/success.html", {"tx": tx})


def _price_ctx():
    price, meta = get_price_per_gram_inr()
    return {
        "price_per_gram_inr": round(price, 2),
        "as_of": meta.get("timestamp"),
    }



@login_required
def history(request):
    """
    List current user's transactions with simple pagination and optional date filters.
    """
    qs = Transaction.objects.filter(user=request.user).order_by("-created_at")

    # Optional filters (?from=YYYY-MM-DD&to=YYYY-MM-DD)
    date_from = request.GET.get("from")
    date_to = request.GET.get("to")
    if date_from:
        df = parse_date(date_from)
        if df:
            qs = qs.filter(created_at__date__gte=df)
    if date_to:
        dt = parse_date(date_to)
        if dt:
            qs = qs.filter(created_at__date__lte=dt)

    paginator = Paginator(qs, 10)  # 10 rows per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "payments/history.html", {
        "page_obj": page_obj,
        "date_from": date_from or "",
        "date_to": date_to or "",
    })
