from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Authentication
    path('auth/register/', views.UserRegistrationView.as_view(), name='register'),
    path('auth/login/', views.UserLoginView.as_view(), name='login'),
    
    # User profile and details
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('user/', views.UserDetailView.as_view(), name='user-detail'),
    
    # Skills
    path('skills/', views.SkillListView.as_view(), name='skill-list'),
    path('user-skills/', views.UserSkillListCreateView.as_view(), name='user-skill-list-create'),
    path('user-skills/<int:pk>/', views.UserSkillDetailView.as_view(), name='user-skill-detail'),
    path('add-skill/', views.add_skill_to_user, name='add-skill'),
    path('remove-skill/<int:skill_id>/', views.remove_skill_from_user, name='remove-skill'),
    
    # Portfolio
    path('portfolio/', views.PortfolioListCreateView.as_view(), name='portfolio-list-create'),
    path('portfolio/<int:pk>/', views.PortfolioDetailView.as_view(), name='portfolio-detail'),
]
