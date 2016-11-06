from django.core.management.base import BaseCommand
from services.google_img_downloader import main


class Command(BaseCommand):
    """
    Launch script for downloading images using Google API
    """
    def handle(self, *args, **options):
        main()
