from django.db import models
from django.contrib.auth.models import User, Group

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Department(models.Model):
    DepartmentId = models.AutoField(primary_key=True)
    DepartmentName = models.CharField(max_length=100)

    def __str__(self):
        return self.DepartmentName

class Employee(models.Model):
    EmployeeId = models.AutoField(primary_key=True)
    EmployeeName = models.CharField(max_length=100)
    Designation = models.CharField(max_length=100)
    DateOfJoining = models.DateField()
    DepartmentId = models.ForeignKey(Department, on_delete=models.CASCADE)
    Contact = models.CharField(max_length=15)
    IsActive = models.BooleanField(default=True)

    def __str__(self):
        return self.EmployeeName

class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_details')
    phoneno = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.user.username
