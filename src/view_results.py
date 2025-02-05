from database import Database
from datetime import datetime
from tabulate import tabulate
import csv

def format_scan_results(website_data):
    """Format the scan results into a readable format"""
    scan_results = website_data.get('scan_results', {})
    url = website_data.get('url')
    scan_date = website_data.get('scan_date', datetime.now())
    
    print(f"\n{'='*80}")
    print(f"🌐 Website: {url}")
    print(f"📅 Scan Date: {scan_date}")
    print(f"📊 SEO Score: {scan_results.get('score', 0)}/100")
    
    # Issues
    if scan_results.get('issues'):
        print("\n⚠️ Issues Found:")
        for issue in scan_results['issues']:
            print(f"  • {issue}")
    
    # Google Data
    if scan_results.get('google_data'):
        print("\n🔎 Google Data:")
        for key, value in scan_results['google_data'].items():
            print(f"  • {key}: {value}")
    
    print(f"{'='*80}\n")

def view_all_results():
    db = Database()
    websites = db.get_all_websites()
    
    if not websites:
        print("No scan results found in database!")
        return
    
    # Summary table
    summary_data = []
    for website in websites:
        scan_results = website.get('scan_results', {})
        summary_data.append([
            website.get('url'),
            scan_results.get('score', 0),
            len(scan_results.get('issues', [])),
            website.get('scan_date', 'Unknown').strftime("%Y-%m-%d %H:%M")
        ])
    
    # Print summary table
    print("\n📊 Summary of All Scans")
    print(tabulate(
        summary_data,
        headers=['URL', 'Score', 'Issues', 'Scan Date'],
        tablefmt='grid'
    ))
    
    # Detailed results
    print("\n🔍 Detailed Results")
    for website in websites:
        format_scan_results(website)

def export_to_csv(filename: str = "scan_results.csv"):
    db = Database()
    websites = db.get_all_websites()
    
    if not websites:
        print("No data to export!")
        return
        
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        writer.writerow([
            'URL',
            'Score',
            'Business Name',
            'Location',
            'Contact Email',
            'Contact Phone',
            'Social Media',
            'Issues Found',
            'Scan Date',
            'Reason for Flag'
        ])
        
        # Write data
        for website in websites:
            scan_results = website.get('scan_results', {})
            contacts = scan_results.get('contacts', {})
            
            writer.writerow([
                website.get('url'),
                scan_results.get('score', 0),
                website.get('business_name', ''),
                website.get('location', ''),
                ', '.join(contacts.get('emails', [])),
                ', '.join(contacts.get('phones', [])),
                ', '.join([s['platform'] for s in contacts.get('social_media', [])]),
                '; '.join(scan_results.get('issues', [])),
                website.get('scan_date', datetime.now()).strftime("%Y-%m-%d %H:%M"),
                scan_results.get('flag_reason', '')
            ])
    
    print(f"Results exported to {filename}")

if __name__ == "__main__":
    view_all_results() 