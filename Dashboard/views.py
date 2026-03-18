from django.shortcuts import render

def index(request):
    return render(request, "landing.html")

def login_view(request):
    return render(request, "login.html")

def signup(request):
    return render(request, "signup.html")

def home(request):
    return render(request, "home.html")

def nearby(request):
    return render(request, "nearby.html")

def route(request):
    return render(request, "route.html")

def feedback(request):
    return render(request, "feedback.html")

def support(request):
    return render(request, "support.html")

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_settings(request):
    return render(request, "admin/settings.html")

@staff_member_required
def admin_chatbot(request):
    return render(request, "admin/chatbot.html")

@staff_member_required
def admin_feedbacks(request):
    return render(request, "admin/feedbacks.html")