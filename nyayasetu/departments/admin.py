from django.contrib import admin
from .models import Department
from accounts.models import User

class DepartmentMemberInline(admin.TabularInline):
    model = User
    extra = 1
    fields = ('username', 'email', 'role', 'is_active')
    verbose_name = 'Department Member'
    verbose_name_plural = 'Department Members'

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'sla_hours', 'transparency_score', 'member_count', 'created_at')
    search_fields = ('name',)
    inlines = [DepartmentMemberInline]
    
    def member_count(self, obj):
        return obj.users.count()
    member_count.short_description = 'Members'
