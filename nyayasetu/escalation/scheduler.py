
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from escalation.services import escalate_complaints

logger = logging.getLogger(__name__)

def run_escalations():
    logger.info('APScheduler: Running scheduled SLA escalation check...')
    try:
        count = escalate_complaints()
        logger.info(f'APScheduler: Escalation check complete. Processed {count} complaints.')
    except Exception as e:
        logger.error(f'APScheduler: Escalation check failed: {e}', exc_info=True)

def start():
    scheduler = BackgroundScheduler()
    # Run every 60 minutes
    scheduler.add_job(run_escalations, 'interval', minutes=60, id='escalation_job', replace_existing=True)
    scheduler.start()
    logger.info('APScheduler started: escalation_job will run every 60 minutes.')

