from django.db import models
from django.conf import settings
from apps.missions.models import Mission


class Asset(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Maintenance', 'Maintenance'),
        ('Retired', 'Retired'),
        ('Lost', 'Lost'),
    ]

    inventory_tag = models.CharField(max_length=50, unique=True)
    device_type = models.CharField(max_length=100)
    make = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=True)
    operating_system = models.CharField(max_length=100, blank=True)
    os_version = models.CharField(max_length=50, blank=True)
    
    location_within_mission = models.CharField(max_length=255, blank=True)
    assigned_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_assets'
    )
    
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='assets')
    purchase_date = models.DateField(null=True, blank=True)
    warranty_expiry_date = models.DateField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'assets'
        verbose_name = 'Asset'
        verbose_name_plural = 'Assets'
        ordering = ['inventory_tag']

    def __str__(self):
        return f"{self.inventory_tag} - {self.device_type}"

    @property
    def is_out_of_warranty(self):
        """Check if asset is out of warranty"""
        if self.warranty_expiry_date:
            from django.utils import timezone
            return timezone.now().date() > self.warranty_expiry_date
        return False

    @property
    def ticket_count_90_days(self):
        """Count tickets in last 90 days"""
        from apps.tickets.models import Ticket
        from django.utils import timezone
        ninety_days_ago = timezone.now() - timezone.timedelta(days=90)
        return Ticket.objects.filter(
            linked_asset=self,
            created_at__gte=ninety_days_ago
        ).count()

    @property
    def needs_replacement(self):
        """Check if asset needs replacement based on warranty and ticket history"""
        return self.is_out_of_warranty or self.ticket_count_90_days > 3


class AssetTicketHistory(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='ticket_history')
    ticket = models.ForeignKey('tickets.Ticket', on_delete=models.CASCADE, related_name='asset_history')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'asset_ticket_history'
        verbose_name = 'Asset Ticket History'
        verbose_name_plural = 'Asset Ticket Histories'
        unique_together = ['asset', 'ticket']

    def __str__(self):
        return f"{self.asset.inventory_tag} - {self.ticket.ticket_number}"
