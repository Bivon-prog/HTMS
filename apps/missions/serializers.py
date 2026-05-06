from rest_framework import serializers
from .models import Mission, HolidayCalendar, TicketCategory


class HolidayCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = HolidayCalendar
        fields = ['id', 'holiday_date', 'holiday_name', 'is_recurring', 'created_at']
        read_only_fields = ['created_at']


class MissionSerializer(serializers.ModelSerializer):
    holidays = HolidayCalendarSerializer(many=True, read_only=True)
    user_count = serializers.SerializerMethodField()

    class Meta:
        model = Mission
        fields = [
            'id', 'name', 'country', 'city', 'region', 'timezone',
            'working_week_start', 'working_week_end', 'work_start_time',
            'work_end_time', 'status', 'created_at', 'updated_at',
            'holidays', 'user_count'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_user_count(self, obj):
        from apps.authentication.models import User
        return User.objects.filter(mission=obj, is_active=True).count()


class TicketCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketCategory
        fields = ['id', 'name', 'description', 'auto_escalation_hours', 'created_at']
        read_only_fields = ['created_at']
