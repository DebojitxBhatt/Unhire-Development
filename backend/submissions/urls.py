from django.urls import path
from . import views

app_name = 'submissions'

urlpatterns = [
    # Submission CRUD operations
    path('submissions/', views.SubmissionListCreateView.as_view(), name='submission-list-create'),
    path('submissions/<int:pk>/', views.SubmissionDetailView.as_view(), name='submission-detail'),
    
    # Submission management
    path('submissions/<int:pk>/update/', views.SubmissionUpdateView.as_view(), name='submission-update'),
    path('submissions/<int:pk>/review/', views.SubmissionReviewView.as_view(), name='submission-review'),
    
    # Submission actions
    path('submissions/<int:submission_id>/approve/', views.approve_submission, name='approve-submission'),
    path('submissions/<int:submission_id>/reject/', views.reject_submission, name='reject-submission'),
    path('submissions/<int:submission_id>/request-revision/', views.request_revision, name='request-revision'),
]
