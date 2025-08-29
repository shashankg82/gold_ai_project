from django.urls import path
from . import views

urlpatterns = [
    path("", views.chat_page, name="chat_page"),
    path("ask/", views.chat_ask, name="chat_ask"),
]