
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Incident,User
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'address', 'pin_code', 'city', 'country', 'password', 'password_confirm', 'enterprise_or_government']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Passwords must match."})
        return data

    def create(self, validated_data):
        # Remove the password_confirm field
        validated_data.pop('password_confirm', None)
        
        # Extract password and create the user
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = ['id', 'incident_id', 'enterprise_or_government', 'reporter_name', 'incident_details', 'reported_datetime', 'priority', 'status']
        read_only_fields = ['incident_id', 'reported_datetime']

    def create(self, validated_data):
        # The `reporter` field should be set in `perform_create` in the view
        return super().create(validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User is deactivated.")
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")
        data['user'] = user
        return data