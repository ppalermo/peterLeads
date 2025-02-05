import asyncio
from scanners.business_finder import BusinessFinder
from typing import List
import json
import os

async def fetch_initial_urls(limit: int = 100) -> List[str]:
    config = {
        'GOOGLE_MAPS_KEY': os.getenv('GOOGLE_MAPS_KEY'),
        'YELP_API_KEY': os.getenv('YELP_API_KEY')
    }
    
    finder = BusinessFinder(config)
    businesses = await finder.find_businesses()
    
    # Filter to businesses with websites
    urls = [b['website'] for b in businesses if b.get('website')]
    
    # Save business data for later reference
    with open('business_data.json', 'w') as f:
        json.dump(businesses, f, indent=2)
    
    return urls[:limit]

if __name__ == "__main__":
    urls = asyncio.run(fetch_initial_urls(100))
    print(f"Found {len(urls)} websites to scan")
    
    # Save URLs for later use
    with open('test_urls.txt', 'w') as f:
        f.write('\n'.join(urls)) 