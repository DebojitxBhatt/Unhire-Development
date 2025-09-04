from rest_framework import serializers
from .models import Submission, SubmissionAttachment
from users.serializers import UserSerializer
from jobs.serializers import JobListSerializer
from applications.serializers import ApplicationListSerializer


class SubmissionAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionAttachment
        fields = ['id', 'file', 'filename', 'file_size', 'uploaded_at']
        read_only_fields = ['filename', 'file_size', 'uploaded_at']


class SubmissionSerializer(serializers.ModelSerializer):
    freelancer = UserSerializer(read_only=True)
    job = JobListSerializer(read_only=True)
    application = ApplicationListSerializer(read_only=True)
    attachments = SubmissionAttachmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Submission
        fields = [
            'id', 'job', 'freelancer', 'application', 'submission_type',
            'title', 'description', 'files', 'status', 'submitted_at',
            'updated_at', 'reviewed_at', 'reviewed_by', 'client_feedback',
            'rejection_reason', 'revision_notes', 'deadline', 'is_overdue',
            'attachments'
        ]
        read_only_fields = [
            'id', 'freelancer', 'job', 'application', 'submitted_at',
            'updated_at', 'reviewed_at', 'reviewed_by', 'client_feedback',
            'rejection_reason', 'revision_notes', 'is_overdue'
        ]


class SubmissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = [
            'job', 'application', 'submission_type', 'title', 'description',
            'files', 'deadline'
        ]
    
    def validate(self, attrs):
        """Validate submission data"""
        job = attrs.get('job')
        application = attrs.get('application')
        submission_type = attrs.get('submission_type')
        deadline = attrs.get('deadline')
        
        # Ensure job and application match
        if application.job != job:
            raise serializers.ValidationError("Application must be for the specified job")
        
        # Ensure freelancer owns the application
        request = self.context.get('request')
        if request and application.freelancer != request.user:
            raise serializers.ValidationError("You can only submit for your own applications")
        
        # Ensure application is accepted for final submissions
        if submission_type == 'final' and application.status != 'accepted':
            raise serializers.ValidationError("Can only submit final submission for accepted applications")
        
        # Ensure deadline is in the future
        from django.utils import timezone
        if deadline and deadline <= timezone.now():
            raise serializers.ValidationError("Deadline must be in the future")
        
        # Check if submission already exists for this type
        if Submission.objects.filter(
            job=job, 
            freelancer=request.user, 
            submission_type=submission_type
        ).exists():
            raise serializers.ValidationError(f"You have already submitted a {submission_type} for this job")
        
        return attrs
    
    def create(self, validated_data):
        validated_data['freelancer'] = self.context['request'].user
        return super().create(validated_data)


class SubmissionUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating submission details"""
    class Meta:
        model = Submission
        fields = ['title', 'description', 'files', 'deadline']
    
    def validate(self, attrs):
        """Ensure submission can be updated"""
        instance = self.instance
        
        if instance.status not in ['submitted', 'revision_requested']:
            raise serializers.ValidationError("Only submitted or revision requested submissions can be updated")
        
        return attrs


class SubmissionReviewSerializer(serializers.ModelSerializer):
    """Serializer for client to review submissions"""
    class Meta:
        model = Submission
        fields = ['status', 'client_feedback', 'rejection_reason', 'revision_notes']
    
    def validate(self, attrs):
        """Ensure only valid status changes"""
        instance = self.instance
        new_status = attrs.get('status')
        
        if instance.status not in ['submitted', 'under_review']:
            raise serializers.ValidationError("Only submitted or under review submissions can be reviewed")
        
        if new_status not in ['approved', 'rejected', 'revision_requested']:
            raise serializers.ValidationError("Invalid status change")
        
        if new_status == 'rejected' and not attrs.get('rejection_reason'):
            raise serializers.ValidationError("Rejection reason is required when rejecting a submission")
        
        if new_status == 'revision_requested' and not attrs.get('revision_notes'):
            raise serializers.ValidationError("Revision notes are required when requesting a revision")
        
        return attrs
    
    def update(self, instance, validated_data):
        """Update submission status and trigger appropriate actions"""
        request = self.context.get('request')
        new_status = validated_data.get('status')
        
        if new_status == 'approved':
            instance.approve(request.user)
        elif new_status == 'rejected':
            instance.reject(request.user, validated_data.get('rejection_reason', ''))
        elif new_status == 'revision_requested':
            instance.request_revision(request.user, validated_data.get('revision_notes', ''))
        
        return super().update(instance, validated_data)


class SubmissionListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing submissions"""
    freelancer = serializers.CharField(source='freelancer.email', read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)
    submission_type_display = serializers.CharField(source='get_submission_type_display', read_only=True)
    
    class Meta:
        model = Submission
        fields = [
            'id', 'freelancer', 'job_title', 'submission_type', 'submission_type_display',
            'title', 'status', 'submitted_at', 'deadline', 'is_overdue'
        ]
