from departments.models import Department

class DepartmentService:
    """
    Service handling operations on the Department model.
    """
    @staticmethod
    def list_departments() -> list[Department]:
        """
        Retrieves all registered departments ordered alphabetically.
        """
        return Department.objects.all().order_by('name')
