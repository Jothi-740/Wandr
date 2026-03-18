from django.urls import path
from . import views
from Account import views as account_views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', account_views.login_view, name='login'),
    path('signup/', account_views.signup_view, name='signup'),
    path('home/', views.home, name='home'),
    path('nearby/', views.nearby, name='nearby'),
    path('route/', views.route, name='route'),
    path('feedback/', views.feedback, name='feedback'),
    path('support/', views.support, name='support'),
]
