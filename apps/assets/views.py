from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Asset, AssetTicketHistory
from .serializers import AssetSerializer, AssetCreateSerializer, AssetTicketHistorySerializer
from apps.permissions import IsMissionUserOrAdmin


class AssetListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'device_type', 'mission', 'assigned_user']
    search_fields = ['inventory_tag', 'device_type', 'make', 'model']
    ordering_fields = ['inventory_tag', 'device_type', 'created_at']
    ordering = ['inventory_tag']

    def get_queryset(self):
        queryset = Asset.objects.select_related('assigned_user', 'mission')
        
        # Mission isolation for non-HQ users
        if self.request.user.role != 'HQ_Super_Admin':
            queryset = queryset.filter(mission=self.request.user.mission)
        
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AssetCreateSerializer
        return AssetSerializer

    def perform_create(self, serializer):
        serializer.save()


class AssetDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Asset.objects.select_related('assigned_user', 'mission')
    permission_classes = [permissions.IsAuthenticated, IsMissionUserOrAdmin]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AssetCreateSerializer
        return AssetSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Mission isolation for non-HQ users
        if self.request.user.role != 'HQ_Super_Admin':
            queryset = queryset.filter(mission=self.request.user.mission)
        
        return queryset


class AssetTicketHistoryListView(generics.ListAPIView):
    serializer_class = AssetTicketHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        asset_id = self.kwargs['asset_id']
        return AssetTicketHistory.objects.filter(
            asset_id=asset_id,
            asset__mission=self.request.user.mission if self.request.user.role != 'HQ_Super_Admin' else None
        ).select_related('ticket').order_by('-created_at')


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def asset_statistics(request):
    """Get asset statistics for dashboard"""
    queryset = Asset.objects.all()
    
    # Mission isolation for non-HQ users
    if request.user.role != 'HQ_Super_Admin':
        queryset = queryset.filter(mission=request.user.mission)
    
    # Basic statistics
    total_assets = queryset.count()
    active_assets = queryset.filter(status='Active').count()
    maintenance_assets = queryset.filter(status='Maintenance').count()
    retired_assets = queryset.filter(status='Retired').count()
    
    # Warranty statistics
    out_of_warranty = sum(1 for asset in queryset if asset.is_out_of_warranty)
    needs_replacement = sum(1 for asset in queryset if asset.needs_replacement)
    
    # Asset type breakdown
    asset_types = {}
    for asset in queryset:
        asset_types[asset.device_type] = asset_types.get(asset.device_type, 0) + 1
    
    # Unassigned assets
    unassigned_assets = queryset.filter(assigned_user__isnull=True).count()
    
    data = {
        'overview': {
            'total_assets': total_assets,
            'active_assets': active_assets,
            'maintenance_assets': maintenance_assets,
            'retired_assets': retired_assets,
            'unassigned_assets': unassigned_assets,
        },
        'warranty': {
            'out_of_warranty': out_of_warranty,
            'needs_replacement': needs_replacement,
        },
        'by_type': asset_types,
    }
    
    return Response(data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def search_assets(request):
    """Search assets by inventory tag or device name"""
    query = request.query_params.get('q', '').strip()
    
    if not query:
        return Response({'error': 'Search query is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    queryset = Asset.objects.all()
    
    # Mission isolation for non-HQ users
    if request.user.role != 'HQ_Super_Admin':
        queryset = queryset.filter(mission=request.user.mission)
    
    # Search by inventory tag or device type
    assets = queryset.filter(
        inventory_tag__icontains=query
    ).select_related('assigned_user', 'mission')[:10]  # Limit to 10 results
    
    serializer = AssetSerializer(assets, many=True)
    return Response(serializer.data)
