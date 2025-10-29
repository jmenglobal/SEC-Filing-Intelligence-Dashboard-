from celery import shared_task
from .models import Company, Filing
from .utils.sec_api import SECFetcher
import logging

logger = logging.getLogger(__name__)


@shared_task
def fetch_company_filings(company_id):
    """Fetch filings for a specific company"""
    try:
        company = Company.objects.get(id=company_id)
        fetcher = SECFetcher()
        
        filings_data = fetcher.get_company_filings(company.cik)
        
        for filing_data in filings_data:
            filing, created = Filing.objects.get_or_create(
                accession_number=filing_data['accession_number'],
                defaults={
                    'company': company,
                    'form_type': filing_data['form_type'],
                    'filing_date': filing_data['filing_date'],
                    'document_url': filing_data['filing_url'],
                }
            )
            
            if created:
                # Download full text
                text = fetcher.download_filing_text(
                    filing_data['accession_number'],
                    company.cik
                )
                if text:
                    filing.raw_text = text
                    filing.save()
                    logger.info(f"Downloaded filing: {filing.accession_number}")
        
        return f"Fetched filings for {company.name}"
    except Exception as e:
        logger.error(f"Error fetching filings: {str(e)}")
        raise

@shared_task
def fetch_all_companies_filings():
    """Queue up filing fetch for all companies"""
    companies = Company.objects.all()
    for company in companies:
        fetch_company_filings.delay(company.id)
