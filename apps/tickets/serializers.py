from rest_framework import serializers
from .models import Ticket, TicketComment, TicketAttachment, AuditLog
from apps.authentication.serializers import UserSerializer
from apps.missions.serializers import MissionSerializer, TicketCategorySerializer


class TicketAttachmentSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.CharField(source='uploaded_by.get_full_name', read_only=True)
    
    class Meta:
        model = TicketAttachment
        fields = [
            'id', 'filename', 'file', 'mime_type', 'file_size_bytes',
            'uploaded_by', 'uploaded_by_name', 'virus_scanned', 'created_at'
        ]
        read_only_fields = ['uploaded_by', 'virus_scanned', 'created_at']


class TicketCommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    author_role = serializers.CharField(source='author.role', read_only=True)
    attachments = TicketAttachmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = TicketComment
        fields = [
            'id', 'content', 'is_internal', 'author', 'author_name', 
            'author_role', 'created_at', 'attachments'
        ]
        read_only_fields = ['author', 'created_at']

    def create(self, validated_data):
        # author is set by the view's perform_create
        return super().create(validated_data)


class TicketSerializer(serializers.ModelSerializer):
    requester_name = serializers.CharField(source='requester.get_full_name', read_only=True)
    requester_email = serializers.CharField(source='requester.email', read_only=True)
    agent_name = serializers.CharField(source='assigned_agent.get_full_name', read_only=True)
    agent_email = serializers.CharField(source='assigned_agent.email', read_only=True)
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    mission_name = serializers.CharField(source='mission.name', read_only=True)
    
    comments = TicketCommentSerializer(many=True, read_only=True)
    attachments = TicketAttachmentSerializer(many=True, read_only=True)
    
    comment_count = serializers.SerializerMethodField()
    is_overdue = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Ticket
        fields = [
            'id', 'ticket_number', 'title', 'description', 'priority', 'status',
            'category', 'category_name', 'requester', 'requester_name', 'requester_email',
            'assigned_agent', 'agent_name', 'agent_email', 'mission', 'mission_name',
            'linked_asset', 'escalated_to_hq', 'escalation_reason',
            'sla_due_date', 'resolved_date', 'closed_date',
            'created_at', 'updated_at', 'comments', 'attachments',
            'comment_count', 'is_overdue'
        ]
        read_only_fields = [
            'ticket_number', 'requester', 'resolved_date', 'closed_date',
            'created_at', 'updated_at'
        ]

    def get_comment_count(self, obj):
        return obj.comments.count()

    def create(self, validated_data):
        validated_data['requester'] = self.context['request'].user
        validated_data['mission'] = self.context['request'].user.mission
        
        # Calculate SLA due date based on category
        if validated_data['category'].auto_escalation_hours:
            from datetime import timedelta
            from django.utils import timezone
            validated_data['sla_due_date'] = timezone.now() + timedelta(
                hours=validated_data['category'].auto_escalation_hours
            )
        
        return super().create(validated_data)


class TicketCreateSerializer(TicketSerializer):
    class Meta(TicketSerializer.Meta):
        fields = [
            'title', 'description', 'category', 'priority', 'linked_asset'
        ]


class TicketStatusUpdateSerializer(serializers.ModelSerializer):
    comment = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = Ticket
        fields = ['status', 'comment']

    def update(self, instance, validated_data):
        comment_text = validated_data.pop('comment', None)
        old_status = instance.status
        
        # Update ticket status
        instance = super().update(instance, validated_data)
        
        # Add comment if provided
        if comment_text:
            TicketComment.objects.create(
                ticket=instance,
                author=self.context['request'].user,
                content=comment_text,
                is_internal=False
            )
        
        # Create audit log
        AuditLog.objects.create(
            user=self.context['request'].user,
            action='Status Changed',
            entity_type='ticket',
            entity_id=instance.id,
            old_values={'status': old_status},
            new_values={'status': instance.status},
            ip_address=self.context['request'].META.get('REMOTE_ADDR')
        )
        
        return instance


class TicketAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['assigned_agent']

    def update(self, instance, validated_data):
        old_agent = instance.assigned_agent
        instance = super().update(instance, validated_data)
        
        # Create audit log
        AuditLog.objects.create(
            user=self.context['request'].user,
            action='Assigned',
            entity_type='ticket',
            entity_id=instance.id,
            old_values={'assigned_agent': old_agent.id if old_agent else None},
            new_values={'assigned_agent': instance.assigned_agent.id if instance.assigned_agent else None},
            ip_address=self.context['request'].META.get('REMOTE_ADDR')
        )
        
        return instance


class AuditLogSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = AuditLog
        fields = [
            'id', 'action', 'entity_type', 'entity_id', 'old_values',
            'new_values', 'user_name', 'ip_address', 'created_at'
        ]
        read_only_fields = ['user', 'created_at']
