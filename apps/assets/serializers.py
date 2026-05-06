from rest_framework import serializers
from .models import Asset, AssetTicketHistory
from apps.authentication.serializers import UserSerializer
from apps.missions.serializers import MissionSerializer


class AssetSerializer(serializers.ModelSerializer):
    assigned_user_name = serializers.CharField(source='assigned_user.get_full_name', read_only=True)
    mission_name = serializers.CharField(source='mission.name', read_only=True)
    is_out_of_warranty = serializers.BooleanField(read_only=True)
    ticket_count_90_days = serializers.IntegerField(read_only=True)
    needs_replacement = serializers.BooleanField(read_only=True)

    class Meta:
        model = Asset
        fields = [
            'id', 'inventory_tag', 'device_type', 'make', 'model',
            'operating_system', 'os_version', 'location_within_mission',
            'assigned_user', 'assigned_user_name', 'mission', 'mission_name',
            'purchase_date', 'warranty_expiry_date', 'status', 'notes',
            'created_at', 'updated_at', 'is_out_of_warranty',
            'ticket_count_90_days', 'needs_replacement'
        ]
        read_only_fields = ['created_at', 'updated_at']


class AssetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = [
            'inventory_tag', 'device_type', 'make', 'model',
            'operating_system', 'os_version', 'location_within_mission',
            'assigned_user', 'mission', 'purchase_date',
            'warranty_expiry_date', 'status', 'notes'
        ]

    def create(self, validated_data):
        # Set mission based on user if not provided
        if 'mission' not in validated_data and self.context['request'].user.role != 'HQ_Super_Admin':
            validated_data['mission'] = self.context['request'].user.mission
        return super().create(validated_data)


class AssetTicketHistorySerializer(serializers.ModelSerializer):
    ticket_number = serializers.CharField(source='ticket.ticket_number', read_only=True)
    ticket_title = serializers.CharField(source='ticket.title', read_only=True)

    class Meta:
        model = AssetTicketHistory
        fields = ['id', 'asset', 'ticket', 'ticket_number', 'ticket_title', 'created_at']
        read_only_fields = ['created_at']
