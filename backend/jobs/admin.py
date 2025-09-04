from django.contrib import admin
from .models import Job, JobAttachment


class JobAttachmentInline(admin.TabularInline):
    model = JobAttachment
    extra = 1


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'client', 'status', 'priority', 'budget_min', 'budget_max',
        'deadline', 'experience_level', 'created_at', 'is_featured'
    ]
    list_filter = [
        'status', 'priority', 'experience_level', 'is_featured', 
        'created_at', 'deadline'
    ]
    search_fields = ['title', 'description', 'client__email']
    readonly_fields = [
        'created_at', 'updated_at', 'started_at', 'completed_at', 
        'views_count', 'applications_count'
    ]
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'client', 'status', 'priority')
        }),
        ('Budget & Timeline', {
            'fields': ('budget_min', 'budget_max', 'deadline', 'experience_level')
        }),
        ('Requirements', {
            'fields': ('required_skills',)
        }),
        ('Attachments', {
            'fields': ('attachments',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'started_at', 'completed_at'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('views_count', 'is_featured'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [JobAttachmentInline]
    
    def applications_count(self, obj):
        return obj.applications.count()
    applications_count.short_description = 'Applications'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('client')


@admin.register(JobAttachment)
class JobAttachmentAdmin(admin.ModelAdmin):
    list_display = ['job', 'filename', 'file_size', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['job__title', 'filename']
    readonly_fields = ['filename', 'file_size', 'uploaded_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('job')
