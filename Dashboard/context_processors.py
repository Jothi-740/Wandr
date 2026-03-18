from django.contrib.auth.models import User
from Account.models import TravelPlan, Memory, ItineraryItem

def admin_dashboard_stats(request):
    """Provides counts and data for the admin dashboard cards"""
    if request.path.startswith('/admin/'):
        return {
            'user_count': User.objects.count(),
            'plan_count': TravelPlan.objects.count(),
            'memory_count': Memory.objects.count(),
            'place_count': ItineraryItem.objects.count(),
            'latest_users': User.objects.order_by('-date_joined')[:5],
            'recent_memories': Memory.objects.order_by('-created_at')[:3],
        }
    return {}
