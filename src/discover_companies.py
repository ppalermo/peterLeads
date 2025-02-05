import asyncio
from scanners.company_finder import CompanyFinder
from typing import List, Dict

# Your seed companies
SEED_COMPANIES = [
    {"name": "Uncommon Thread Vintage", "type": "Retail", "website": "uncommonthreadvintage.com"},
    {"name": "Rare Bloom", "type": "Retail", "website": "rarebloom.com"},
    {"name": "EZ Breezy Heating & Air", "type": "Service", "website": "ezbreezyhvac.com"},
    {"name": "Workiz", "type": "Software", "website": "workiz.com"},
    {"name": "Justworks Hours", "type": "Software", "website": "justworkshours.com"},
    {"name": "Cashie Commerce", "type": "Software", "website": "cashiecommerce.com"},
    {"name": "Nirvanix", "type": "Technology", "website": "nirvanix.com"},
    {"name": "Rose ASP", "type": "Technology", "website": "roseasp.com"},
    {"name": "AI + Strategy", "type": "Consulting", "website": "aistrategy.co"},
    {"name": "Dark Horse CPAs", "type": "Financial", "website": "darkhorse.cpa"},
    {"name": "Southwest Value Partners", "type": "Real Estate", "website": "swvp.com"},
    {"name": "The Enyeart Group", "type": "Real Estate", "website": "ockraig.com"},
    {"name": "GreenTech Landscaping", "type": "Service", "website": "greentechlandscaping.com"},
    {"name": "Riptide Sushi", "type": "Restaurant", "website": "riptidesushi.com"},
    {"name": "Calm Me Candles", "type": "Retail", "website": "calmmecandles.com"},
    {"name": "Sun Tamers Window Tinting", "type": "Service", "website": "suntamers.com"},
    {"name": "Parkes Plastic Bags", "type": "Manufacturing", "website": "parkesplastic.com"},
    {"name": "South County Plumbing", "type": "Service", "website": "socoplumbing.com"},
    {"name": "Brian Berg Insurance", "type": "Insurance", "website": "bbisinc.com"},
    {"name": "Memories Photography", "type": "Photography", "website": "flow.page/nlebaron"},
    {"name": "JF Financial", "type": "Financial", "website": "jffinancial.com"},
    {"name": "Genesis Sports PT", "type": "Healthcare", "website": "sports-performance-physical-therapy.com"},
    {"name": "Shield AI", "type": "Technology", "website": "shield.ai"},
    {"name": "Platform Science", "type": "Technology", "website": "platformscience.com"},
    {"name": "Great Question", "type": "Software", "website": "greatquestion.co"},
    {"name": "Community Boost", "type": "Marketing", "website": "communityboost.org"},
    {"name": "Lucas Group", "type": "Consulting", "website": "lucasgroup.com"},
    {"name": "Made Omni Inc", "type": "Technology", "website": "madeomni.com"},
    {"name": "Cask", "type": "Technology", "website": "casknx.com"}
]

async def main():
    finder = CompanyFinder()
    
    print("🔍 Finding similar companies...")
    companies = await finder.find_similar_companies(SEED_COMPANIES)
    
    print(f"✅ Found {len(companies)} companies")
    finder.save_companies(companies)
    
    # Create a combined list of seed + discovered companies
    all_companies = SEED_COMPANIES + companies
    
    # Save all URLs for scanning
    urls = [c['website'] for c in all_companies]
    with open('all_urls.txt', 'w') as f:
        f.write('\n'.join(urls))
    
    print(f"📝 Saved {len(urls)} URLs to all_urls.txt")
    return urls

if __name__ == "__main__":
    urls = asyncio.run(main()) 