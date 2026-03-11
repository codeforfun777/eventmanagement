from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('events/', views.event_list, name='event-list'),
    path('categories/', views.manage_category, name='category-list'),
    path('categories/edit/<int:pk>/', views.manage_category, name='category-update'),
    path('categories/delete/<int:pk>/', views.delete_category, name='category-delete'),
    path('events/new/', views.manage_event, name='event-create'),
    path('events/<int:pk>/edit/', views.manage_event, name='event-update'),
    path('events/<int:pk>/delete/', views.delete_event, name='event-delete'),
    path('register/', views.register_participant, name='participant-register'),
]