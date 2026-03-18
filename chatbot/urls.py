from django.urls import path
from . import views

urlpatterns = [
    path("ask/", views.chatbot_reply, name="chatbot_reply"),
    path("test/", views.test_chatbot, name="test_chatbot"), 
]