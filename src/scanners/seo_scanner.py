import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
from googleapiclient.discovery import build
import re

# Load environment variables
load_dotenv()

# Configuration
USER_AGENT = 'SMBScanner/1.0'
MAX_TIMEOUT = 30
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_SEARCH_ENGINE_ID = os.getenv('GOOGLE_SEARCH_ENGINE_ID')

class SEOScanner:
    def __init__(self, url: str):
        self.url = url
        self.domain = self._extract_domain(url)
        self.headers = {'User-Agent': USER_AGENT}
        self.issues = []
        self.score = 0
        self.google_data = {}

    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL without protocol and www."""
        domain = re.sub(r'https?://(www\.)?', '', url)
        return domain.split('/')[0]

    async def scan(self) -> Dict:
        try:
            # Basic SEO checks
            response = requests.get(
                self.url, 
                headers=self.headers, 
                timeout=MAX_TIMEOUT
            )
            soup = BeautifulSoup(response.text, 'html.parser')
            
            self._check_title(soup)
            self._check_meta_description(soup)
            self._check_h1(soup)
            self._check_images_alt(soup)
            
            # Google-specific checks
            await self._check_google_indexing()
            await self._check_google_ranking()
            await self._check_site_links()
            
            return {
                'issues': self.issues,
                'score': self.score,
                'google_data': self.google_data
            }
        
        except Exception as e:
            self.issues.append(f"Failed to scan: {str(e)}")
            return {
                'issues': self.issues,
                'score': 0,
                'google_data': {}
            }

    async def _check_google_indexing(self):
        """Check if the site is indexed in Google"""
        try:
            if GOOGLE_API_KEY:
                service = build('customsearch', 'v1', developerKey=GOOGLE_API_KEY)
                result = service.cse().list(
                    q=f'site:{self.domain}',
                    cx=GOOGLE_SEARCH_ENGINE_ID
                ).execute()
                
                indexed_pages = int(result.get('searchInformation', {}).get('totalResults', 0))
                self.google_data['indexed_pages'] = indexed_pages
                
                if indexed_pages == 0:
                    self.issues.append("Site not indexed in Google")
                    self.score -= 30
                else:
                    self.score += 20
            else:
                # Fallback to scraping if no API key
                search_url = f"https://www.google.com/search?q=site:{quote_plus(self.domain)}"
                response = requests.get(search_url, headers=self.headers)
                if "did not match any documents" in response.text:
                    self.issues.append("Site not indexed in Google")
                    self.score -= 30
        except Exception as e:
            self.issues.append(f"Failed to check Google indexing: {str(e)}")

    async def _check_google_ranking(self):
        """Check if the site ranks for its own brand name"""
        try:
            brand_name = self.domain.split('.')[0]  # Simple brand name extraction
            if GOOGLE_API_KEY:
                service = build('customsearch', 'v1', developerKey=GOOGLE_API_KEY)
                result = service.cse().list(
                    q=brand_name,
                    cx=GOOGLE_SEARCH_ENGINE_ID
                ).execute()
                
                items = result.get('items', [])
                found_position = None
                for i, item in enumerate(items[:10]):
                    if self.domain in item['link']:
                        found_position = i + 1
                        break
                
                self.google_data['brand_position'] = found_position
                if not found_position or found_position > 5:
                    self.issues.append(f"Site not ranking well for brand name '{brand_name}'")
                    self.score -= 20
        except Exception as e:
            self.issues.append(f"Failed to check Google ranking: {str(e)}")

    async def _check_site_links(self):
        """Check if the site has sitelinks in Google"""
        try:
            if GOOGLE_API_KEY:
                service = build('customsearch', 'v1', developerKey=GOOGLE_API_KEY)
                result = service.cse().list(
                    q=self.domain,
                    cx=GOOGLE_SEARCH_ENGINE_ID
                ).execute()
                
                # Check for sitelinks in the search results
                if 'items' in result and len(result['items']) > 0:
                    first_result = result['items'][0]
                    if 'sitelinks' in first_result:
                        self.google_data['has_sitelinks'] = True
                        self.score += 10
                    else:
                        self.google_data['has_sitelinks'] = False
                        self.issues.append("No sitelinks in Google results")
        except Exception as e:
            self.issues.append(f"Failed to check sitelinks: {str(e)}")

    def _check_title(self, soup):
        title = soup.find('title')
        if not title:
            self.issues.append("Missing title tag")
            return
        if len(title.text) < 10 or len(title.text) > 60:
            self.issues.append(f"Title length issue ({len(title.text)} chars)")
        else:
            self.score += 20

    def _check_meta_description(self, soup):
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if not meta_desc:
            self.issues.append("Missing meta description")
        else:
            self.score += 20

    def _check_h1(self, soup):
        h1_tags = soup.find_all('h1')
        if not h1_tags:
            self.issues.append("Missing H1 tag")
        elif len(h1_tags) > 1:
            self.issues.append("Multiple H1 tags found")
        else:
            self.score += 20

    def _check_images_alt(self, soup):
        images = soup.find_all('img')
        missing_alt = 0
        for img in images:
            if not img.get('alt'):
                missing_alt += 1
        
        if missing_alt > 0:
            self.issues.append(f"Found {missing_alt} images without alt text")
        else:
            self.score += 20 