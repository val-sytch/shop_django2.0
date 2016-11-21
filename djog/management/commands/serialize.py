from django.core.management.base import BaseCommand
from djog.serialization.serialize import main


class Command(BaseCommand):
    """
    Launch script for serializing models in json
    """
    def handle(self, *args, **options):
        main()
