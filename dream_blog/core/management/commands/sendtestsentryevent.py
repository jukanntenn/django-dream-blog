from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Sends a test sentry event."

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        1 / 0
