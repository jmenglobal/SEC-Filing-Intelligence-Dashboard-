import requests
import time
from django.core.management.base import BaseCommand
from filings.models import Company

class Command(BaseCommand):
    help = 'Load company data from SEC'

    def handle(self, *args, **options):
        # Download company tickers JSON
        url = 'https://www.sec.gov/files/company_tickers.json'
        headers = {'User-Agent': 'mburca444@gmail.com'}
        
        response = requests.get(url, headers=headers)
        data = response.json()
        
        for key, company_data in data.items():
            Company.objects.update_or_create(
                cik=str(company_data['cik_str']).zfill(10),
                defaults={
                    'name': company_data['title'],
                    'ticker': company_data['ticker'],
                }
            )
            self.stdout.write(f"Loaded: {company_data['ticker']}")
        
        self.stdout.write(self.style.SUCCESS('Companies loaded successfully'))