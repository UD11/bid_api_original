from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from bidapp.models import User,team
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    # Add any customization specific to your User model here
    list_display = ('id', 'firstname', 'lastname', 'email','team', 'username', 'password', 'year', 'user_image',
                  'player_position', 'owner', 'coowner', 'player_value',
                    'marquee', 'captain','vicecaptain', 'department', 'host', 'is_active',
                    'date_joined','sold')
    search_fields = ('username', 'email','firstname', 'lastname')
    list_display_links = ('username', 'email','firstname', 'lastname')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': (
        'firstname', 'lastname','team','year', 'user_image', 'player_position','owner', 'coowner', 'player_value', 'marquee',
        'captain', 'department', 'host','sold')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


class TeamAdmin(admin.ModelAdmin):
    search_fields = ['team_name']
    list_display_links = ['team_name', 'owner', 'coowner', 'captain','vicecaptain','marquee']
    filter_horizontal = ['players']
    list_display = ('id','team_name', 'owner', 'coowner', 'captain', 'vicecaptain','pot','marquee')
    # autocomplete_fields = ['owner__firstname', 'coowner', 'captain', 'vicecaptain','marquee']
    raw_id_fields = ['owner', 'coowner', 'captain', 'vicecaptain', 'marquee']

    fieldsets = (
        (None, {'fields': ('team_name','pot')}),
        ('Owners and Captains', {'fields': ('owner', 'coowner', 'captain','marquee','vicecaptain')}),
        ('Players', {'fields': ('players',)}),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(team, TeamAdmin)
