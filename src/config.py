import os
from dotenv import load_dotenv
from openai import OpenAI
import httpx

load_dotenv()

# MongoDB Configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
DB_NAME = os.getenv('DB_NAME', 'smb_scanner')

# API Keys and Configurations
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Scanning Configuration
MAX_TIMEOUT = 30  # seconds
USER_AGENT = 'SMBScanner/1.0'

# Nuclei Configuration
NUCLEI_TEMPLATES = ['cves', 'vulnerabilities', 'misconfiguration']

def get_openai_client():
    client = OpenAI(
        api_key=os.getenv('OPENAI_API_KEY'),
        http_client=httpx.Client(
            timeout=60.0,
            follow_redirects=True
        )
    )
    return client 