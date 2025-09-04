from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, Profile, Skill, UserSkill, Portfolio


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'is_active', 'date_joined']
        read_only_fields = ['id', 'is_active', 'date_joined']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm', 'role', 'first_name', 'last_name']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        
        user = User.objects.create_user(**validated_data)
        
        # Create profile
        Profile.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name
        )
        
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include email and password')
        
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class UserSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)
    skill_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = UserSkill
        fields = ['id', 'skill', 'skill_id', 'proficiency', 'years_experience', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def create(self, validated_data):
        skill_id = validated_data.pop('skill_id')
        validated_data['skill_id'] = skill_id
        return super().create(validated_data)


class PortfolioSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Portfolio
        fields = '__all__'
        read_only_fields = ['user', 'created_at']


class UserDetailSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    skills = UserSkillSerializer(many=True, read_only=True)
    portfolio_items = PortfolioSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'is_active', 'date_joined', 'profile', 'skills', 'portfolio_items']
        read_only_fields = ['id', 'is_active', 'date_joined']
