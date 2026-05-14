from rest_framework import serializers

from .models import Mission, TicketCategory


class TicketCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketCategory
        fields = ['id', 'name', 'description', 'routing_department', 'auto_escalation_hours']


class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = [
            'id', 'name', 'country', 'city', 'region', 'timezone',
            'working_week_start', 'working_week_end', 'work_start_time', 'work_end_time',
            'status', 'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']
