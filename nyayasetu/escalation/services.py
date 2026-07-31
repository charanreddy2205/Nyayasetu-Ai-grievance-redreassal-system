from api.services.escalation_service import EscalationService

def escalate_complaints() -> int:
    """
    Delegates to the refactored EscalationService to process SLA breaches.
    """
    return EscalationService.escalate_complaints()
