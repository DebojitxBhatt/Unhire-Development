from django.db import models
from django.conf import settings
from django.utils import timezone


class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    job = models.ForeignKey('jobs.Job', on_delete=models.CASCADE, related_name='applications')
    freelancer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_applications')
    proposal = models.TextField()
    proposed_budget = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_duration = models.PositiveIntegerField(help_text='Estimated duration in days')
    
    # Status and tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='reviewed_applications'
    )
    
    # Client feedback
    client_feedback = models.TextField(blank=True, null=True)
    rejection_reason = models.TextField(blank=True, null=True)
    
    # Additional fields
    is_featured = models.BooleanField(default=False)
    cover_letter = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-applied_at']
        unique_together = ['job', 'freelancer']
    
    def __str__(self):
        return f"{self.freelancer.email} - {self.job.title}"
    
    @property
    def is_pending(self):
        return self.status == 'pending'
    
    @property
    def is_accepted(self):
        return self.status == 'accepted'
    
    @property
    def is_rejected(self):
        return self.status == 'rejected'
    
    @property
    def is_withdrawn(self):
        return self.status == 'withdrawn'
    
    def accept(self, reviewed_by):
        """Accept the application and start the job"""
        self.status = 'accepted'
        self.reviewed_at = timezone.now()
        self.reviewed_by = reviewed_by
        self.save()
        
        # Update job status
        self.job.status = 'in_progress'
        self.job.started_at = timezone.now()
        self.job.save()
    
    def reject(self, reviewed_by, reason=''):
        """Reject the application"""
        self.status = 'rejected'
        self.reviewed_at = timezone.now()
        self.reviewed_by = reviewed_by
        self.rejection_reason = reason
        self.save()
    
    def withdraw(self):
        """Freelancer withdraws the application"""
        self.status = 'withdrawn'
        self.save()
    
    def can_be_accepted(self):
        """Check if application can be accepted"""
        return self.status == 'pending' and self.job.status == 'open'
    
    def can_be_rejected(self):
        """Check if application can be rejected"""
        return self.status == 'pending'
    
    def can_be_withdrawn(self):
        """Check if application can be withdrawn"""
        return self.status == 'pending'
