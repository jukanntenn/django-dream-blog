from django.core.management import call_command
from huey import crontab
from huey.contrib.djhuey import db_periodic_task


@db_periodic_task(crontab(minute="00", hour="22"))
def backup_db():
    call_command("dbbackup", "--clean")
