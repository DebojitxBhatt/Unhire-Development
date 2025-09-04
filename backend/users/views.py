from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import Profile, Skill, UserSkill, Portfolio
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserSerializer,
    ProfileSerializer, SkillSerializer, UserSkillSerializer,
    PortfolioSerializer, UserDetailSerializer
)

User = get_user_model()


class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'User registered successfully',
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Login successful',
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)


class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class SkillListView(generics.ListAPIView):
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Skill.objects.all()


class UserSkillListCreateView(generics.ListCreateAPIView):
    serializer_class = UserSkillSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserSkill.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserSkillDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSkillSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserSkill.objects.filter(user=self.request.user)


class PortfolioListCreateView(generics.ListCreateAPIView):
    serializer_class = PortfolioSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PortfolioDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PortfolioSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_skill_to_user(request):
    """Add a skill to user's skill set"""
    skill_id = request.data.get('skill_id')
    proficiency = request.data.get('proficiency', 'beginner')
    years_experience = request.data.get('years_experience', 0)
    
    if not skill_id:
        return Response({'error': 'skill_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    skill = get_object_or_404(Skill, id=skill_id)
    
    # Check if user already has this skill
    user_skill, created = UserSkill.objects.get_or_create(
        user=request.user,
        skill=skill,
        defaults={
            'proficiency': proficiency,
            'years_experience': years_experience
        }
    )
    
    if not created:
        # Update existing skill
        user_skill.proficiency = proficiency
        user_skill.years_experience = years_experience
        user_skill.save()
    
    serializer = UserSkillSerializer(user_skill)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def remove_skill_from_user(request, skill_id):
    """Remove a skill from user's skill set"""
    try:
        user_skill = UserSkill.objects.get(user=request.user, skill_id=skill_id)
        user_skill.delete()
        return Response({'message': 'Skill removed successfully'}, status=status.HTTP_200_OK)
    except UserSkill.DoesNotExist:
        return Response({'error': 'Skill not found'}, status=status.HTTP_404_NOT_FOUND)
