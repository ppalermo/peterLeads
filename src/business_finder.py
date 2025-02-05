import asyncio
import aiohttp
from typing import List, Dict
import json
from bs4 import BeautifulSoup
from config import get_openai_client
import requests
from urllib.parse import urljoin
import os
from dotenv import load_dotenv

load_dotenv()

class BusinessFinder:
    def __init__(self):
        self.openai = get_openai_client()
        self.yelp_api_key = os.getenv('YELP_API_KEY')
        print(f"Debug - API Key loaded: {self.yelp_api_key[:10]}... (length: {len(self.yelp_api_key) if self.yelp_api_key else 0})")
        self.target_areas = [
            {'city': 'San Diego', 'state': 'CA'},
            {'city': 'La Jolla', 'state': 'CA'},
            {'city': 'Del Mar', 'state': 'CA'},
            {'city': 'Carlsbad', 'state': 'CA'},
            {'city': 'Encinitas', 'state': 'CA'},
            {'city': 'Sorrento Valley', 'state': 'CA'},
            {'city': 'Miramar', 'state': 'CA'},
            {'city': 'Kearny Mesa', 'state': 'CA'},
            {'city': 'UTC', 'state': 'CA'},
            {'city': 'Mission Valley', 'state': 'CA'}
        ]
        
    def get_business_categories(self) -> List[str]:
        """Generate business categories for mid-sized companies"""
        prompt = """Generate 20 specific Yelp search terms for established businesses in San Diego area.
        Focus on businesses that:
        1. Have 10-200 employees
        2. Revenue $1M-$50M annually
        3. Need digital marketing or tech solutions
        4. Have growth potential
        
        Format each term as a specific business type, like:
        commercial construction company
        enterprise software development
        medical device manufacturer
        boutique marketing agency
        
        Target industries:
        - Technology/Software
        - Professional Services
        - Manufacturing
        - Healthcare/Medical
        - Construction/Real Estate
        - Business Services
        
        Exclude:
        - Retail chains
        - Restaurants/Food service
        - Personal services
        - Very small businesses"""
        
        response = self.openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        
        categories = response.choices[0].message.content.strip().split('\n')
        return [c.strip() for c in categories]

    async def search_yelp(self, category: str, location: Dict) -> List[Dict]:
        """Search Yelp API for businesses"""
        companies = []
        
        try:
            api_key = self.yelp_api_key.strip()
            headers = {
                'Authorization': f'Bearer {api_key}'  # Just use the key directly
            }
            url = 'https://api.yelp.com/v3/businesses/search'
            
            # More targeted parameters
            params = {
                'term': category,
                'location': f"{location['city']}, {location['state']}",
                'limit': 50,
                'sort_by': 'review_count',
                'radius': 40000,
                'price': '3,4'  # Focus on higher-end businesses
            }
            
            print(f"  🔍 Searching for {category} in {location['city']}...")
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code != 200:
                print(f"  ❌ Yelp API error ({response.status_code}): {response.text}")
                return companies

            data = response.json()
            total = data.get('total', 0)
            print(f"  📊 Found {total} total results")
            
            for business in data.get('businesses', []):
                if (business.get('url') and 
                    business.get('review_count', 0) >= 25 and  # More reviews suggest established business
                    not any(chain in business['name'].lower() 
                           for chain in ['walmart', 'target', 'costco', 'amazon', 'starbucks', 
                                       'mcdonalds', 'subway', 'enterprise', 'hertz']) and
                    not any(term in business['name'].lower()
                           for term in ['franchise', 'chain', 'inc.', 'corporation'])):
                    
                    company = {
                        'name': business['name'],
                        'website': business['url'],
                        'address': ', '.join(business['location']['display_address']),
                        'phone': business.get('phone', ''),
                        'type': category,
                        'area': f"{location['city']}, {location['state']}",
                        'rating': business.get('rating', 0),
                        'reviews': business.get('review_count', 0),
                        'price': business.get('price', ''),
                        'source': 'yelp'
                    }
                    companies.append(company)
                    print(f"  ✅ Found: {company['name']} ({company['reviews']} reviews)")
            
        except Exception as e:
            print(f"  ❌ Error searching {category} in {location['city']}: {str(e)}")
            
        return companies

    async def find_businesses(self, limit: int = 200) -> List[Dict]:
        """Find businesses using multiple sources"""
        all_companies = []
        categories = self.get_business_categories()
        
        print("🔍 Generated search terms:")
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
        filtered_companies = sorted(
            list(unique_companies),
            key=lambda x: (x.get('reviews', 0), x.get('rating', 0)),
            reverse=True
        )[:limit]
        
        print(f"\n🎯 Found {len(filtered_companies)} potential businesses")
        return filtered_companies

    def save_results(self, companies: List[Dict]):
        """Save results to files"""
        # Save full details
        with open('discovered_companies.json', 'w') as f:
            json.dump(companies, f, indent=2)
            
        # Save just URLs for scanning
        urls = [c['website'] for c in companies]
        with open('all_urls.txt', 'w') as f:
            f.write('\n'.join(urls))
            
        print(f"📝 Saved {len(companies)} companies")

async def main():
    finder = BusinessFinder()
    companies = await finder.find_businesses()
    finder.save_results(companies)

if __name__ == "__main__":
    asyncio.run(main()) 