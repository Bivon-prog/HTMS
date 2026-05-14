from rest_framework import serializers

from apps.authentication.models import OnBehalfOfGrant, User
from .models import Ticket, TicketComment, TicketAttachment, AuditLog


class TicketAttachmentSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.CharField(source='uploaded_by.get_full_name', read_only=True)
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = TicketAttachment
        fields = [
            'id', 'filename', 'mime_type', 'file_size_bytes',
            'uploaded_by', 'uploaded_by_name', 'virus_scanned', 'created_at', 'download_url',
        ]
        read_only_fields = ['uploaded_by', 'virus_scanned', 'created_at']

    def get_download_url(self, obj):
        request = self.context.get('request')
        if not request:
            return None
        path = f'/api/tickets/{obj.ticket_id}/attachments/{obj.pk}/download/'
        return request.build_absolute_uri(path)


class TicketCommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    author_role = serializers.CharField(source='author.role', read_only=True)
    attachments = TicketAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = TicketComment
        fields = [
            'id', 'content', 'is_internal', 'author', 'author_name',
            'author_role', 'created_at', 'attachments',
        ]
        read_only_fields = ['author', 'created_at']

    def create(self, validated_data):
        return super().create(validated_data)


class TicketSerializer(serializers.ModelSerializer):
    requester_name = serializers.CharField(source='requester.get_full_name', read_only=True)
    requester_email = serializers.CharField(source='requester.email', read_only=True)
    beneficiary_name = serializers.SerializerMethodField()
    agent_name = serializers.CharField(source='assigned_agent.get_full_name', read_only=True)
    agent_email = serializers.CharField(source='assigned_agent.email', read_only=True)

    category_name = serializers.CharField(source='category.name', read_only=True)
    mission_name = serializers.CharField(source='mission.name', read_only=True)

    comments = TicketCommentSerializer(many=True, read_only=True)
    attachments = TicketAttachmentSerializer(many=True, read_only=True)

    comment_count = serializers.SerializerMethodField()
    is_overdue = serializers.BooleanField(read_only=True)
    submission_display = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = [
            'id', 'ticket_number', 'title', 'description', 'priority', 'status',
            'category', 'category_name', 'requester', 'requester_name', 'requester_email',
            'beneficiary', 'beneficiary_name', 'submission_display',
            'assigned_agent', 'agent_name', 'agent_email', 'mission', 'mission_name',
            'linked_asset', 'escalated_to_hq', 'escalation_reason',
            'sla_due_date', 'resolved_date', 'closed_date',
            'created_at', 'updated_at', 'comments', 'attachments',
            'comment_count', 'is_overdue',
        ]
        read_only_fields = [
            'ticket_number', 'requester', 'beneficiary', 'resolved_date', 'closed_date',
            'created_at', 'updated_at',
        ]

    def get_beneficiary_name(self, obj):
        if obj.beneficiary_id:
            return obj.beneficiary.get_full_name()
        return None

    def get_comment_count(self, obj):
        return obj.comments.count()

    def get_submission_display(self, obj):
        if obj.beneficiary_id:
            return f'{obj.requester.get_full_name()} on behalf of {obj.beneficiary.get_full_name()}'
        return obj.requester.get_full_name()

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        beneficiary = validated_data.pop('beneficiary', None)

        validated_data['requester'] = user
        validated_data['mission'] = user.mission

        if beneficiary:
            if not OnBehalfOfGrant.objects.filter(
                mission=user.mission,
                assistant=user,
                official=beneficiary,
                is_active=True,
            ).exists():
                raise serializers.ValidationError(
                    {'beneficiary': 'No active On-Behalf-Of authorisation for this official.'}
                )
            validated_data['beneficiary'] = beneficiary
            if validated_data.get('priority') == 'Low':
                validated_data['priority'] = 'High'

        instance = super().create(validated_data)

        from apps.tickets.working_hours import compute_ticket_sla_due
        from apps.tickets.assignment import assign_round_robin
        from apps.notifications.notify import notify_ticket_routing, notify_users

        instance.sla_due_date = compute_ticket_sla_due(instance)
        instance.save(update_fields=['sla_due_date', 'updated_at'])

        assign_round_robin(instance)

        AuditLog.objects.create(
            user=user,
            action='Created',
            entity_type='ticket',
            entity_id=instance.id,
            new_values={'ticket_number': instance.ticket_number, 'title': instance.title},
            ip_address=request.META.get('REMOTE_ADDR'),
        )

        notify_ticket_routing(instance)
        if instance.beneficiary_id:
            notify_users(
                'ticket_created',
                [instance.beneficiary],
                f'Ticket {instance.ticket_number} was raised on your behalf: {instance.title}',
                entity_type='ticket',
                entity_id=instance.id,
            )

        return instance


class TicketCreateSerializer(TicketSerializer):
    beneficiary = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False, allow_null=True,
    )

    class Meta(TicketSerializer.Meta):
        fields = [
            'title', 'description', 'category', 'priority', 'linked_asset', 'beneficiary',
        ]
        read_only_fields = [
            'ticket_number', 'requester', 'resolved_date', 'closed_date',
            'created_at', 'updated_at',
        ]


class TicketStatusUpdateSerializer(serializers.ModelSerializer):
    comment = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Ticket
        fields = ['status', 'comment']

    def update(self, instance, validated_data):
        comment_text = validated_data.pop('comment', None)
        old_status = instance.status

        instance = super().update(instance, validated_data)

        if comment_text:
            TicketComment.objects.create(
                ticket=instance,
                author=self.context['request'].user,
                content=comment_text,
                is_internal=False,
            )

        AuditLog.objects.create(
            user=self.context['request'].user,
            action='Status Changed',
            entity_type='ticket',
            entity_id=instance.id,
            old_values={'status': old_status},
            new_values={'status': instance.status},
            ip_address=self.context['request'].META.get('REMOTE_ADDR'),
        )

        return instance


class TicketAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['assigned_agent']

    def update(self, instance, validated_data):
        old_agent = instance.assigned_agent
        instance = super().update(instance, validated_data)

        AuditLog.objects.create(
            user=self.context['request'].user,
            action='Assigned',
            entity_type='ticket',
            entity_id=instance.id,
            old_values={'assigned_agent': old_agent.id if old_agent else None},
            new_values={'assigned_agent': instance.assigned_agent.id if instance.assigned_agent else None},
            ip_address=self.context['request'].META.get('REMOTE_ADDR'),
        )

        return instance


class AuditLogSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            'id', 'action', 'entity_type', 'entity_id', 'old_values',
            'new_values', 'user_name', 'ip_address', 'created_at',
        ]
        read_only_fields = ['user', 'created_at']
