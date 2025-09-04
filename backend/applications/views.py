from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from .models import Application
from .serializers import (
    ApplicationSerializer, ApplicationCreateSerializer, ApplicationUpdateSerializer,
    ApplicationReviewSerializer, ApplicationListSerializer
)


class IsFreelancerOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow freelancers to create/edit applications"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_freelancer
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.freelancer == request.user


class IsClientOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow clients to review applications"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_client
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.job.client == request.user


class ApplicationListCreateView(generics.ListCreateAPIView):
    """List all applications or create a new application (freelancers only)"""
    serializer_class = ApplicationListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'job', 'freelancer']
    search_fields = ['proposal', 'cover_letter']
    ordering_fields = ['applied_at', 'proposed_budget', 'estimated_duration']
    ordering = ['-applied_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ApplicationCreateSerializer
        return ApplicationListSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_client:
            # Clients see applications for their jobs
            return Application.objects.filter(job__client=user)
        elif user.is_freelancer:
            # Freelancers see their own applications
            return Application.objects.filter(freelancer=user)
        else:
            # Admins see all applications
            return Application.objects.all()
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated, IsFreelancerOrReadOnly]
        return [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(freelancer=self.request.user)


class ApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete an application"""
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsFreelancerOrReadOnly]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_client:
            return Application.objects.filter(job__client=user)
        elif user.is_freelancer:
            return Application.objects.filter(freelancer=user)
        else:
            return Application.objects.all()


class ApplicationUpdateView(generics.UpdateAPIView):
    """Update application details (freelancers only)"""
    queryset = Application.objects.all()
    serializer_class = ApplicationUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsFreelancerOrReadOnly]
    
    def get_queryset(self):
        return Application.objects.filter(freelancer=self.request.user)


class ApplicationReviewView(generics.UpdateAPIView):
    """Review application (clients only)"""
    queryset = Application.objects.all()
    serializer_class = ApplicationReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsClientOrReadOnly]
    
    def get_queryset(self):
        return Application.objects.filter(job__client=self.request.user)


class FreelancerApplicationListView(generics.ListAPIView):
    """List applications by the authenticated freelancer"""
    serializer_class = ApplicationListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Application.objects.filter(freelancer=self.request.user)


class ClientApplicationListView(generics.ListAPIView):
    """List applications for jobs posted by the authenticated client"""
    serializer_class = ApplicationListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Application.objects.filter(job__client=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def withdraw_application(request, application_id):
    """Withdraw an application (freelancers only)"""
    application = get_object_or_404(Application, id=application_id)
    
    if application.freelancer != request.user:
        return Response(
            {'error': 'You can only withdraw your own applications'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    if not application.can_be_withdrawn():
        return Response(
            {'error': 'Application cannot be withdrawn'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    application.withdraw()
    return Response({'message': 'Application withdrawn successfully'})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def accept_application(request, application_id):
    """Accept an application (clients only)"""
    application = get_object_or_404(Application, id=application_id)
    
    if application.job.client != request.user:
        return Response(
            {'error': 'You can only accept applications for your own jobs'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    if not application.can_be_accepted():
        return Response(
            {'error': 'Application cannot be accepted'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    application.accept(request.user)
    return Response({'message': 'Application accepted successfully'})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def reject_application(request, application_id):
    """Reject an application (clients only)"""
    application = get_object_or_404(Application, id=application_id)
    rejection_reason = request.data.get('rejection_reason', '')
    
    if application.job.client != request.user:
        return Response(
            {'error': 'You can only reject applications for your own jobs'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    if not application.can_be_rejected():
        return Response(
            {'error': 'Application cannot be rejected'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not rejection_reason:
        return Response(
            {'error': 'Rejection reason is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    application.reject(request.user, rejection_reason)
    return Response({'message': 'Application rejected successfully'})
