import os
from typing import List, Dict
import json
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from src.config import get_openai_client
import requests
from urllib.parse import urlparse

load_dotenv()

class CompanyFinder:
    def __init__(self):
        self.openai = get_openai_client()
        self.yelp_api_key = os.getenv('YELP_API_KEY')
        self.target_areas = [
            {'city': 'Los Angeles', 'state': 'CA'},
            {'city': 'San Diego', 'state': 'CA'},
            {'city': 'Irvine', 'state': 'CA'},  # Orange County
            {'city': 'Newport Beach', 'state': 'CA'},
            {'city': 'Laguna Beach', 'state': 'CA'}
        ]
        
    def get_business_categories(self, seed_companies: List[Dict]) -> List[str]:
        """Use GPT to analyze and categorize seed companies"""
        companies_text = "\n".join([f"{c['name']} - {c.get('type', 'Unknown')}" for c in seed_companies])
        
        prompt = f"""Given these companies:
        {companies_text}
        
        Generate 10 Yelp business categories that would find similar SMALL businesses.
        Focus on businesses that:
        1. Are local/independent (not chains)
        2. Likely need marketing help
        3. Have growth potential
        4. Are smaller scale (1-50 employees)
        
        Format: one category per line
        Example: restaurants, homeservices, professional
        
        Exclude categories for:
        - Major chains/franchises
        - Well-established brands
        - Large corporations"""
        
        response = self.openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        
        categories = response.choices[0].message.content.strip().split('\n')
        return categories

    async def search_yelp(self, category: str, location: Dict) -> List[Dict]:
        """Search Yelp API for businesses"""
        companies = []
        
        try:
            headers = {
                'Authorization': f'Bearer {self.yelp_api_key}'
            }
            
            # Search Yelp Business API
            url = 'https://api.yelp.com/v3/businesses/search'
            params = {
                'categories': category,
                'location': f"{location['city']}, {location['state']}",
                'limit': 20,
                'sort_by': 'rating',
                'attributes': 'website'  # Only businesses with websites
            }
            
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            
            for business in data.get('businesses', []):
                if business.get('url'):  # Only if they have a website
                    company = {
                        'name': business['name'],
                        'website': business['url'],
                        'address': ', '.join(business['location']['display_address']),
                        'phone': business.get('phone', ''),
                        'type': category,
                        'area': f"{location['city']}, {location['state']}",
                        'rating': business.get('rating', 0),
                        'reviews': business.get('review_count', 0),
                        'source': 'yelp'
                    }
                    companies.append(company)
                    print(f"  ✅ Found: {company['name']}")
            
        except Exception as e:
            print(f"  ❌ Error searching {category} in {location['city']}: {str(e)}")
            
        return companies

    async def find_similar_companies(self, seed_companies: List[Dict], limit: int = 100) -> List[Dict]:
        """Find similar companies using Yelp"""
        all_companies = []
        categories = self.get_business_categories(seed_companies)
        
        print("🔍 Generated business categories:")
        for cat in categories:
            print(f"  • {cat}")
        
        for location in self.target_areas:
            print(f"\n📍 Searching in {location['city']}...")
            for category in categories:
                companies = await self.search_yelp(category, location)
                all_companies.extend(companies)
                await asyncio.sleep(1)  # Rate limiting
        
        # Remove duplicates and filter
        unique_companies = {c['website']: c for c in all_companies}.values()
        filtered_companies = list(unique_companies)[:limit]
        
        print(f"\n🎯 Found {len(filtered_companies)} potential small businesses")
        return filtered_companies

    def save_companies(self, companies: List[Dict], filename: str = "discovered_companies.json"):
        """Save discovered companies to file"""
        with open(filename, 'w') as f:
            json.dump(companies, f, indent=2) 