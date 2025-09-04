from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from .models import Submission, SubmissionAttachment
from .serializers import (
    SubmissionSerializer, SubmissionCreateSerializer, SubmissionUpdateSerializer,
    SubmissionReviewSerializer, SubmissionListSerializer, SubmissionAttachmentSerializer
)


class IsFreelancerOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow freelancers to create/edit submissions"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_freelancer
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.freelancer == request.user


class IsClientOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow clients to review submissions"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_client
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.job.client == request.user


class SubmissionListCreateView(generics.ListCreateAPIView):
    """List all submissions or create a new submission (freelancers only)"""
    serializer_class = SubmissionListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'submission_type', 'job', 'freelancer']
    search_fields = ['title', 'description']
    ordering_fields = ['submitted_at', 'deadline']
    ordering = ['-submitted_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SubmissionCreateSerializer
        return SubmissionListSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_client:
            # Clients see submissions for their jobs
            return Submission.objects.filter(job__client=user)
        elif user.is_freelancer:
            # Freelancers see their own submissions
            return Submission.objects.filter(freelancer=user)
        else:
            # Admins see all submissions
            return Submission.objects.all()
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated, IsFreelancerOrReadOnly]
        return [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(freelancer=self.request.user)


class SubmissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a submission"""
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated, IsFreelancerOrReadOnly]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_client:
            return Submission.objects.filter(job__client=user)
        elif user.is_freelancer:
            return Submission.objects.filter(freelancer=user)
        else:
            return Submission.objects.all()


class SubmissionUpdateView(generics.UpdateAPIView):
    """Update submission details (freelancers only)"""
    queryset = Submission.objects.all()
    serializer_class = SubmissionUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsFreelancerOrReadOnly]
    
    def get_queryset(self):
        return Submission.objects.filter(freelancer=self.request.user)


class SubmissionReviewView(generics.UpdateAPIView):
    """Review submission (clients only)"""
    queryset = Submission.objects.all()
    serializer_class = SubmissionReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsClientOrReadOnly]
    
    def get_queryset(self):
        return Submission.objects.filter(job__client=self.request.user)


class FreelancerSubmissionListView(generics.ListAPIView):
    """List submissions by the authenticated freelancer"""
    serializer_class = SubmissionListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Submission.objects.filter(freelancer=self.request.user)


class ClientSubmissionListView(generics.ListAPIView):
    """List submissions for jobs posted by the authenticated client"""
    serializer_class = SubmissionListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Submission.objects.filter(job__client=self.request.user)


class SubmissionAttachmentView(generics.CreateAPIView):
    """Add attachments to a submission"""
    serializer_class = SubmissionAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsFreelancerOrReadOnly]
    
    def perform_create(self, serializer):
        submission_id = self.kwargs.get('submission_id')
        submission = get_object_or_404(Submission, id=submission_id, freelancer=self.request.user)
        serializer.save(submission=submission)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def approve_submission(request, submission_id):
    """Approve a submission (clients only)"""
    submission = get_object_or_404(Submission, id=submission_id)
    
    if submission.job.client != request.user:
        return Response(
            {'error': 'You can only approve submissions for your own jobs'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    if not submission.can_be_approved():
        return Response(
            {'error': 'Submission cannot be approved'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    submission.approve(request.user)
    return Response({'message': 'Submission approved successfully'})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def reject_submission(request, submission_id):
    """Reject a submission (clients only)"""
    submission = get_object_or_404(Submission, id=submission_id)
    rejection_reason = request.data.get('rejection_reason', '')
    
    if submission.job.client != request.user:
        return Response(
            {'error': 'You can only reject submissions for your own jobs'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    if not submission.can_be_rejected():
        return Response(
            {'error': 'Submission cannot be rejected'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not rejection_reason:
        return Response(
            {'error': 'Rejection reason is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    submission.reject(request.user, rejection_reason)
    return Response({'message': 'Submission rejected successfully'})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def request_revision(request, submission_id):
    """Request revision of a submission (clients only)"""
    submission = get_object_or_404(Submission, id=submission_id)
    revision_notes = request.data.get('revision_notes', '')
    
    if submission.job.client != request.user:
        return Response(
            {'error': 'You can only request revisions for your own jobs'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    if not submission.can_request_revision():
        return Response(
            {'error': 'Revision cannot be requested'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not revision_notes:
        return Response(
            {'error': 'Revision notes are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    submission.request_revision(request.user, revision_notes)
    return Response({'message': 'Revision requested successfully'})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def submission_deadlines(request):
    """Get upcoming submission deadlines for the authenticated user"""
    user = request.user
    
    if user.is_freelancer:
        submissions = Submission.objects.filter(
            freelancer=user,
            status__in=['submitted', 'under_review', 'revision_requested']
        ).order_by('deadline')
    elif user.is_client:
        submissions = Submission.objects.filter(
            job__client=user,
            status__in=['submitted', 'under_review', 'revision_requested']
        ).order_by('deadline')
    else:
        submissions = Submission.objects.filter(
            status__in=['submitted', 'under_review', 'revision_requested']
        ).order_by('deadline')
    
    serializer = SubmissionListSerializer(submissions, many=True)
    return Response(serializer.data)
