from django.urls import path
from . import views

urlpatterns = [
    path('', views.AssetListView.as_view(), name='asset_list'),
    path('<int:pk>/', views.AssetDetailView.as_view(), name='asset_detail'),
    path('<int:asset_id>/history/', views.AssetTicketHistoryListView.as_view(), name='asset_history'),
    path('statistics/', views.asset_statistics, name='asset_statistics'),
    path('search/', views.search_assets, name='search_assets'),
]
