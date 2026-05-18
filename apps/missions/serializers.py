from rest_framework import serializers

from .models import Mission, TicketCategory


class TicketCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketCategory
        fields = ['id', 'name', 'description', 'routing_department', 'auto_escalation_hours']


class MissionSerializer(serializers.ModelSerializer):
    mission_admin_id = serializers.SerializerMethodField()
    mission_admin_name = serializers.SerializerMethodField()

    class Meta:
        model = Mission
        fields = [
            'id', 'mission_id', 'name', 'country', 'city', 'region', 'timezone',
            'working_week_start', 'working_week_end', 'work_start_time', 'work_end_time',
            'status', 'mission_admin_id', 'mission_admin_name', 'kenyan_working_hours', 'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at', 'mission_id', 'kenyan_working_hours']

    def _get_admin(self, obj):
        from apps.authentication.models import User
        return User.objects.filter(mission=obj, role='Mission_Admin').first()

    def get_mission_admin_id(self, obj):
        admin = self._get_admin(obj)
        return str(admin.id) if admin else None

    def get_mission_admin_name(self, obj):
        admin = self._get_admin(obj)
        return admin.get_full_name() if admin else None
