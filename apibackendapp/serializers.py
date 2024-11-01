from rest_framework import serializers
from .models import Employee, Department, UserDetails

from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password

class SignupSerializer(serializers.ModelSerializer):
    #override create method to change the password into hash.

    group_name = serializers.CharField(write_only=True, required=False)  # Add group name field

    def create(self, validated_data):
        # Remove group_name from validated_data to avoid issues with the User model
        group_name = validated_data.pop("group_name", None)

        # Hash the password
        validated_data["password"] = make_password(validated_data.get("password"))
        
        # Create the user
        user = super(SignupSerializer, self).create(validated_data)

        # Add the user to the group if group_name is provided
        if group_name:
            group, created = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)

        return user

    class Meta:
        model = User
        fields = ['username', 'password', 'group_name']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'password']
 
    
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('DepartmentId', 'DepartmentName')

from datetime import date
import re
def date_of_joining_restriction(dateOfJoining):
    today = date.today()
    if dateOfJoining != today:
        raise serializers.ValidationError("The date of joining must be today")
    return dateOfJoining

def name_validation(employeeName):
    if len(employeeName) < 3 or not re.match("^[A-Za-z]+$", employeeName):
        raise serializers.ValidationError("Name must be at least 3 letters and contain only alphabetic characters")
    return employeeName

class EmployeeSerializer(serializers.ModelSerializer):
    Department = DepartmentSerializer(source='DepartmentId', read_only=True)  # Nested serializer to include Department details
    
    DateOfJoining = serializers.DateField(validators=[date_of_joining_restriction])
    EmployeeName = serializers.CharField(max_length=200, validators=[name_validation])

    class Meta:
        model = Employee
        fields = ('EmployeeId', 'EmployeeName', 'Designation', 'DateOfJoining', 
                  'Contact', 'IsActive','DepartmentId','Department')

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = '__all__'
