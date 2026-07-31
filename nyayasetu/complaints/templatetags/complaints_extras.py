from django import template

register = template.Library()

@register.filter
def is_overdue(complaint, now):
    if not now:
        return False
    if not complaint.sla_deadline:
        return False
    
    is_past_deadline = complaint.sla_deadline < now
    not_resolved = complaint.status != 'resolved'
    not_failed = complaint.status != 'administrative_failure'
    
    return is_past_deadline and not_resolved and not_failed
