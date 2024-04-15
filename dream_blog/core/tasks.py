from django.conf import settings
from django.core.mail import send_mail
from django.core.management import call_command
from huey import crontab
from huey.contrib.djhuey import db_periodic_task


@db_periodic_task(crontab(minute="00", hour="13"))  # UTC time
def backup_db():
    call_command("dbbackup", "--clean")


@db_periodic_task(crontab(minute="00", hour="13"))  # UTC time
def ping_hc_email_service_check():
    subject = "[django-dream-blog] Ping healthchecks.io email service check"
    message = "Ok!"

    ping_email = getattr(settings, "HC_EMAIL_SERVICE_PING_EMAIL", None)
    if not ping_email:
        return

    recipient_list = [ping_email]
    send_mail(subject, message, from_email=None, recipient_list=recipient_list)
