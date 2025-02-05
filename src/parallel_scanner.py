import asyncio
import aiohttp
from typing import List, Dict
import pandas as pd
from tqdm import tqdm
from scanners.contact_scanner import ContactScanner
import os

async def scan_website(url: str) -> Dict:
    """Scan a single website"""
    scanner = ContactScanner(url)
    try:
        results = await scanner.scan()
        results['url'] = url
        return results
    except Exception as e:
        print(f"Error scanning {url}: {str(e)}")
        return {'url': url, 'error': str(e)}

async def scan_websites(urls: List[str], max_concurrent: int = 5):
    """Scan multiple websites concurrently"""
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def bounded_scan(url):
        async with semaphore:
            return await scan_website(url)
    
    tasks = [bounded_scan(url) for url in urls]
    results = []
    
    for task in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="Scanning websites"):
        result = await task
        results.append(result)
    
    return results

def export_results(results: List[Dict], filename: str = "scan_results.csv"):
    """Export results to CSV"""
    # Flatten the results
    flattened = []
    for r in results:
        flat = {
            'url': r.get('url', ''),
            'emails': ', '.join(r.get('emails', [])),
            'phones': ', '.join(r.get('phones', [])),
            'contact_page': r.get('contact_page', ''),
            'business_hours': r.get('business_hours', ''),
            'social_media': ', '.join([f"{s['platform']}: {s['url']}" for s in r.get('social_media', [])]),
            'forms_count': len(r.get('forms', [])),
            'whois_registrar': r.get('whois_info', {}).get('registrar', ''),
            'whois_emails': ', '.join(r.get('whois_info', {}).get('emails', []) or [])
        }
        flattened.append(flat)
    
    df = pd.DataFrame(flattened)
    df.to_csv(filename, index=False)
    print(f"Results exported to {filename}")

def format_url(url: str) -> str:
    """Ensure URL has proper format with protocol"""
    if not url.startswith(('http://', 'https://')):
        return f'https://{url}'
    return url

def main():
    # Read URLs from file
    with open('all_urls.txt', 'r') as f:
        urls = [format_url(line.strip()) for line in f if line.strip()]
    
    # Run the scanner
    results = asyncio.run(scan_websites(urls))
    
    # Export results
    export_results(results)

if __name__ == "__main__":
    main() 