from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('', views.account_dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('plans/', views.plans_view, name='plans'),
    path('settings/', views.settings_view, name='settings'),
    path('add-memory/', views.add_memory, name='add_memory'),
    path('delete-memory/<int:memory_id>/', views.delete_memory, name='delete_memory'),
    path('delete-plan/<int:plan_id>/', views.delete_plan, name='delete_plan'),
    path('add-day/<int:plan_id>/', views.add_day, name='add_day'),
    path('delete-day/<int:day_id>/', views.delete_day, name='delete_day'),
    path('edit-day/<int:day_id>/', views.edit_day, name='edit_day'),
    path('add-item/<int:day_id>/', views.add_item, name='add_item'),
    path('delete-item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('google-login/', views.google_login, name='google_login'),
]
