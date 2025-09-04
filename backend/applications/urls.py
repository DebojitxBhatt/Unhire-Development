from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    # Application CRUD operations
    path('applications/', views.ApplicationListCreateView.as_view(), name='application-list-create'),
    path('applications/<int:pk>/', views.ApplicationDetailView.as_view(), name='application-detail'),
    
    # Application management
    path('applications/<int:pk>/update/', views.ApplicationUpdateView.as_view(), name='application-update'),
    path('applications/<int:pk>/review/', views.ApplicationReviewView.as_view(), name='application-review'),
    
    # Application listings by user type
    path('applications/freelancer/', views.FreelancerApplicationListView.as_view(), name='freelancer-applications'),
    path('applications/client/', views.ClientApplicationListView.as_view(), name='client-applications'),
    
    # Application actions
    path('applications/<int:application_id>/withdraw/', views.withdraw_application, name='withdraw-application'),
    path('applications/<int:application_id>/accept/', views.accept_application, name='accept-application'),
    path('applications/<int:application_id>/reject/', views.reject_application, name='reject-application'),
]
