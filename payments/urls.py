from django.urls import path
from . import views


urlpatterns = [
    path("buy/", views.buy_page, name="buy_page"),
    path("mock/charge/", views.mock_charge, name="mock_charge"),
    path("success/<int:tx_id>/", views.buy_success, name="buy_success"),
    path("history/", views.history, name="tx_history"),
]