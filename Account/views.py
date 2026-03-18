from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator

from .models import UserProfile, TravelPlan, TravelDay, ItineraryItem, UserSettings, Memory  # type: ignore


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
import json
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests

def login_view(request):
    """Login page"""
    if request.method == 'POST':
        login_id = request.POST.get('loginId')
        password = request.POST.get('password')
        
        user = None
        try:
            if '@' in login_id:
                user_obj = User.objects.get(email=login_id)
                user = authenticate(request, username=user_obj.username, password=password)
            else:
                user_obj = UserProfile.objects.get(phone=login_id).user
                user = authenticate(request, username=user_obj.username, password=password)
        except (User.DoesNotExist, UserProfile.DoesNotExist):
            user = authenticate(request, username=login_id, password=password)
            
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials.')
            
    return render(request, 'login.html')


def signup_view(request):
    """Signup page"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        
        # Simple username logic: use email prefix
        username = email.split('@')[0] if email else mobile
        if User.objects.filter(username=username).exists():
            username = f"{username}{mobile[-4:]}"
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'signup.html')
            
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = name
        user.save()
        
        # Create user profile
        UserProfile.objects.create(user=user, phone=mobile)
        
        # Log them in automatically
        login(request, user)
        messages.success(request, 'Account created successfully!')
        return redirect('home')
        
    return render(request, 'signup.html')


@csrf_exempt
def google_login(request):
    """Handle Google Login/Signup via Google Identity Services"""
    if request.method == 'POST':
        try:
            # Handle both JSON (popup) and URL-encoded (redirect) POST data
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                token = data.get('credential')
            else:
                token = request.POST.get('credential')
            
            if not token:
                raise ValueError("No credential token received.")
            
            # Global Google Client ID
            CLIENT_ID = "155807928935-vb36t88v1dkqp7smmgc4hs6ncmc6kq2e.apps.googleusercontent.com"
            
            # Verify the token
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
            
            email = idinfo['email']
            first_name = idinfo.get('given_name', '')
            last_name = idinfo.get('family_name', '')
            
            # Find or create user
            user = User.objects.filter(email=email).first()
            
            if not user:
                # Create a new user if they don't exist
                username = email.split('@')[0]
                # Ensure username is unique
                original_username = username
                counter = 1
                while User.objects.filter(username=username).exists():
                    username = f"{original_username}{counter}"
                    counter += 1
                
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name
                )
                # Create profile
                UserProfile.objects.create(user=user)
                messages.success(request, f'Welcome to Wandr, {first_name}!')
            
            # Log the user in
            login(request, user)
            
            # For redirect mode, we need to return a redirect response, not JSON
            if request.content_type != 'application/json':
                return redirect('home')
                
            return JsonResponse({
                'status': 'success', 
                'redirect_url': reverse('home')
            })
            
        except Exception as e:
            if request.content_type != 'application/json':
                messages.error(request, f"Authentication failed: {str(e)}")
                return redirect('login')
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@login_required(login_url='login')
def account_dashboard(request):
    """Main Account dashboard view"""
    context = {}
    try:
        profile = UserProfile.objects.get(user=request.user)
        context['profile'] = profile
    except UserProfile.DoesNotExist:
        context['profile'] = None
    
    try:
        settings = UserSettings.objects.get(user=request.user)
        context['settings'] = settings
    except UserSettings.DoesNotExist:
        context['settings'] = None
    
    plans = TravelPlan.objects.filter(user=request.user)
    context['plans'] = plans
    
    
    return render(request, 'Account/account.html', context)


@login_required(login_url='login')
def profile_view(request):
    """User Profile page"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        profile.phone = request.POST.get('phone', profile.phone)
        profile.address = request.POST.get('address', profile.address)
        profile.city = request.POST.get('city', profile.city)
        profile.state = request.POST.get('state', profile.state)
        profile.postal_code = request.POST.get('postal_code', profile.postal_code)
        profile.country = request.POST.get('country', profile.country)
        profile.bio = request.POST.get('bio', profile.bio)
        
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
        
        profile.save()

        # Update User fields
        user = request.user
        
        new_username = request.POST.get('username')
        if new_username and new_username != user.username:
            if User.objects.filter(username=new_username).exists():
                messages.error(request, 'That username is already taken.')
            else:
                user.username = new_username

        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('account:profile')
    
    context = {
        'profile': profile,
        'memories': Memory.objects.filter(user=request.user)
    }
    return render(request, 'Account/profile.html', context)


@login_required(login_url='login')
def plans_view(request):
    """User Plans page"""
    if request.method == 'POST':
        plan_id = request.POST.get('plan_id')
        title = request.POST.get('title')
        destination = request.POST.get('destination')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        description = request.POST.get('description')
        
        if plan_id:
            plan = get_object_or_404(TravelPlan, id=plan_id, user=request.user)
            plan.title = title
            plan.destination = destination
            plan.start_date = start_date
            plan.end_date = end_date
            plan.description = description
            plan.save()
            messages.success(request, 'Itinerary updated successfully!')
        else:
            TravelPlan.objects.create(
                user=request.user,
                title=title,
                destination=destination,
                start_date=start_date,
                end_date=end_date,
                description=description
            )
            messages.success(request, 'Itinerary created successfully!')
        return redirect('account:plans')

    plans = TravelPlan.objects.filter(user=request.user).order_by('start_date')
    
    context = {
        'plans': plans,
    }
    return render(request, 'Account/plans.html', context)

@require_http_methods(["POST"])
@login_required(login_url='login')
def delete_plan(request, plan_id):
    plan = get_object_or_404(TravelPlan, id=plan_id, user=request.user)
    plan.delete()
    messages.success(request, 'Itinerary deleted.')
    return redirect('account:plans')

@require_http_methods(["POST"])
@login_required(login_url='login')
def add_day(request, plan_id):
    plan = get_object_or_404(TravelPlan, id=plan_id, user=request.user)
    TravelDay.objects.create(travel_plan=plan)
    messages.success(request, 'New day added to your trip.')
    return redirect(f'/account/plans/#plan-{plan_id}')

@require_http_methods(["POST"])
@login_required(login_url='login')
def delete_day(request, day_id):
    day = get_object_or_404(TravelDay, id=day_id, travel_plan__user=request.user)
    day.delete()
    messages.success(request, 'Day removed from itinerary.')
    return redirect(f'/account/plans/#plan-{day.travel_plan.id}')

@require_http_methods(["POST"])
@login_required(login_url='login')
def edit_day(request, day_id):
    day = get_object_or_404(TravelDay, id=day_id, travel_plan__user=request.user)
    label = request.POST.get('label')
    description = request.POST.get('description')
    day.label = label
    day.description = description
    day.save()
    messages.success(request, 'Day details updated.')
    return redirect(f'/account/plans/#plan-{day.travel_plan.id}')

@require_http_methods(["POST"])
@login_required(login_url='login')
def add_item(request, day_id):
    day = get_object_or_404(TravelDay, id=day_id, travel_plan__user=request.user)
    title = request.POST.get('title')
    if title:
        ItineraryItem.objects.create(day=day, title=title)
        messages.success(request, 'Item added to day.')
    return redirect(f'/account/plans/#plan-{day.travel_plan.id}')

@require_http_methods(["POST"])
@login_required(login_url='login')
def delete_item(request, item_id):
    item = get_object_or_404(ItineraryItem, id=item_id, day__travel_plan__user=request.user)
    item.delete()
    messages.success(request, 'Item removed.')
    return redirect(f'/account/plans/#plan-{item.day.travel_plan.id}')


@login_required(login_url='login')
def settings_view(request):
    """User Settings page"""
    settings, created = UserSettings.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        settings.notifications_enabled = request.POST.get('notifications_enabled') == 'on'
        settings.email_notifications = request.POST.get('email_notifications') == 'on'
        settings.sms_notifications = request.POST.get('sms_notifications') == 'on'
        settings.two_factor_auth = request.POST.get('two_factor_auth') == 'on'
        settings.privacy_level = request.POST.get('privacy_level', settings.privacy_level)
        settings.language = request.POST.get('language', settings.language)
        settings.theme = request.POST.get('theme', settings.theme)
        
        settings.save()
        messages.success(request, 'Settings updated successfully!')
        return redirect('account:settings')
    
    context = {'settings': settings}
    return render(request, 'Account/settings.html', context)



@require_http_methods(["POST"])
@login_required(login_url='login')
def add_memory(request):
    """AJAX endpoint to upload a new memory"""
    title = request.POST.get('title')
    description = request.POST.get('description')
    image = request.FILES.get('image')
    
    if title and image:
        memory = Memory.objects.create(
            user=request.user, 
            title=title, 
            description=description,
            image=image
        )
        return JsonResponse({
            'status': 'success',
            'memory_id': memory.id,
            'title': memory.title,
            'description': memory.description,
            'image_url': memory.image.url
        })
    else:
        return JsonResponse({'status': 'error', 'message': 'Missing data'}, status=400)

@require_http_methods(["POST", "DELETE"])
@login_required(login_url='login')
def delete_memory(request, memory_id):
    """AJAX endpoint to delete a memory"""
    memory = get_object_or_404(Memory, id=memory_id, user=request.user)
    memory.delete()
    return JsonResponse({'status': 'success'})

@require_http_methods(["POST"])
@login_required(login_url='login')
def delete_account(request):
    """View to delete user account completely"""
    user = request.user
    logout(request)
    user.delete()
    return redirect('login')
