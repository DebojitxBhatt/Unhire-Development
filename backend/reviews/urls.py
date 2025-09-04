from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    # Review CRUD operations
    path('reviews/', views.ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
    
    # Review responses
    path('reviews/<int:review_id>/respond/', views.ReviewResponseView.as_view(), name='review-response'),
    
    # Review listings
    path('reviews/user/<int:user_id>/', views.UserReviewsView.as_view(), name='user-reviews'),
    path('reviews/job/<int:job_id>/', views.JobReviewsView.as_view(), name='job-reviews'),
]
