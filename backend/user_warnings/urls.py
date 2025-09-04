from django.urls import path
from . import views

app_name = 'user_warnings'

urlpatterns = [
    # Warning CRUD operations
    path('warnings/', views.WarningListCreateView.as_view(), name='warning-list-create'),
    path('warnings/<int:pk>/', views.WarningDetailView.as_view(), name='warning-detail'),
    
    # Warning management
    path('warnings/<int:warning_id>/acknowledge/', views.acknowledge_warning, name='acknowledge-warning'),
    path('warnings/<int:warning_id>/resolve/', views.resolve_warning, name='resolve-warning'),
    
    # Warning templates
    path('warning-templates/', views.WarningTemplateListView.as_view(), name='warning-template-list'),
]
