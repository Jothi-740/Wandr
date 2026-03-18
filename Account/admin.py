from django.contrib import admin
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from .models import UserProfile, TravelPlan, TravelDay, ItineraryItem, UserSettings, Memory

# ─────────────────────────────────────────────
# Customize Admin Site Header
# ─────────────────────────────────────────────
admin.site.site_header  = "🌍 Wandr Admin Panel"
admin.site.site_title   = "Wandr Admin"
admin.site.index_title  = "Welcome to Wandr Management"


# ─────────────────────────────────────────────
# Inline: TravelDay inside TravelPlan
# ─────────────────────────────────────────────
class ItineraryItemInline(admin.TabularInline):
    model = ItineraryItem
    extra = 0
    fields = ('title', 'created_at')
    readonly_fields = ('created_at',)


class TravelDayInline(admin.StackedInline):
    model = TravelDay
    extra = 0
    fields = ('label', 'description', 'created_at')
    readonly_fields = ('created_at',)
    show_change_link = True


# ─────────────────────────────────────────────
# UserProfile Admin
# ─────────────────────────────────────────────
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display  = ('user_avatar', 'full_name', 'username', 'city', 'country', 'phone', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'city', 'country', 'phone')
    list_filter   = ('country', 'created_at')
    readonly_fields = ('created_at', 'updated_at', 'user_avatar_large')
    ordering      = ('-created_at',)

    fieldsets = (
        ('👤 User', {
            'fields': ('user', 'user_avatar_large', 'profile_picture', 'bio')
        }),
        ('📍 Location', {
            'fields': ('city', 'state', 'country', 'postal_code', 'address')
        }),
        ('📞 Contact', {
            'fields': ('phone',)
        }),
        ('🕒 Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def user_avatar(self, obj):
        if obj.profile_picture:
            return mark_safe(f'<img src="{obj.profile_picture.url}" width="40" height="40" style="border-radius: 50%; object-fit: cover; border: 2px solid #4cc9f0;" />')
        return "—"
    user_avatar.short_description = 'Photo'

    def user_avatar_large(self, obj):
        if obj.profile_picture:
            return mark_safe(f'<img src="{obj.profile_picture.url}" width="120" height="120" style="border-radius: 50%; object-fit: cover; border: 3px solid #4cc9f0;" />')
        return "No photo uploaded"
    user_avatar_large.short_description = 'Profile Picture Preview'

    def full_name(self, obj):
        return obj.user.get_full_name() or "—"
    full_name.short_description = 'Full Name'

    def username(self, obj):
        return obj.user.username
    username.short_description = 'Username'


# ─────────────────────────────────────────────
# TravelPlan Admin
# ─────────────────────────────────────────────
@admin.register(TravelPlan)
class TravelPlanAdmin(admin.ModelAdmin):
    list_display  = ('title', 'user', 'destination', 'start_date', 'end_date', 'duration_days', 'created_at')
    search_fields = ('title', 'destination', 'user__username')
    list_filter   = ('start_date', 'end_date')
    readonly_fields = ('created_at', 'updated_at')
    ordering      = ('-created_at',)
    inlines       = [TravelDayInline]

    fieldsets = (
        ('📋 Plan Details', {
            'fields': ('user', 'title', 'destination', 'description')
        }),
        ('📅 Dates', {
            'fields': ('start_date', 'end_date')
        }),
        ('🕒 Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def duration_days(self, obj):
        if obj.start_date and obj.end_date:
            delta = (obj.end_date - obj.start_date).days
            return f"{delta} day{'s' if delta != 1 else ''}"
        return "—"
    duration_days.short_description = 'Duration'


# ─────────────────────────────────────────────
# UserSettings Admin
# ─────────────────────────────────────────────
@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display  = ('user', 'language', 'theme', 'privacy_level', 'notifications_enabled', 'two_factor_auth', 'updated_at')
    search_fields = ('user__username',)
    list_filter   = ('language', 'theme', 'privacy_level', 'notifications_enabled', 'two_factor_auth')
    readonly_fields = ('created_at', 'updated_at')
    ordering      = ('user__username',)

    fieldsets = (
        ('👤 User', {
            'fields': ('user',)
        }),
        ('🔔 Notifications', {
            'fields': ('notifications_enabled', 'email_notifications', 'sms_notifications')
        }),
        ('🔒 Security & Privacy', {
            'fields': ('two_factor_auth', 'privacy_level')
        }),
        ('🎨 Preferences', {
            'fields': ('language', 'theme')
        }),
        ('🕒 Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# ─────────────────────────────────────────────
# Memory Admin
# ─────────────────────────────────────────────
@admin.register(Memory)
class MemoryAdmin(admin.ModelAdmin):
    list_display  = ('memory_thumb', 'title', 'user', 'created_at')
    search_fields = ('title', 'user__username', 'description')
    list_filter   = ('created_at',)
    readonly_fields = ('created_at', 'memory_thumb_large')
    ordering      = ('-created_at',)

    fieldsets = (
        ('🖼️ Memory', {
            'fields': ('user', 'title', 'description', 'image', 'memory_thumb_large')
        }),
        ('🕒 Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def memory_thumb(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="60" height="40" style="object-fit: cover; border-radius: 6px;" />')
        return "—"
    memory_thumb.short_description = 'Image'

    def memory_thumb_large(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="300" style="object-fit: cover; border-radius: 10px;" />')
        return "No image uploaded"
    memory_thumb_large.short_description = 'Preview'
