from django.urls import path
from . import views

urlpatterns = [
    path('', views.TicketListView.as_view(), name='ticket_list'),
    path('<int:pk>/', views.TicketDetailView.as_view(), name='ticket_detail'),
    path('<int:pk>/status/', views.TicketStatusUpdateView.as_view(), name='ticket_status_update'),
    path('<int:pk>/assign/', views.TicketAssignmentView.as_view(), name='ticket_assignment'),
    path('<int:pk>/escalate/', views.escalate_ticket, name='ticket_escalate'),
    path('<int:ticket_id>/comments/', views.TicketCommentListCreateView.as_view(), name='ticket_comments'),
    path('<int:ticket_id>/attachments/', views.TicketAttachmentListCreateView.as_view(), name='ticket_attachments'),
    path('statistics/', views.ticket_statistics, name='ticket_statistics'),
    path('audit/', views.AuditLogListView.as_view(), name='audit_log'),
    path('<int:ticket_id>/audit/', views.AuditLogListView.as_view(), name='ticket_audit_log'),
]
