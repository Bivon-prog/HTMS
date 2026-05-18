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

    working_week_start = models.IntegerField(default=1)
    working_week_end = models.IntegerField(default=5)
    work_start_time = models.TimeField(default='09:00')
    work_end_time = models.TimeField(default='17:00')

    status = models.CharField(max_length=20, default='Active', choices=[
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ])

    mission_id = models.CharField(max_length=50, blank=True, null=True, unique=True)
    seq_number = models.IntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'missions'
        verbose_name = 'Mission'
        verbose_name_plural = 'Missions'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} - {self.city}, {self.country}'

    def save(self, *args, **kwargs):
        if not self.mission_id:
            # Find the highest sequence number
            from apps.missions.models import Mission as MissionModel
            last_mission = MissionModel.objects.order_by('-seq_number').first()
            next_seq = 1
            if last_mission and last_mission.seq_number:
                next_seq = last_mission.seq_number + 1
            
            self.seq_number = next_seq
            self.mission_id = f"HTMS/MSN/{next_seq:04d}"
            
        super().save(*args, **kwargs)

    @property
    def kenyan_working_hours(self):
        import pytz
        from datetime import datetime, time
        
        today = datetime.now().date()
        tz = pytz.timezone(str(self.timezone))
        
        start_dt = tz.localize(datetime.combine(today, self.work_start_time))
        end_dt = tz.localize(datetime.combine(today, self.work_end_time))
        
        ke_tz = pytz.timezone('Africa/Nairobi')
        start_ke = start_dt.astimezone(ke_tz)
        end_ke = end_dt.astimezone(ke_tz)
        
        return f"{start_ke.strftime('%I:%M %p')} to {end_ke.strftime('%I:%M %p')}"

    def is_working_hours(self, datetime_obj=None):
        from django.utils import timezone
        import pytz

        if datetime_obj is None:
            datetime_obj = timezone.now()

        local_time = datetime_obj.astimezone(pytz.timezone(str(self.timezone)))
        iso = local_time.isoweekday()
        ws, we = self.working_week_start, self.working_week_end
        if ws <= we:
            if not (ws <= iso <= we):
                return False
        else:
            if not (iso >= ws or iso <= we):
                return False

        if HolidayCalendar.objects.filter(mission=self, holiday_date=local_time.date()).exists():
            return False

        current_time = local_time.time()
        return self.work_start_time <= current_time <= self.work_end_time


class HolidayCalendar(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='holidays')
    holiday_date = models.DateField()
    holiday_name = models.CharField(max_length=100)
    is_recurring = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'holiday_calendars'
        verbose_name = 'Holiday'
        verbose_name_plural = 'Holidays'
        ordering = ['holiday_date']
        unique_together = [['mission', 'holiday_date']]

    def __str__(self):
        return f'{self.holiday_name} - {self.mission.name} ({self.holiday_date})'


class TicketCategory(models.Model):
    ROUTING_DEPARTMENT_CHOICES = [
        ('IT', 'IT'),
        ('HR', 'HR'),
        ('Facilities', 'Facilities'),
        ('Finance', 'Finance'),
        ('Admin', 'Admin'),
    ]

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    routing_department = models.CharField(
        max_length=20,
        choices=ROUTING_DEPARTMENT_CHOICES,
        default='IT',
        help_text='Department queue this category routes to (SRS 3.4 / pdf2)',
    )
    auto_escalation_hours = models.IntegerField(null=True, blank=True, help_text='Hours before auto-escalation to HQ')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ticket_categories'
        verbose_name = 'Ticket Category'
        verbose_name_plural = 'Ticket Categories'
        ordering = ['name']

    def __str__(self):
        return self.name
