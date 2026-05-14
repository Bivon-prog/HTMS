from django.contrib import admin

from .models import HolidayCalendar, Mission, TicketCategory


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'city', 'region', 'status']
    list_filter = ['region', 'status']


@admin.register(TicketCategory)
class TicketCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'routing_department', 'auto_escalation_hours']


@admin.register(HolidayCalendar)
class HolidayCalendarAdmin(admin.ModelAdmin):
    list_display = ['holiday_name', 'mission', 'holiday_date']
