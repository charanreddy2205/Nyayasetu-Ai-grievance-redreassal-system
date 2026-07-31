from django.contrib import admin
from .models import EscalationLog

@admin.register(EscalationLog)
class EscalationLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'complaint', 'escalated_to', 'escalated_at', 'reason_preview')
    search_fields = ('complaint__title', 'escalated_to__username', 'reason')
    list_filter = ('escalated_at', 'escalated_to__role')
    date_hierarchy = 'escalated_at'
    readonly_fields = ('escalated_at',)
    
    fieldsets = (
        ('Complaint Information', {
            'fields': ('complaint',)
        }),
        ('Escalation Details', {
            'fields': ('escalated_to', 'reason', 'escalated_at')
        }),
    )
    
    def reason_preview(self, obj):
        return obj.reason[:50] + '...' if len(obj.reason) > 50 else obj.reason
    reason_preview.short_description = 'Reason'
    
    def has_add_permission(self, request):
        # Allow manual escalation creation
        return True
