from rest_framework import serializers

from .models import Mission, TicketCategory


class TicketCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketCategory
        fields = ['id', 'name', 'description', 'routing_department', 'auto_escalation_hours']


class MissionSerializer(serializers.ModelSerializer):
    mission_admin_id = serializers.SerializerMethodField()

    class Meta:
        model = Mission
        fields = [
            'id', 'name', 'country', 'city', 'region', 'timezone',
            'working_week_start', 'working_week_end', 'work_start_time', 'work_end_time',
            'status', 'mission_admin_id', 'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_mission_admin_id(self, obj):
        admin = obj.user_set.filter(role='Mission_Admin').first()
        return admin.id if admin else None
