from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """Model for user profile information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"


class TravelPlan(models.Model):
    """Model for user travel itineraries"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='travel_plans')
    destination = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.title} ({self.destination})"

    class Meta:
        verbose_name = "Travel Plan"
        verbose_name_plural = "Travel Plans"
        ordering = ['start_date']

class TravelDay(models.Model):
    travel_plan = models.ForeignKey(TravelPlan, on_delete=models.CASCADE, related_name='days')
    label = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

class ItineraryItem(models.Model):
    day = models.ForeignKey(TravelDay, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


class UserSettings(models.Model):
    """Model for user settings/preferences"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    notifications_enabled = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    two_factor_auth = models.BooleanField(default=False)
    privacy_level = models.CharField(
        max_length=20,
        choices=[('public', 'Public'), ('private', 'Private'), ('friends_only', 'Friends Only')],
        default='private'
    )
    language = models.CharField(max_length=20, default='en')
    theme = models.CharField(
        max_length=20,
        choices=[('light', 'Light'), ('dark', 'Dark')],
        default='light'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Settings"

    class Meta:
        verbose_name = "User Settings"
        verbose_name_plural = "User Settings"



class Memory(models.Model):
    """Model for user memory images and titles"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memories')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='memories/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    class Meta:
        verbose_name = "Memory"
        verbose_name_plural = "Memories"
        ordering = ['-created_at']

