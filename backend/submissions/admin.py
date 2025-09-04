from django.contrib import admin
from .models import Submission, SubmissionAttachment


class SubmissionAttachmentInline(admin.TabularInline):
    model = SubmissionAttachment
    extra = 1


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'job', 'freelancer', 'submission_type', 'title', 'status',
        'submitted_at', 'deadline', 'is_overdue'
    ]
    list_filter = [
        'status', 'submission_type', 'is_overdue', 'submitted_at', 'deadline'
    ]
    search_fields = [
        'job__title', 'freelancer__email', 'title', 'description'
    ]
    readonly_fields = [
        'submitted_at', 'updated_at', 'reviewed_at', 'is_overdue'
    ]
    ordering = ['-submitted_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('job', 'freelancer', 'application', 'submission_type', 'title', 'description')
        }),
        ('Files & Status', {
            'fields': ('files', 'status', 'deadline', 'is_overdue')
        }),
        ('Review Information', {
            'fields': ('reviewed_by', 'client_feedback', 'rejection_reason', 'revision_notes'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('submitted_at', 'updated_at', 'reviewed_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [SubmissionAttachmentInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('job', 'freelancer', 'application', 'reviewed_by')
    
    def has_add_permission(self, request):
        return False  # Submissions should only be created through the API
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(SubmissionAttachment)
class SubmissionAttachmentAdmin(admin.ModelAdmin):
    list_display = ['submission', 'filename', 'file_size', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['submission__title', 'filename']
    readonly_fields = ['filename', 'file_size', 'uploaded_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('submission')
