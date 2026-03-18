from django.urls import path
from . import views

app_name = 'food'

urlpatterns = [
    path('', views.nearby_food, name='nearby_food'),
    path('route/', views.route_page, name='route_page'),
]
