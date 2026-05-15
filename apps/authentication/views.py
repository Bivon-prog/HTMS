import logging
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import OnBehalfOfGrant, User
from .serializers import (
    LoginSerializer,
    OnBehalfOfGrantSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    UserCreateSerializer,
    UserSerializer,
    UserUpdateSerializer,
)
from apps.permissions import IsAdminUser, IsOwnerOrAdmin, IsHQSuperAdmin

logger = logging.getLogger(__name__)


class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        return UserSerializer if self.request.method == 'GET' else UserUpdateSerializer


class UserListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    filterset_fields = ['role', 'department', 'mission']
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = ['first_name', 'last_name', 'date_joined']
    ordering = ['first_name', 'last_name']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsHQSuperAdmin()]
        return [permissions.IsAuthenticated(), IsAdminUser()]

    def get_serializer_class(self):
        return UserCreateSerializer if self.request.method == 'POST' else UserSerializer

    def get_queryset(self):
        qs = User.objects.filter(is_active=True)
        user = self.request.user
        if user.role != 'HQ_Super_Admin':
            qs = qs.filter(mission=user.mission)
        if user.role == 'Mission_Admin':
            qs = qs.exclude(role__in=['Mission_Admin', 'HQ_Super_Admin'])
        return qs

    def perform_create(self, serializer):
        if self.request.user.role == 'Mission_Admin':
            serializer.save(mission=self.request.user.mission)
        else:
            serializer.save()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_serializer_class(self):
        return UserUpdateSerializer if self.request.method in ['PUT', 'PATCH'] else UserSerializer

    def get_queryset(self):
        return User.objects.filter(is_active=True)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(update_fields=['is_active'])


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        user.last_login = timezone.now()
        user.last_login_ip = request.META.get('REMOTE_ADDR')
        user.save(update_fields=['last_login', 'last_login_ip'])

        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Login successful',
            'token': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            },
            'user': UserSerializer(user).data,
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def logout_view(request):
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({'message': 'Logout successful'})
    except Exception:
        return Response({'message': 'Logout completed'})


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def password_reset_request(request):
    serializer = PasswordResetRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    email = serializer.validated_data['email']
    try:
        user = User.objects.get(email=email, is_active=True)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = f"{request.data.get('frontend_url', 'http://localhost:3000')}/reset-password/{uid}/{token}/"

        send_mail(
            subject='HTMS — Password Reset Request',
            message=(
                f'Hello {user.first_name},\n\n'
                f'You requested a password reset for your HTMS account.\n\n'
                f'Click the link below to reset your password (valid for 24 hours):\n{reset_url}\n\n'
                f'If you did not request this, please ignore this email.\n\n'
                f'Ministry of Foreign and Diaspora Affairs, Kenya'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True,
        )
        logger.info(f'Password reset email sent to {email}')
    except User.DoesNotExist:
        pass  # Don't reveal whether the email exists

    # Always return success to prevent email enumeration
    return Response({'message': 'If the email exists, a reset link has been sent.'})


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def password_reset_confirm(request):
    serializer = PasswordResetConfirmSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    uid = serializer.validated_data['uid']
    token = serializer.validated_data['token']
    password = serializer.validated_data['password']

    try:
        user_id = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=user_id, is_active=True)
    except (User.DoesNotExist, ValueError, TypeError):
        return Response({'error': 'Invalid reset link'}, status=status.HTTP_400_BAD_REQUEST)

    if not default_token_generator.check_token(user, token):
        return Response({'error': 'Reset link is invalid or has expired'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(password)
    user.save(update_fields=['password'])
    logger.info(f'Password reset completed for {user.email}')
    return Response({'message': 'Password reset successful. You can now log in.'})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def verify_token(request):
    """Verify JWT token and return current user info."""
    return Response({
        'valid': True,
        'user': UserSerializer(request.user).data,
    })


class OnBehalfOfGrantListCreateView(generics.ListCreateAPIView):
    serializer_class = OnBehalfOfGrantSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        qs = OnBehalfOfGrant.objects.select_related('mission', 'assistant', 'official').order_by('-created_at')
        user = self.request.user
        if user.role == 'HQ_Super_Admin':
            return qs
        if user.role == 'Mission_Admin':
            return qs.filter(mission=user.mission)
        return qs.filter(assistant=user, is_active=True)
