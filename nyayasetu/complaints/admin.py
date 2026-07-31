from django.contrib import admin
from .models import Complaint
from escalation.models import EscalationLog

class EscalationLogInline(admin.TabularInline):
    model = EscalationLog
    extra = 0
    fields = ('escalated_to', 'escalated_at', 'reason')
    readonly_fields = ('escalated_at',)
    can_delete = True

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'department', 'status', 'urgency_level', 'assigned_to', 'created_by', 'created_at', 'sla_deadline', 'is_overdue')
    list_filter = ('status', 'department', 'escalation_level', 'urgency_level', 'created_at')
    search_fields = ('title', 'description', 'created_by__username', 'assigned_to__username')
    list_editable = ('status', 'assigned_to')
    date_hierarchy = 'created_at'
    inlines = [EscalationLogInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'department')
        }),
        ('Assignment', {
            'fields': ('created_by', 'assigned_to', 'status')
        }),
        ('Priority & Escalation', {
            'fields': ('urgency_level', 'escalation_level')
        }),
        ('SLA & Timeline', {
            'fields': ('original_sla_hours', 'sla_deadline', 'created_at', 'resolved_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at',)
    
    def is_overdue(self, obj):
        from django.utils import timezone
        if obj.sla_deadline and obj.status not in ['resolved', 'administrative_failure']:
            return obj.sla_deadline < timezone.now()
        return False
    is_overdue.boolean = True
    is_overdue.short_description = 'Overdue'
    
    actions = ['mark_as_resolved', 'mark_as_escalated', 'assign_to_me']
    
    def mark_as_resolved(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='resolved', resolved_at=timezone.now())
        self.message_user(request, f'{updated} complaint(s) marked as resolved.')
    mark_as_resolved.short_description = 'Mark selected as Resolved'
    
    def mark_as_escalated(self, request, queryset):
        updated = queryset.update(status='escalated')
        self.message_user(request, f'{updated} complaint(s) marked as escalated.')
    mark_as_escalated.short_description = 'Mark selected as Escalated'
    
    def assign_to_me(self, request, queryset):
        updated = queryset.update(assigned_to=request.user)
        self.message_user(request, f'{updated} complaint(s) assigned to you.')
    assign_to_me.short_description = 'Assign selected to me'
