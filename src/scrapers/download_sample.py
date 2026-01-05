"""Download and extract SEC sample dataset"""
import requests
import zipfile
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def download_dataset(url, output_dir="data/raw/sample"):
    """Download and extract a dataset"""
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Extract filename
    filename = url.split('/')[-1]
    zip_path = Path(output_dir) / filename
    
    # Download
    logger.info(f"Downloading {filename}...")
    response = requests.get(url, headers={
        'User-Agent': 'FinData Inc. student@university.edu'
    })
    
    with open(zip_path, 'wb') as f:
        f.write(response.content)
    
    logger.info(f"Downloaded {zip_path}")
    
    # Extract
    logger.info("Extracting files...")
    extract_dir = Path(output_dir) / filename.replace('.zip', '')
    extract_dir.mkdir(exist_ok=True)
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    
    logger.info(f"Extracted to {extract_dir}")
    
    # List files
    files = list(extract_dir.glob('*.txt'))
    logger.info(f"Found {len(files)} files:")
    for f in files:
        logger.info(f"  - {f.name}")
    
    return extract_dir


if __name__ == "__main__":
    # Download Q4 2024
    url = "https://www.sec.gov/files/dera/data/financial-statement-data-sets/2024q4.zip"
    extract_dir = download_dataset(url)
    
    print(f"\n✅ Dataset downloaded and extracted to: {extract_dir}")
    print("\nNext: Examine the .txt files to understand data structure")
