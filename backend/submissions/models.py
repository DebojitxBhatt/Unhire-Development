from django.db import models
from django.conf import settings
from django.utils import timezone


class Submission(models.Model):
    SUBMISSION_TYPE_CHOICES = [
        ('draft', 'Draft'),
        ('final', 'Final'),
    ]
    
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('revision_requested', 'Revision Requested'),
    ]
    
    job = models.ForeignKey('jobs.Job', on_delete=models.CASCADE, related_name='submissions')
    freelancer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submissions')
    application = models.ForeignKey('applications.Application', on_delete=models.CASCADE, related_name='submissions')
    
    # Submission details
    submission_type = models.CharField(max_length=20, choices=SUBMISSION_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    files = models.FileField(upload_to='submissions/')
    
    # Status and tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='reviewed_submissions'
    )
    
    # Client feedback
    client_feedback = models.TextField(blank=True, null=True)
    rejection_reason = models.TextField(blank=True, null=True)
    revision_notes = models.TextField(blank=True, null=True)
    
    # Deadline tracking
    deadline = models.DateTimeField()
    is_overdue = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-submitted_at']
        unique_together = ['job', 'freelancer', 'submission_type']
    
    def __str__(self):
        return f"{self.freelancer.email} - {self.job.title} - {self.submission_type}"
    
    def save(self, *args, **kwargs):
        # Check if submission is overdue
        if self.deadline and timezone.now() > self.deadline:
            self.is_overdue = True
        super().save(*args, **kwargs)
    
    @property
    def is_draft(self):
        return self.submission_type == 'draft'
    
    @property
    def is_final(self):
        return self.submission_type == 'final'
    
    @property
    def is_approved(self):
        return self.status == 'approved'
    
    @property
    def is_rejected(self):
        return self.status == 'rejected'
    
    @property
    def is_revision_requested(self):
        return self.status == 'revision_requested'
    
    def approve(self, reviewed_by):
        """Approve the submission"""
        self.status = 'approved'
        self.reviewed_at = timezone.now()
        self.reviewed_by = reviewed_by
        self.save()
        
        # If this is a draft approval, update application status
        if self.is_draft:
            self.application.status = 'accepted'
            self.application.save()
    
    def reject(self, reviewed_by, reason=''):
        """Reject the submission"""
        self.status = 'rejected'
        self.reviewed_at = timezone.now()
        self.reviewed_by = reviewed_by
        self.rejection_reason = reason
        self.save()
    
    def request_revision(self, reviewed_by, notes=''):
        """Request revision of the submission"""
        self.status = 'revision_requested'
        self.reviewed_at = timezone.now()
        self.reviewed_by = reviewed_by
        self.revision_notes = notes
        self.save()
    
    def can_be_approved(self):
        """Check if submission can be approved"""
        return self.status in ['submitted', 'under_review']
    
    def can_be_rejected(self):
        """Check if submission can be rejected"""
        return self.status in ['submitted', 'under_review']
    
    def can_request_revision(self):
        """Check if revision can be requested"""
        return self.status in ['submitted', 'under_review']


class SubmissionAttachment(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='submission_attachments/')
    filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.submission} - {self.filename}"
    
    def save(self, *args, **kwargs):
        if not self.filename:
            self.filename = self.file.name.split('/')[-1]
        if not self.file_size:
            self.file_size = self.file.size
        super().save(*args, **kwargs)
