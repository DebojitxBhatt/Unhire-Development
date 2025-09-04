from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Review(models.Model):
    job = models.ForeignKey('jobs.Job', on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_given')
    reviewed_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_received')
    
    # Rating and feedback
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Rating from 1 to 5'
    )
    comment = models.TextField()
    
    # Review type
    review_type = models.CharField(
        max_length=20,
        choices=[
            ('client_to_freelancer', 'Client to Freelancer'),
            ('freelancer_to_client', 'Freelancer to Client'),
        ]
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['job', 'reviewer', 'reviewed_user']
    
    def __str__(self):
        return f"{self.reviewer.email} -> {self.reviewed_user.email} ({self.job.title})"
    
    @property
    def is_client_review(self):
        return self.review_type == 'client_to_freelancer'
    
    @property
    def is_freelancer_review(self):
        return self.review_type == 'freelancer_to_client'
    
    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Ensure reviewer and reviewed_user are different
        if self.reviewer == self.reviewed_user:
            raise ValidationError("Reviewer cannot review themselves")
        
        # Ensure review type matches the reviewer's role
        if self.reviewer.is_client and self.review_type != 'client_to_freelancer':
            raise ValidationError("Clients can only review freelancers")
        
        if self.reviewer.is_freelancer and self.review_type != 'freelancer_to_client':
            raise ValidationError("Freelancers can only review clients")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class ReviewResponse(models.Model):
    review = models.OneToOneField(Review, on_delete=models.CASCADE, related_name='response')
    responder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='review_responses')
    response_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Response to {self.review} by {self.responder.email}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Ensure responder is the reviewed user
        if self.responder != self.review.reviewed_user:
            raise ValidationError("Only the reviewed user can respond to a review")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
