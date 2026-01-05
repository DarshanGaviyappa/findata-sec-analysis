"""SEC Financial Statement Data Scraper"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SECScraper:
    """Scraper for SEC Financial Statement Data Sets"""
    
    BASE_URL = "https://www.sec.gov/dera/data/financial-statement-data-sets"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'FinData Inc. student@university.edu'
        })
    
    def scrape_dataset_links(self):
        """Scrape all dataset links from SEC page"""
        logger.info("Fetching SEC datasets...")
        response = self.session.get(self.BASE_URL)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        datasets = []
        for link in soup.find_all('a', href=True):
            if '.zip' in link['href'].lower():
                url = link['href']
                if not url.startswith('http'):
                    url = f"https://www.sec.gov{url}"
                datasets.append({
                    'url': url,
                    'filename': url.split('/')[-1],
                    'text': link.text.strip()
                })
        
        df = pd.DataFrame(datasets)
        logger.info(f"Found {len(df)} datasets")
        return df


if __name__ == "__main__":
    scraper = SECScraper()
    df = scraper.scrape_dataset_links()
    
    print(f"\nFound {len(df)} datasets")
    print("\nFirst 10 datasets:")
    print(df.head(10))
    
    # Save to CSV
    output_file = "../../data/raw/sec_datasets.csv"
    df.to_csv(output_file, index=False)
    print(f"\nSaved to {output_file}")
