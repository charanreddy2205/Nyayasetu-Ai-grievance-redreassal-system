from .auth import UserSerializer, RegisterSerializer
from .complaint import ComplaintSerializer, CommentSerializer, ComplaintCreateSerializer
from .department import DepartmentSerializer
from .dashboard import DashboardStatsSerializer

__all__ = [
    "UserSerializer",
    "RegisterSerializer",
    "ComplaintSerializer",
    "CommentSerializer",
    "ComplaintCreateSerializer",
    "DepartmentSerializer",
    "DashboardStatsSerializer",
]
