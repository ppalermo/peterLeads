import json
import pandas as pd
from tabulate import tabulate

def analyze_companies():
    # Load the JSON data
    with open('discovered_companies.json', 'r') as f:
        companies = json.load(f)
    
    # Convert to DataFrame for easier analysis
    df = pd.DataFrame(companies)
    
    # Basic stats
    print(f"\n📊 Found {len(df)} companies")
    print(f"📍 Areas covered: {', '.join(df['area'].unique())}")
    print(f"💼 Business types: {', '.join(df['type'].unique())}")
    
    # Show top companies by reviews
    print("\n🏆 Top 10 companies by reviews:")
    top_10 = df.nlargest(10, 'reviews')[['name', 'type', 'area', 'reviews', 'rating', 'website']]
    print(tabulate(top_10, headers='keys', tablefmt='pipe', showindex=False))
    
    # Group by area
    print("\n📍 Companies by area:")
    area_counts = df.groupby('area').size().sort_values(ascending=False)
    print(tabulate(pd.DataFrame(area_counts), headers=['Area', 'Count'], tablefmt='pipe'))
    
    # Group by business type
    print("\n💼 Companies by type:")
    type_counts = df.groupby('type').size().sort_values(ascending=False)
    print(tabulate(pd.DataFrame(type_counts), headers=['Type', 'Count'], tablefmt='pipe'))

if __name__ == "__main__":
    analyze_companies() 