from rest_framework import generics, permissions
from apps.authentication.models import User
from apps.authentication.serializers import UserSerializer
from apps.permissions import IsAdminUser


class UserListView(generics.ListAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    search_fields = ['first_name', 'last_name', 'email']
    ordering = ['first_name', 'last_name']

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Mission isolation for non-HQ users
        if self.request.user.role != 'HQ_Super_Admin':
            queryset = queryset.filter(mission=self.request.user.mission)
        
        return queryset
