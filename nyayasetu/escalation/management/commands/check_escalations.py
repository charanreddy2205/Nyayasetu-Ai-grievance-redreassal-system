import logging
from django.core.management.base import BaseCommand
from escalation.services import escalate_complaints

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Checks for overdue complaints and escalates them accordingly.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting escalation check...'))
        try:
            escalate_complaints()
            self.stdout.write(self.style.SUCCESS('Escalation check completed successfully.'))
        except Exception as e:
            logger.error(f"Error during escalation check: {e}")
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
