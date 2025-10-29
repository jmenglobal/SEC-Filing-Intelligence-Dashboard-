from django.core.management.base import BaseCommand
from filings.tasks import fetch_all_companies_filings

class Command(BaseCommand):
    help = 'Fetch filings for all companies'

    def handle(self, *args, **options):
        fetch_all_companies_filings.delay()
        self.stdout.write(self.style.SUCCESS('Filing fetch jobs queued'))