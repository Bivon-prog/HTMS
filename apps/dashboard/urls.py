from django.urls import path
from . import views

urlpatterns = [
    path('overview/', views.dashboard_overview, name='dashboard_overview'),
    path('missions/', views.mission_statistics, name='mission_statistics'),
    path('trends/', views.ticket_trends, name='ticket_trends'),
    path('agents/', views.agent_performance, name='agent_performance'),
]
