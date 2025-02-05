import asyncio
from scanners.seo_scanner import SEOScanner
from database import Database
from datetime import datetime

async def test_scan_website(url: str):
    print(f"\n🔍 Scanning website: {url}")
    print("=" * 50)
    
    scanner = SEOScanner(url)
    results = await scanner.scan()
    
    print("\n📊 SEO Score:", results['score'])
    
    if results['issues']:
        print("\n⚠️ Issues Found:")
        for issue in results['issues']:
            print(f"  • {issue}")
    
    if results['google_data']:
        print("\n🔎 Google Data:")
        for key, value in results['google_data'].items():
            print(f"  • {key}: {value}")
    
    print("\n" + "=" * 50)
    return results

async def main():
    # Test URLs with a variety of sites
    test_urls = [
        "https://www.python.org",   # Well-established site
        "https://example.com",      # Simple test site
        "https://www.smallbusinesssd.com",  # Small business site (example)
        "https://www.sandiegobusiness.org", # Local business site
    ]
    
    db = Database()
    
    for url in test_urls:
        try:
            print(f"\nTesting: {url}")
            results = await test_scan_website(url)
            # Store results in MongoDB
            website_data = {
                'url': url,
                'scan_results': results,
                'scan_date': datetime.now()
            }
            db.save_website(website_data)
        except Exception as e:
            print(f"Error scanning {url}: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 