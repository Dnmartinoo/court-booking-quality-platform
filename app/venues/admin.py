from django.contrib import admin

from .models import Court, MaintenanceBlock, Venue


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
        "address",
        "active",
        "created_at",
    )
    list_filter = ("active",)
    search_fields = (
        "name",
        "address",
        "owner__username",
        "owner__email",
    )


@admin.register(Court)
class CourtAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "venue",
        "court_type",
        "price_per_slot",
        "active",
        "opening_time",
        "closing_time",
    )
    list_filter = (
        "court_type",
        "active",
        "venue",
    )
    search_fields = (
        "name",
        "venue__name",
    )


@admin.register(MaintenanceBlock)
class MaintenanceBlockAdmin(admin.ModelAdmin):
    list_display = (
        "court",
        "starts_at",
        "ends_at",
        "reason",
    )
    list_filter = (
        "court__venue",
        "court",
    )
    search_fields = (
        "court__name",
        "court__venue__name",
        "reason",
    )