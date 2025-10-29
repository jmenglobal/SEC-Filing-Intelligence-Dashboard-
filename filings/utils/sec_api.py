import requests
import time
from datetime import datetime, timedelta

class SECFetcher:
    BASE_URL = "https://www.sec.gov"
    RATE_LIMIT_DELAY = 0.11  # 10 requests per second = 0.1s, add buffer

    def __init__(self):
        self.headers = {
            'User-Agent': 'mburca444@gmail.com',
            'Accept-Encoding': 'gzip, deflate',
        }

    def get_company_filings(self, cik, form_types=['10-K', '10-Q', '8-K'], count=100):
        """Fetch recent filings for a company"""
        url = f"{self.BASE_URL}/cgi-bin/browse-edgar"
        params = {
            'action': 'getcompany',
            'CIK': cik,
            'type': '',
            'dateb': '',
            'owner': 'exclude',
            'count': count,
            'output': 'atom'
        }
       
        time.sleep(self.RATE_LIMIT_DELAY)
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            return self._parse_atom_feed(response.content, form_types)
        return []
    
    def _parse_atom_feed(self, content, form_types):
        """Parse EDGAR ATOM feed"""
        from xml.etree import ElementTree as ET
        
        root = ET.fromstring(content)
        namespace = {'atom': 'http://www.w3.org/2005/Atom'}
        
        filings = []
        for entry in root.findall('atom:entry', namespace):
            form_type = entry.find('atom:category', namespace).get('term')
            
            if form_type in form_types:
                filing = {
                    'form_type': form_type,
                    'filing_date': entry.find('atom:updated', namespace).text[:10],
                    'accession_number': entry.find('atom:id', namespace).text.split('accession-number=')[1],
                    'filing_url': entry.find('atom:link', namespace).get('href')
                }
                filings.append(filing)
        
        return filings
    
    def download_filing_text(self, accession_number, cik):
        """Download full text of a filing"""
        # Remove dashes from accession number for URL
        acc_no_nodash = accession_number.replace('-', '')
        url = f"{self.BASE_URL}/Archives/edgar/data/{cik}/{acc_no_nodash}/{accession_number}.txt"
        
        time.sleep(self.RATE_LIMIT_DELAY)
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.text
        return None
    
    