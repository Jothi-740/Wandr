from django.urls import path
from . import views

app_name = 'emergency'

urlpatterns = [
    path('', views.emergency_dashboard, name='dashboard'),
    path("nearby-hospitals/", views.nearby_hospitals, name="nearby_hospitals"),
    path("nearby-police/", views.nearby_police, name="nearby_police"),
    path("nearby-fire/", views.nearby_fire, name="nearby_fire"),
    path("nearby-mechanic/", views.nearby_mechanic, name="nearby_mechanic"),
    path("hospital-route/", views.hospital_route, name="hospital_route"),
]
