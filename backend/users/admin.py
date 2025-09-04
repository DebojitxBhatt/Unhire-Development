from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile, Skill, UserSkill, Portfolio


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'


class UserSkillInline(admin.TabularInline):
    model = UserSkill
    extra = 1


class PortfolioInline(admin.TabularInline):
    model = Portfolio
    extra = 1


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'role', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active', 'date_joined']
    search_fields = ['email']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('role',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role'),
        }),
    )
    
    inlines = [ProfileInline, UserSkillInline, PortfolioInline]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'availability_status', 'created_at']
    list_filter = ['availability_status', 'created_at']
    search_fields = ['user__email', 'first_name', 'last_name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']


@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ['user', 'skill', 'proficiency', 'years_experience', 'created_at']
    list_filter = ['proficiency', 'created_at']
    search_fields = ['user__email', 'skill__name']
    readonly_fields = ['created_at']


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__email', 'title', 'description']
    readonly_fields = ['created_at']
