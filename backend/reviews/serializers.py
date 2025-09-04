from rest_framework import serializers
from .models import Review, ReviewResponse
from users.serializers import UserSerializer
from jobs.serializers import JobListSerializer


class ReviewResponseSerializer(serializers.ModelSerializer):
    responder = UserSerializer(read_only=True)
    
    class Meta:
        model = ReviewResponse
        fields = ['id', 'responder', 'response_text', 'created_at', 'updated_at']
        read_only_fields = ['id', 'responder', 'created_at', 'updated_at']


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer(read_only=True)
    reviewed_user = UserSerializer(read_only=True)
    job = JobListSerializer(read_only=True)
    response = ReviewResponseSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'job', 'reviewer', 'reviewed_user', 'rating', 'comment',
            'review_type', 'created_at', 'updated_at', 'response'
        ]
        read_only_fields = [
            'id', 'reviewer', 'reviewed_user', 'job', 'created_at', 'updated_at'
        ]


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['job', 'reviewed_user', 'rating', 'comment', 'review_type']
    
    def validate(self, attrs):
        """Validate review data"""
        job = attrs.get('job')
        reviewed_user = attrs.get('reviewed_user')
        review_type = attrs.get('review_type')
        request = self.context.get('request')
        
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("User must be authenticated")
        
        # Ensure reviewer and reviewed_user are different
        if request.user == reviewed_user:
            raise serializers.ValidationError("You cannot review yourself")
        
        # Ensure review type matches the reviewer's role
        if request.user.is_client and review_type != 'client_to_freelancer':
            raise serializers.ValidationError("Clients can only review freelancers")
        
        if request.user.is_freelancer and review_type != 'freelancer_to_client':
            raise serializers.ValidationError("Freelancers can only review clients")
        
        # Ensure job is completed
        if job.status != 'completed':
            raise serializers.ValidationError("Can only review completed jobs")
        
        # Ensure reviewer was involved in the job
        if request.user.is_client and job.client != request.user:
            raise serializers.ValidationError("You can only review jobs you posted")
        
        if request.user.is_freelancer:
            # Check if freelancer was accepted for this job
            if not job.applications.filter(freelancer=request.user, status='accepted').exists():
                raise serializers.ValidationError("You can only review jobs you were accepted for")
        
        # Ensure reviewed_user was involved in the job
        if request.user.is_client:
            # Client reviewing freelancer - check if freelancer was accepted
            if not job.applications.filter(freelancer=reviewed_user, status='accepted').exists():
                raise serializers.ValidationError("Can only review freelancers who were accepted for this job")
        else:
            # Freelancer reviewing client - check if client posted the job
            if job.client != reviewed_user:
                raise serializers.ValidationError("Can only review clients who posted this job")
        
        # Check if review already exists
        if Review.objects.filter(
            job=job, 
            reviewer=request.user, 
            reviewed_user=reviewed_user
        ).exists():
            raise serializers.ValidationError("You have already reviewed this user for this job")
        
        return attrs
    
    def create(self, validated_data):
        validated_data['reviewer'] = self.context['request'].user
        return super().create(validated_data)


class ReviewUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating review details"""
    class Meta:
        model = Review
        fields = ['rating', 'comment']
    
    def validate(self, attrs):
        """Ensure review can be updated"""
        instance = self.instance
        
        # Only allow updates within a short time window (e.g., 24 hours)
        from django.utils import timezone
        from datetime import timedelta
        
        if instance.created_at < timezone.now() - timedelta(hours=24):
            raise serializers.ValidationError("Reviews can only be updated within 24 hours of creation")
        
        return attrs


class ReviewResponseCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating review responses"""
    class Meta:
        model = ReviewResponse
        fields = ['response_text']
    
    def validate(self, attrs):
        """Validate response data"""
        review = self.context.get('review')
        request = self.context.get('request')
        
        if not review or not request:
            raise serializers.ValidationError("Invalid context")
        
        # Ensure responder is the reviewed user
        if review.reviewed_user != request.user:
            raise serializers.ValidationError("Only the reviewed user can respond to a review")
        
        # Check if response already exists
        if hasattr(review, 'response'):
            raise serializers.ValidationError("You have already responded to this review")
        
        return attrs
    
    def create(self, validated_data):
        validated_data['responder'] = self.context['request'].user
        validated_data['review'] = self.context['review']
        return super().create(validated_data)


class ReviewListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing reviews"""
    reviewer = serializers.CharField(source='reviewer.email', read_only=True)
    reviewed_user = serializers.CharField(source='reviewed_user.email', read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)
    review_type_display = serializers.CharField(source='get_review_type_display', read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'reviewer', 'reviewed_user', 'job_title', 'rating', 'comment',
            'review_type', 'review_type_display', 'created_at'
        ]
