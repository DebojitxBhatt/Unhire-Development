from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('freelancer', 'Freelancer'),
        ('admin', 'Admin'),
    ]
    
    username = None  # Disable username field
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    @property
    def is_client(self):
        return self.role == 'client'
    
    @property
    def is_freelancer(self):
        return self.role == 'freelancer'
    
    @property
    def is_admin(self):
        return self.role == 'admin'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    availability_status = models.CharField(
        max_length=20,
        choices=[
            ('available', 'Available'),
            ('busy', 'Busy'),
            ('unavailable', 'Unavailable'),
        ],
        default='available'
    )
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.first_name} {self.last_name}"


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class UserSkill(models.Model):
    PROFICIENCY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES, default='beginner')
    years_experience = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'skill']
    
    def __str__(self):
        return f"{self.user.email} - {self.skill.name} ({self.proficiency})"


class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolio_items')
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='portfolio/')
    url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.title}"
