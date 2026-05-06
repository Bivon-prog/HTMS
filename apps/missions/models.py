from django.db import models
from timezone_field import TimeZoneField


class Mission(models.Model):
    REGION_CHOICES = [
        ('Africa', 'Africa'),
        ('Europe', 'Europe'),
        ('Americas', 'Americas'),
        ('Asia', 'Asia'),
        ('Middle_East', 'Middle East'),
        ('Multilateral', 'Multilateral'),
    ]

    name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=20, choices=REGION_CHOICES)
    timezone = TimeZoneField()
    
    # Working hours configuration
    working_week_start = models.IntegerField(default=1)  # 1=Monday, 7=Sunday
    working_week_end = models.IntegerField(default=5)    # 5=Friday
    work_start_time = models.TimeField(default='09:00')
    work_end_time = models.TimeField(default='17:00')
    
    status = models.CharField(max_length=20, default='Active', choices=[
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'missions'
        verbose_name = 'Mission'
        verbose_name_plural = 'Missions'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.city}, {self.country}"

    def is_working_hours(self, datetime_obj=None):
        """Check if given datetime is within working hours for this mission"""
        from django.utils import timezone
        import pytz
        
        if datetime_obj is None:
            datetime_obj = timezone.now()
        
        # Convert to mission timezone
        local_time = datetime_obj.astimezone(pytz.timezone(str(self.timezone)))
        
        # Check day of week
        if not (self.working_week_start <= local_time.isoweekday() <= self.working_week_end):
            return False
        
        # Check time of day
        current_time = local_time.time()
        return self.work_start_time <= current_time <= self.work_end_time


class HolidayCalendar(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='holidays')
    holiday_date = models.DateField()
    holiday_name = models.CharField(max_length=100)
    is_recurring = models.BooleanField(default=False)  # For annual holidays
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'holiday_calendars'
        verbose_name = 'Holiday'
        verbose_name_plural = 'Holidays'
        ordering = ['holiday_date']
        unique_together = ['mission', 'holiday_date']

    def __str__(self):
        return f"{self.holiday_name} - {self.mission.name} ({self.holiday_date})"


class TicketCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    auto_escalation_hours = models.IntegerField(null=True, blank=True, help_text="Hours before auto-escalation to HQ")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ticket_categories'
        verbose_name = 'Ticket Category'
        verbose_name_plural = 'Ticket Categories'
        ordering = ['name']

    def __str__(self):
        return self.name
