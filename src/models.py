from datetime import datetime
from typing import List, Optional, Dict

class Website:
    def __init__(self, url: str):
        self.url = url
        self.scan_date = datetime.utcnow()
        self.seo_issues = []
        self.security_issues = []
        self.broken_components = []
        self.contact_info = {
            'emails': [],
            'phones': [],
            'social_media': []
        }
        self.score = 0
        self.reasons = []

    def to_dict(self) -> Dict:
        return {
            'url': self.url,
            'scan_date': self.scan_date,
            'seo_issues': self.seo_issues,
            'security_issues': self.security_issues,
            'broken_components': self.broken_components,
            'contact_info': self.contact_info,
            'score': self.score,
            'reasons': self.reasons
        } 