# User Roles
ROLE_CITIZEN = 'citizen'
ROLE_STAFF = 'staff'
ROLE_HOD = 'hod'
ROLE_DISTRICT_OFFICER = 'district_officer'
ROLE_STATE_ADMIN = 'state_admin'

ROLE_CHOICES = (
    (ROLE_CITIZEN, 'Citizen'),
    (ROLE_STAFF, 'Staff'),
    (ROLE_HOD, 'HOD'),
    (ROLE_DISTRICT_OFFICER, 'District Officer'),
    (ROLE_STATE_ADMIN, 'State Admin'),
)

# Complaint Statuses
STATUS_PENDING = 'pending'
STATUS_IN_PROGRESS = 'in_progress'
STATUS_RESOLVED = 'resolved'
STATUS_ESCALATED = 'escalated'
STATUS_ADMINISTRATIVE_FAILURE = 'administrative_failure'

STATUS_CHOICES = (
    (STATUS_PENDING, 'Pending'),
    (STATUS_IN_PROGRESS, 'In Progress'),
    (STATUS_RESOLVED, 'Resolved'),
    (STATUS_ESCALATED, 'Escalated'),
    (STATUS_ADMINISTRATIVE_FAILURE, 'Administrative Failure'),
)

# Urgency Levels
URGENCY_LOW = 'low'
URGENCY_MEDIUM = 'medium'
URGENCY_HIGH = 'high'
URGENCY_CRITICAL = 'critical'

URGENCY_CHOICES = (
    (URGENCY_LOW, 'Low'),
    (URGENCY_MEDIUM, 'Medium'),
    (URGENCY_HIGH, 'High'),
    (URGENCY_CRITICAL, 'Critical'),
)

# SLA Rules
DEFAULT_SLA_HOURS = 24
MAX_ESCALATION_LEVEL = 3
TRANSPARENCY_PENALTY = 5
