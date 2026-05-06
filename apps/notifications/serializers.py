from rest_framework import serializers
from .models import Notification, NotificationPreference


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id', 'event_type', 'message', 'entity_type', 'entity_id',
            'is_read', 'created_at'
        ]
        read_only_fields = ['created_at']


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = [
            'id', 'event_type', 'email_enabled', 'in_app_enabled', 'created_at'
        ]
        read_only_fields = ['created_at']
