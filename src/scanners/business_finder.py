import requests
from typing import List, Dict
import json
from bs4 import BeautifulSoup
import googlemaps
from yelp.client import Client

class BusinessFinder:
    def __init__(self, config):
        self.google_maps_key = config.get('GOOGLE_MAPS_KEY')
        self.yelp_api_key = config.get('YELP_API_KEY')
        self.target_locations = ['San Diego, CA', 'Orange County, CA']
        self.search_radius = 50000  # 50km radius

    async def find_businesses(self) -> List[Dict]:
        businesses = []
        
        # Google Places API search
        if self.google_maps_key:
            gmaps = googlemaps.Client(key=self.google_maps_key)
            for location in self.target_locations:
                # Search for different business types
                for business_type in ['restaurant', 'retail', 'service']:
                    results = gmaps.places_nearby(
                        location=gmaps.geocode(location)[0]['geometry']['location'],
                        radius=self.search_radius,
                        type=business_type
                    )
                    for place in results.get('results', []):
                        businesses.append({
                            'name': place.get('name'),
                            'address': place.get('vicinity'),
                            'website': place.get('website'),
                            'phone': place.get('formatted_phone_number'),
                            'source': 'google_places',
                            'location': location,
                            'business_type': business_type
                        })

        # Add more sources (Yelp, Chamber of Commerce, etc.)
        return businesses 