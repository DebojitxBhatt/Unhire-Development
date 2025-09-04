from django.db import models
from django.conf import settings
from django.utils import timezone


class Job(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posted_jobs')
    budget_min = models.DecimalField(max_digits=10, decimal_places=2)
    budget_max = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    # Requirements and skills
    required_skills = models.ManyToManyField('users.Skill', blank=True, related_name='required_for_jobs')
    experience_level = models.CharField(
        max_length=20,
        choices=[
            ('entry', 'Entry Level'),
            ('intermediate', 'Intermediate'),
            ('senior', 'Senior'),
            ('expert', 'Expert'),
        ],
        default='intermediate'
    )
    
    # Attachments
    attachments = models.FileField(upload_to='job_attachments/', blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    # Additional fields
    is_featured = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.client.email}"
    
    @property
    def is_open(self):
        return self.status == 'open'
    
    @property
    def is_in_progress(self):
        return self.status == 'in_progress'
    
    @property
    def is_completed(self):
        return self.status == 'completed'
    
    @property
    def is_overdue(self):
        return self.deadline < timezone.now() and self.status not in ['completed', 'cancelled']
    
    @property
    def budget_range(self):
        if self.budget_min == self.budget_max:
            return f"${self.budget_min}"
        return f"${self.budget_min} - ${self.budget_max}"
    
    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])


class JobAttachment(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_attachments')
    file = models.FileField(upload_to='job_attachments/')
    filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.job.title} - {self.filename}"
    
    def save(self, *args, **kwargs):
        if not self.filename:
            self.filename = self.file.name.split('/')[-1]
        if not self.file_size:
            self.file_size = self.file.size
        super().save(*args, **kwargs)
