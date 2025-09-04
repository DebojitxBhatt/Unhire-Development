from rest_framework import serializers
from .models import Application
from users.serializers import UserSerializer
from jobs.serializers import JobListSerializer


class ApplicationSerializer(serializers.ModelSerializer):
    freelancer = UserSerializer(read_only=True)
    job = JobListSerializer(read_only=True)
    
    class Meta:
        model = Application
        fields = [
            'id', 'job', 'freelancer', 'proposal', 'proposed_budget',
            'estimated_duration', 'status', 'applied_at', 'updated_at',
            'reviewed_at', 'reviewed_by', 'client_feedback', 'rejection_reason',
            'is_featured', 'cover_letter'
        ]
        read_only_fields = [
            'id', 'freelancer', 'job', 'applied_at', 'updated_at',
            'reviewed_at', 'reviewed_by', 'client_feedback', 'rejection_reason'
        ]


class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            'job', 'proposal', 'proposed_budget', 'estimated_duration',
            'cover_letter'
        ]
    
    def validate_job(self, value):
        """Ensure job is open and freelancer hasn't already applied"""
        if value.status != 'open':
            raise serializers.ValidationError("Can only apply to open jobs")
        
        # Check if freelancer has already applied
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            if Application.objects.filter(job=value, freelancer=request.user).exists():
                raise serializers.ValidationError("You have already applied to this job")
        
        return value
    
    def validate_proposed_budget(self, value):
        """Ensure proposed budget is within job budget range"""
        job = self.context.get('job')
        if job:
            if value < job.budget_min or value > job.budget_max:
                raise serializers.ValidationError(
                    f"Proposed budget must be between ${job.budget_min} and ${job.budget_max}"
                )
        return value
    
    def create(self, validated_data):
        validated_data['freelancer'] = self.context['request'].user
        return super().create(validated_data)


class ApplicationUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating application (freelancer only)"""
    class Meta:
        model = Application
        fields = ['proposal', 'proposed_budget', 'estimated_duration', 'cover_letter']
    
    def validate(self, attrs):
        """Ensure application can be updated"""
        instance = self.instance
        if instance.status != 'pending':
            raise serializers.ValidationError("Only pending applications can be updated")
        return attrs


class ApplicationReviewSerializer(serializers.ModelSerializer):
    """Serializer for client to review applications"""
    class Meta:
        model = Application
        fields = ['status', 'client_feedback', 'rejection_reason']
    
    def validate(self, attrs):
        """Ensure only valid status changes"""
        instance = self.instance
        new_status = attrs.get('status')
        
        if instance.status != 'pending':
            raise serializers.ValidationError("Only pending applications can be reviewed")
        
        if new_status not in ['accepted', 'rejected']:
            raise serializers.ValidationError("Invalid status change")
        
        if new_status == 'rejected' and not attrs.get('rejection_reason'):
            raise serializers.ValidationError("Rejection reason is required when rejecting an application")
        
        return attrs
    
    def update(self, instance, validated_data):
        """Update application status and trigger job status change if accepted"""
        request = self.context.get('request')
        if request and validated_data.get('status') == 'accepted':
            instance.accept(request.user)
        elif request and validated_data.get('status') == 'rejected':
            instance.reject(request.user, validated_data.get('rejection_reason', ''))
        
        return super().update(instance, validated_data)


class ApplicationListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing applications"""
    freelancer = serializers.CharField(source='freelancer.email', read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)
    
    class Meta:
        model = Application
        fields = [
            'id', 'freelancer', 'job_title', 'proposed_budget', 'estimated_duration',
            'status', 'applied_at', 'is_featured'
        ]
