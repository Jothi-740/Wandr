from django.urls import path
from . import views

urlpatterns = [
    path('',views.stay,name="stay"),
    path('route/', views.route, name="stay_route"),
]