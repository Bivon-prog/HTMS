from django.urls import path
from . import views

urlpatterns = [
    path('', views.TicketListView.as_view(), name='ticket_list'),
    path('<str:pk>/', views.TicketDetailView.as_view(), name='ticket_detail'),
    path('<str:pk>/status/', views.TicketStatusUpdateView.as_view(), name='ticket_status_update'),
    path('<str:pk>/assign/', views.TicketAssignmentView.as_view(), name='ticket_assignment'),
    path('<str:pk>/escalate/', views.escalate_ticket, name='ticket_escalate'),
    path('<str:ticket_id>/comments/', views.TicketCommentListCreateView.as_view(), name='ticket_comments'),
    path('<str:ticket_id>/attachments/', views.TicketAttachmentListCreateView.as_view(), name='ticket_attachments'),
    path(
        '<str:ticket_id>/attachments/<str:pk>/download/',
        views.ticket_attachment_download,
        name='ticket_attachment_download',
    ),
    path('statistics/', views.ticket_statistics, name='ticket_statistics'),
    path('audit/', views.AuditLogListView.as_view(), name='audit_log'),
    path('audit/export/csv/', views.export_audit_logs_csv, name='audit_export_csv'),
    path('export/csv/', views.export_tickets_csv, name='tickets_export_csv'),
    path('<str:ticket_id>/audit/', views.AuditLogListView.as_view(), name='ticket_audit_log'),
]
