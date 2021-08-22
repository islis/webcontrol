from django.core.management.base import BaseCommand
from smarthouse.mqtt_worker import listener


class Command(BaseCommand):
    def handle(self, *args, **options):
        listener()
