from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    # Job CRUD operations
    path('jobs/', views.JobListCreateView.as_view(), name='job-list-create'),
    path('jobs/<int:pk>/', views.JobDetailView.as_view(), name='job-detail'),
    
    # Job listings by user type
    path('jobs/client/', views.ClientJobListView.as_view(), name='client-jobs'),
    path('jobs/freelancer/', views.FreelancerJobListView.as_view(), name='freelancer-jobs'),
    
    # Job search and management
    path('jobs/search/', views.job_search, name='job-search'),
    path('jobs/<int:job_id>/toggle-featured/', views.toggle_job_featured, name='toggle-featured'),
    path('jobs/<int:job_id>/close/', views.close_job, name='close-job'),
]
