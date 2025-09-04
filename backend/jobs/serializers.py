from rest_framework import serializers
from .models import Job, JobAttachment
from users.serializers import UserSerializer


class JobAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobAttachment
        fields = ['id', 'file', 'filename', 'file_size', 'uploaded_at']
        read_only_fields = ['filename', 'file_size', 'uploaded_at']


class JobSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)
    required_skills = serializers.SlugRelatedField(
        many=True, 
        read_only=True, 
        slug_field='name'
    )
    applications_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'client', 'budget_min', 'budget_max',
            'deadline', 'status', 'priority', 'required_skills', 'experience_level',
            'attachments', 'created_at', 'updated_at', 'started_at', 'completed_at',
            'is_featured', 'views_count', 'applications_count'
        ]
        read_only_fields = [
            'id', 'client', 'created_at', 'updated_at', 'started_at', 
            'completed_at', 'views_count', 'applications_count'
        ]
    
    def get_applications_count(self, obj):
        return obj.applications.count()
    
    def validate_deadline(self, value):
        """Ensure deadline is in the future"""
        from django.utils import timezone
        if value <= timezone.now():
            raise serializers.ValidationError("Deadline must be in the future")
        return value
    
    def validate_budget(self, attrs):
        """Ensure budget_min <= budget_max"""
        budget_min = attrs.get('budget_min')
        budget_max = attrs.get('budget_max')
        
        if budget_min and budget_max and budget_min > budget_max:
            raise serializers.ValidationError("Minimum budget cannot be greater than maximum budget")
        
        return attrs


class JobCreateSerializer(serializers.ModelSerializer):
    required_skills = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        write_only=True
    )
    
    class Meta:
        model = Job
        fields = [
            'title', 'description', 'budget_min', 'budget_max', 'deadline',
            'priority', 'required_skills', 'experience_level', 'attachments'
        ]
    
    def create(self, validated_data):
        required_skills_ids = validated_data.pop('required_skills', [])
        validated_data['client'] = self.context['request'].user
        
        # Create the job first
        job = super().create(validated_data)
        
        # Add required skills if provided
        if required_skills_ids:
            from users.models import Skill
            skills = Skill.objects.filter(id__in=required_skills_ids)
            job.required_skills.set(skills)
        
        return job


class JobDetailSerializer(JobSerializer):
    """Detailed job serializer with full information"""
    client = UserSerializer(read_only=True)
    required_skills = serializers.SlugRelatedField(
        many=True, 
        read_only=True, 
        slug_field='name'
    )
    
    class Meta(JobSerializer.Meta):
        fields = JobSerializer.Meta.fields + ['budget_range', 'is_overdue']


class JobListSerializer(serializers.ModelSerializer):
    """Simplified job serializer for list views"""
    client = serializers.CharField(source='client.email', read_only=True)
    budget_range = serializers.CharField(read_only=True)
    applications_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'client', 'budget_range', 'deadline', 'status',
            'priority', 'experience_level', 'created_at', 'is_featured',
            'views_count', 'applications_count'
        ]
    
    def get_applications_count(self, obj):
        return obj.applications.count()
