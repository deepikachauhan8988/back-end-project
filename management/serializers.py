# serializers.py

from rest_framework import serializers
from .models import Employee
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken


class EmployeeRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Employee
        fields = ['name', 'email', 'password', 'confirm_password']

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        return super().create(validated_data)


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }


class EmployeeLoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):

        email = data.get("email")
        password = data.get("password")

        try:
            employee = Employee.objects.get(email=email)

        except Employee.DoesNotExist:
            raise serializers.ValidationError("Invalid Email")

        # Check Password
        if not check_password(password, employee.password):
            raise serializers.ValidationError("Invalid Password")

        # Generate JWT Token
        refresh = RefreshToken.for_user(employee)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['employee'] = employee

        return data