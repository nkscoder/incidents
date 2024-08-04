
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    pin_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    enterprise_or_government = models.CharField(max_length=100, choices=[('Enterprise', 'Enterprise'), ('Government', 'Government'), ('Individual', 'Individual')])


    def __str__(self):
        return self.username

class Incident(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    incident_id = models.CharField(max_length=20, unique=True)
    enterprise_or_government = models.CharField(max_length=100)
    reporter_name = models.CharField(max_length=100)
    incident_details = models.TextField()
    reported_datetime = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(max_length=20, choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')])
    status = models.CharField(max_length=20, choices=[('Open', 'Open'), ('In progress', 'In progress'), ('Closed', 'Closed')])
    def save(self, *args, **kwargs):
        if not self.pk and not self.incident_id:
            super().save(*args, **kwargs)
            self.incident_id = f'RMG{self.pk:05d}{datetime.now().year}'
            super().save(update_fields=['incident_id'])
        else:
            super().save(*args, **kwargs)