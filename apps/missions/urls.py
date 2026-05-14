from django.urls import path

from . import views

urlpatterns = [
    path('', views.MissionListView.as_view(), name='mission_list'),
    path('<int:pk>/', views.MissionDetailView.as_view(), name='mission_detail'),
    path('categories/', views.ticket_categories, name='ticket_categories'),
    path('holidays/', views.mission_holidays, name='mission_holidays'),
]
