from dotenv import load_dotenv
import os

load_dotenv()

yelp_key = os.getenv('YELP_API_KEY')
print(f"YELP API Key loaded: {yelp_key[:10]}... (length: {len(yelp_key) if yelp_key else 0})") 