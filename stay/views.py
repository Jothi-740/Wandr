from django.shortcuts import render

def stay(request):
    return render(request,'stay/stay.html')
# Create your views here.

def route(request):
    return render(request, "stay/route.html")