from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserSerializer(serializers.ModelSerializer):
    mission_name = serializers.CharField(source='mission.name', read_only=True)
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'role', 'department', 'mission', 'mission_name', 'timezone',
            'is_active', 'date_joined', 'last_login', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'username', 'date_joined', 'last_login', 'created_at', 'updated_at']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 'password',
            'password_confirm', 'role', 'department', 'mission', 'timezone'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, validators=[validate_password], required=False)
    new_password_confirm = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'timezone', 'current_password',
            'new_password', 'new_password_confirm'
        ]

    def validate(self, attrs):
        # Password change validation
        if 'new_password' in attrs:
            if not attrs.get('current_password'):
                raise serializers.ValidationError("Current password is required to change password")
            if attrs.get('new_password') != attrs.get('new_password_confirm'):
                raise serializers.ValidationError("New passwords don't match")
            
            # Verify current password
            if not self.instance.check_password(attrs['current_password']):
                raise serializers.ValidationError("Current password is incorrect")
        
        return attrs

    def update(self, instance, validated_data):
        # Handle password change
        if 'new_password' in validated_data:
            instance.set_password(validated_data['new_password'])
            validated_data.pop('new_password')
            validated_data.pop('new_password_confirm')
            validated_data.pop('current_password')

        return super().update(instance, validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Both email and password are required')


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value, is_active=True)
        except User.DoesNotExist:
            # Don't reveal if email exists for security
            pass
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    password = serializers.CharField(validators=[validate_password])
    password_confirm = serializers.CharField()

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
