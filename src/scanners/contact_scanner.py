import re
import whois
import requests
from bs4 import BeautifulSoup
from typing import Dict
import aiohttp
from urllib.parse import urljoin

class ContactScanner:
    def __init__(self, url: str):
        self.url = url
        self.domain = self._extract_domain(url)
        
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL without protocol and www."""
        domain = re.sub(r'https?://(www\.)?', '', url)
        return domain.split('/')[0]
        
    def _is_contact_form(self, form: BeautifulSoup) -> bool:
        """Check if a form is likely a contact form"""
        contact_indicators = ['contact', 'email', 'message', 'name', 'phone']
        
        # Check form action
        action = form.get('action', '').lower()
        if any(ind in action for ind in ['contact', 'enquiry', 'feedback']):
            return True
            
        # Check input fields
        inputs = form.find_all(['input', 'textarea'])
        input_names = [i.get('name', '').lower() for i in inputs]
        if any(ind in ' '.join(input_names) for ind in contact_indicators):
            return True
            
        return False
        
    def _extract_contact_info(self, soup: BeautifulSoup, contacts: Dict):
        """Extract contact information from HTML"""
        # Extract emails
        text = soup.get_text()
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
        contacts['emails'].extend(list(set(emails)))
        
        # Extract phones
        phones = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
        contacts['phones'].extend(list(set(phones)))
        
        # Find social media links
        social_patterns = {
            'linkedin': r'linkedin\.com/(?:company|in)/',
            'facebook': r'facebook\.com/',
            'twitter': r'twitter\.com/',
            'instagram': r'instagram\.com/',
            'youtube': r'youtube\.com/'
        }
        
        for platform, pattern in social_patterns.items():
            links = soup.find_all('a', href=re.compile(pattern))
            if links:
                contacts['social_media'].append({
                    'platform': platform,
                    'url': links[0]['href']
                })
                
        # Try to find business hours
        hours_keywords = ['hours', 'schedule', 'timing', 'open']
        for keyword in hours_keywords:
            hours_section = soup.find(class_=re.compile(keyword, re.I))
            if hours_section:
                contacts['business_hours'] = hours_section.get_text(strip=True)
                break
                
    async def scan(self) -> Dict:
        """Scan website for contact information"""
        contacts = {
            'emails': [],
            'phones': [],
            'social_media': [],
            'contact_page': None,
            'forms': [],
            'business_hours': None,
            'whois_info': {}
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url, timeout=30) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        # Find contact page
                        contact_links = soup.find_all('a', href=re.compile(r'contact|about', re.I))
                        if contact_links:
                            contacts['contact_page'] = urljoin(self.url, contact_links[0]['href'])
                            
                            # Scan contact page
                            async with session.get(contacts['contact_page']) as contact_response:
                                if contact_response.status == 200:
                                    contact_html = await contact_response.text()
                                    contact_soup = BeautifulSoup(contact_html, 'html.parser')
                                    self._extract_contact_info(contact_soup, contacts)
                        
                        # Extract from main page too
                        self._extract_contact_info(soup, contacts)
                        
                        # Find contact forms
                        forms = soup.find_all('form')
                        for form in forms:
                            if self._is_contact_form(form):
                                contacts['forms'].append({
                                    'action': form.get('action', ''),
                                    'method': form.get('method', 'post'),
                                    'fields': [i.get('name', '') for i in form.find_all('input')]
                                })
                        
                        # Get WHOIS information
                        try:
                            w = whois.whois(self.domain)
                            contacts['whois_info'] = {
                                'registrar': w.registrar,
                                'creation_date': w.creation_date,
                                'emails': w.emails
                            }
                        except Exception as e:
                            print(f"WHOIS lookup failed for {self.domain}: {str(e)}")
                        
        except Exception as e:
            print(f"Error scanning {self.url}: {str(e)}")
            
        return contacts 