from django.urls import path
from . import views

app_name = 'transport'

urlpatterns = [
    path('', views.nearby_transport, name='nearby_transport'),
    path('route/', views.route_page, name='route_page'),
]
