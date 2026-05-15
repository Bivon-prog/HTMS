from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.permissions import IsHQSuperAdmin

from .models import Mission, TicketCategory
from .serializers import MissionSerializer, TicketCategorySerializer


from django.db.models import Case, When, Value, IntegerField

class MissionListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MissionSerializer
    pagination_class = None
    filterset_fields = ['region', 'status']
    search_fields = ['name', 'city', 'country']

    def get_queryset(self):
        return Mission.objects.annotate(
            hq_order=Case(
                When(name='Ministry Headquarters', then=Value(1)),
                When(name='316 UPPERHILL', then=Value(2)),
                default=Value(3),
                output_field=IntegerField(),
            )
        ).order_by('hq_order', 'name')


class MissionDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def ticket_categories(request):
    qs = TicketCategory.objects.all().order_by('name')
    return Response(TicketCategorySerializer(qs, many=True).data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsHQSuperAdmin])
def mission_holidays(request):
    """Placeholder list; extend with CRUD as needed (SRS 4.1)."""
    from .models import HolidayCalendar

    qs = HolidayCalendar.objects.select_related('mission').all().order_by('holiday_date')[:500]
    data = [
        {
            'id': h.id,
            'mission_id': h.mission_id,
            'mission_name': h.mission.name,
            'holiday_date': h.holiday_date,
            'holiday_name': h.holiday_name,
        }
        for h in qs
    ]
    return Response(data)
