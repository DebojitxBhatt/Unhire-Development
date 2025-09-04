from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'job', 'freelancer', 'status', 'proposed_budget', 
        'estimated_duration', 'applied_at', 'is_featured'
    ]
    list_filter = [
        'status', 'is_featured', 'applied_at', 'reviewed_at'
    ]
    search_fields = [
        'job__title', 'freelancer__email', 'proposal', 'cover_letter'
    ]
    readonly_fields = [
        'applied_at', 'updated_at', 'reviewed_at'
    ]
    ordering = ['-applied_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('job', 'freelancer', 'status', 'is_featured')
        }),
        ('Proposal Details', {
            'fields': ('proposal', 'cover_letter', 'proposed_budget', 'estimated_duration')
        }),
        ('Review Information', {
            'fields': ('reviewed_by', 'client_feedback', 'rejection_reason'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('applied_at', 'updated_at', 'reviewed_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('job', 'freelancer', 'reviewed_by')
    
    def has_add_permission(self, request):
        return False  # Applications should only be created through the API
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
