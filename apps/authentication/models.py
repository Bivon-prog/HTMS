from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from timezone_field import TimeZoneField


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        # Set a dummy username for Django compatibility
        extra_fields['username'] = email
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = [
        ('Requester', 'Requester'),
        ('Agent', 'Agent'),
        ('Mission_Admin', 'Mission Admin'),
        ('HQ_Super_Admin', 'HQ Super Admin'),
    ]
    
    DEPARTMENT_CHOICES = [
        ('IT', 'IT'),
        ('HR', 'HR'),
        ('Facilities', 'Facilities'),
        ('Finance', 'Finance'),
        ('Admin', 'Admin'),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Requester')
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, blank=True, null=True)
    mission = models.ForeignKey('missions.Mission', on_delete=models.SET_NULL, null=True, blank=True)
    timezone = TimeZoneField(default='UTC')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def has_mission_access(self, mission):
        """Check if user has access to the given mission"""
        if self.role == 'HQ_Super_Admin':
            return True
        return self.mission == mission

    def can_view_all_mission_tickets(self):
        """Check if user can view all tickets in their mission"""
        return self.role in ['Agent', 'Mission_Admin', 'HQ_Super_Admin']

    def can_assign_tickets(self):
        """Check if user can assign tickets"""
        return self.role in ['Agent', 'Mission_Admin', 'HQ_Super_Admin']
