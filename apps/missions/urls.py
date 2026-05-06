from django.urls import path
from . import views

urlpatterns = [
    path('', views.MissionListView.as_view(), name='mission_list'),
    path('<int:pk>/', views.MissionDetailView.as_view(), name='mission_detail'),
    path('<int:mission_id>/working-hours/', views.mission_working_hours, name='mission_working_hours'),
    path('holidays/', views.HolidayCalendarListView.as_view(), name='holiday_list'),
    path('holidays/<int:pk>/', views.HolidayCalendarDetailView.as_view(), name='holiday_detail'),
    path('categories/', views.TicketCategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', views.TicketCategoryDetailView.as_view(), name='category_detail'),
]
