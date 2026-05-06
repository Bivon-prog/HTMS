from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Mission, HolidayCalendar, TicketCategory
from .serializers import MissionSerializer, HolidayCalendarSerializer, TicketCategorySerializer
from apps.permissions import IsAdminUser


class MissionListView(generics.ListCreateAPIView):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['region', 'status', 'country']
    search_fields = ['name', 'city', 'country']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsAdminUser()]
        return [permissions.IsAuthenticated()]


class MissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]


class HolidayCalendarListView(generics.ListCreateAPIView):
    serializer_class = HolidayCalendarSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['mission', 'is_recurring']
    ordering = ['holiday_date']

    def get_queryset(self):
        queryset = HolidayCalendar.objects.all()
        mission_id = self.request.query_params.get('mission')
        if mission_id:
            queryset = queryset.filter(mission_id=mission_id)
        return queryset

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsAdminUser()]
        return [permissions.IsAuthenticated()]


class HolidayCalendarDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HolidayCalendar.objects.all()
    serializer_class = HolidayCalendarSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]


class TicketCategoryListView(generics.ListCreateAPIView):
    queryset = TicketCategory.objects.all()
    serializer_class = TicketCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering = ['name']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsAdminUser()]
        return [permissions.IsAuthenticated()]


class TicketCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TicketCategory.objects.all()
    serializer_class = TicketCategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def mission_working_hours(request, mission_id):
    """Check if it's currently working hours for a mission"""
    try:
        mission = Mission.objects.get(id=mission_id)
        is_working = mission.is_working_hours()
        
        return Response({
            'mission_id': mission_id,
            'mission_name': mission.name,
            'timezone': str(mission.timezone),
            'is_working_hours': is_working,
            'working_hours': {
                'start': mission.work_start_time,
                'end': mission.work_end_time,
                'week_start': mission.working_week_start,
                'week_end': mission.working_week_end,
            }
        })
    except Mission.DoesNotExist:
        return Response({'error': 'Mission not found'}, status=status.HTTP_404_NOT_FOUND)
