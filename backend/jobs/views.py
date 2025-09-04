from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from .models import Job
from .serializers import (
    JobSerializer, JobCreateSerializer, JobDetailSerializer, JobListSerializer
)


class IsClientOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow clients to create/edit jobs"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_client
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.client == request.user


class JobListCreateView(generics.ListCreateAPIView):
    """List all jobs or create a new job (clients only)"""
    queryset = Job.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'experience_level', 'client']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'deadline', 'budget_min', 'views_count']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return JobCreateSerializer
        return JobListSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated, IsClientOrReadOnly]
        return [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(client=self.request.user)


class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a job"""
    queryset = Job.objects.all()
    serializer_class = JobDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsClientOrReadOnly]
    
    def retrieve(self, request, *args, **kwargs):
        """Increment view count when job is viewed"""
        instance = self.get_object()
        instance.increment_views()
        return super().retrieve(request, *args, **kwargs)


class ClientJobListView(generics.ListAPIView):
    """List jobs posted by the authenticated client"""
    serializer_class = JobListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Job.objects.filter(client=self.request.user)


class FreelancerJobListView(generics.ListAPIView):
    """List jobs available for freelancers (open jobs only)"""
    serializer_class = JobListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Job.objects.filter(status='open')


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def job_search(request):
    """Advanced job search with filters"""
    queryset = Job.objects.filter(status='open')
    
    # Filter by skills
    skills = request.query_params.getlist('skills')
    if skills:
        queryset = queryset.filter(required_skills__name__in=skills).distinct()
    
    # Filter by budget range
    min_budget = request.query_params.get('min_budget')
    max_budget = request.query_params.get('max_budget')
    if min_budget:
        queryset = queryset.filter(budget_max__gte=min_budget)
    if max_budget:
        queryset = queryset.filter(budget_min__lte=max_budget)
    
    # Filter by experience level
    experience_level = request.query_params.get('experience_level')
    if experience_level:
        queryset = queryset.filter(experience_level=experience_level)
    
    # Filter by deadline
    deadline_before = request.query_params.get('deadline_before')
    if deadline_before:
        from django.utils import timezone
        from datetime import datetime
        try:
            deadline_date = datetime.fromisoformat(deadline_before.replace('Z', '+00:00'))
            queryset = queryset.filter(deadline__lte=deadline_date)
        except ValueError:
            pass
    
    # Ordering
    ordering = request.query_params.get('ordering', '-created_at')
    if ordering in ['created_at', '-created_at', 'deadline', '-deadline', 'budget_min', '-budget_min']:
        queryset = queryset.order_by(ordering)
    
    # Pagination
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 20))
    start = (page - 1) * page_size
    end = start + page_size
    
    jobs = queryset[start:end]
    serializer = JobListSerializer(jobs, many=True)
    
    return Response({
        'results': serializer.data,
        'total': queryset.count(),
        'page': page,
        'page_size': page_size,
        'has_next': end < queryset.count(),
        'has_previous': page > 1
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def toggle_job_featured(request, job_id):
    """Toggle job featured status (clients only)"""
    job = get_object_or_404(Job, id=job_id)
    
    if job.client != request.user:
        return Response(
            {'error': 'You can only modify your own jobs'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    job.is_featured = not job.is_featured
    job.save()
    
    return Response({
        'message': f'Job {"featured" if job.is_featured else "unfeatured"} successfully',
        'is_featured': job.is_featured
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def close_job(request, job_id):
    """Close a job (clients only)"""
    job = get_object_or_404(Job, id=job_id)
    
    if job.client != request.user:
        return Response(
            {'error': 'You can only modify your own jobs'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    if job.status != 'open':
        return Response(
            {'error': 'Only open jobs can be closed'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    job.status = 'cancelled'
    job.save()
    
    return Response({'message': 'Job closed successfully'})
