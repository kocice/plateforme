from django.contrib import admin

from users.models import CustomUser
from django.contrib.auth.admin import UserAdmin
from agency_manager.models import Agence, Gestionnaire, Zone


class CustomUserInline(admin.TabularInline):
    model = CustomUser


@admin.register(Gestionnaire)
class GestionnaireAdmin(admin.ModelAdmin):
    pass
    # inlines = [CustomUserInline]


class GestionnaireInline(admin.TabularInline):
    model = Gestionnaire


@admin.register(Agence)
class AgenceAdmin(admin.ModelAdmin):
    search_fields = ('agency_name',)
    list_filter = ('agency_name', 'agency_manager',)
    ordering = ('-date_create',)
    list_display = ('agency_name', 'agency_manager', 'date_create')

    # inlines = [GestionnaireInline]

    # Vue détaille des utilisateurs
    fieldsets = (
        (None, {'fields': ('agency_name', 'date_create')}),
        ('Manager', {'fields': ('agency_manager',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'agency_name', 'date_create', 'longitude', 'latitude',
            )
        }),
    )


class AgenceInline(admin.TabularInline):
    model = Agence


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    search_fields = ('zone_name',)
    list_filter = ('zone_name',)
    ordering = ('-date_create',)
    list_display = ('zone_name', 'date_create', 'zone_chief')

    # inlines = [AgenceInline]

    # Vue détaille des utilisateurs
    fieldsets = (
        (None, {'fields': ('zone_name', 'date_create')}),
        ('Manager', {'fields': ('zone_chief',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'zone_name', 'date_create',
            )
        }),
    )
