from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class Warning(models.Model):
    WARNING_TYPE_CHOICES = [
        ('missed_deadline', 'Missed Deadline'),
        ('rejected_submission', 'Rejected Final Submission'),
        ('poor_quality', 'Poor Quality Work'),
        ('communication_issue', 'Communication Issue'),
        ('other', 'Other'),
    ]
    
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    freelancer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='warnings')
    issued_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='warnings_issued'
    )
    
    # Warning details
    warning_type = models.CharField(max_length=30, choices=WARNING_TYPE_CHOICES)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='medium')
    description = models.TextField()
    evidence = models.TextField(blank=True, null=True)
    
    # Related objects
    job = models.ForeignKey('jobs.Job', on_delete=models.CASCADE, related_name='warnings', blank=True, null=True)
    submission = models.ForeignKey('submissions.Submission', on_delete=models.CASCADE, related_name='warnings', blank=True, null=True)
    
    # Timestamps
    issued_at = models.DateTimeField(auto_now_add=True)
    acknowledged_at = models.DateTimeField(blank=True, null=True)
    acknowledged_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='warnings_acknowledged'
    )
    
    # Status
    is_acknowledged = models.BooleanField(default=False)
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(blank=True, null=True)
    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='warnings_resolved'
    )
    
    class Meta:
        ordering = ['-issued_at']
    
    def __str__(self):
        return f"{self.freelancer.email} - {self.warning_type} ({self.severity})"
    
    @property
    def warning_count(self):
        """Get total warning count for this freelancer"""
        return Warning.objects.filter(
            freelancer=self.freelancer,
            is_resolved=False
        ).count()
    
    @property
    def is_third_strike(self):
        """Check if this is the third strike"""
        return self.warning_count >= 3
    
    def acknowledge(self, acknowledged_by):
        """Mark warning as acknowledged"""
        self.is_acknowledged = True
        self.acknowledged_at = timezone.now()
        self.acknowledged_by = acknowledged_by
        self.save()
    
    def resolve(self, resolved_by):
        """Mark warning as resolved"""
        self.is_resolved = True
        self.resolved_at = timezone.now()
        self.resolved_by = resolved_by
        self.save()
    
    def can_be_acknowledged(self):
        """Check if warning can be acknowledged"""
        return not self.is_acknowledged
    
    def can_be_resolved(self):
        """Check if warning can be resolved"""
        return self.is_acknowledged and not self.is_resolved


class WarningTemplate(models.Model):
    """Template for common warning types"""
    warning_type = models.CharField(max_length=30, choices=Warning.WARNING_TYPE_CHOICES)
    severity = models.CharField(max_length=20, choices=Warning.SEVERITY_CHOICES)
    title = models.CharField(max_length=200)
    description_template = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} ({self.warning_type})"


@receiver(post_save, sender=Warning)
def check_warning_limit(sender, instance, created, **kwargs):
    """Check if freelancer should be banned after 3 warnings"""
    if created and instance.freelancer.is_freelancer:
        warning_count = Warning.objects.filter(
            freelancer=instance.freelancer,
            is_resolved=False
        ).count()
        
        if warning_count >= 3:
            # Ban the freelancer
            instance.freelancer.is_active = False
            instance.freelancer.save()
            
            # Create a system warning about the ban
            Warning.objects.create(
                freelancer=instance.freelancer,
                warning_type='other',
                severity='critical',
                description=f'Account automatically banned after receiving {warning_count} warnings.',
                evidence=f'Automatic ban triggered at {timezone.now()}',
                issued_by=None  # System warning
            )
