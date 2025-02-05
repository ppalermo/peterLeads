# Business Lead Generator

A tool to discover and analyze potential business leads in the San Diego area, with a focus on mid-sized companies that might need digital marketing and tech solutions.

## Features

### 1. Business Discovery
- Uses Yelp's API to find established businesses
- Targets companies with 10-200 employees
- Focuses on B2B and enterprise businesses
- Filters out chains and very small businesses
- Covers multiple areas in San Diego region

### 2. Data Collection
- Company name and contact details
- Business type and location
- Review counts and ratings
- Website URLs
- Phone numbers
- Physical addresses

### 3. Web Interface
- Interactive data table with sorting and filtering
- Quick stats overview
- CSV export functionality
- Real-time data refresh
- Mobile responsive design

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/business-lead-generator.git
cd business-lead-generator
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables in `.env`:
```env
YELP_API_KEY=your_yelp_api_key
OPENAI_API_KEY=your_openai_api_key
GOOGLE_MAPS_KEY=your_google_maps_key
MAX_CONCURRENT_SCANS=10
```

## Usage

### 1. Find Businesses
```bash
PYTHONPATH=. python src/business_finder.py
```
This will:
- Generate targeted search terms using GPT
- Search for businesses using Yelp's API
- Save results to `discovered_companies.json`
- Create `all_urls.txt` for scanning

### 2. Scan Websites
```bash
PYTHONPATH=. python src/parallel_scanner.py
```
This will:
- Scan company websites for contact information
- Extract emails, phone numbers, and social media
- Save results to `scan_results.csv`

### 3. View Results in Web Interface
```bash
PYTHONPATH=. FLASK_APP=src/app.py flask run
```
Then visit http://localhost:5000 to:
- Browse discovered companies
- Sort and filter results
- Export data to CSV
- View analytics

## Project Structure
```
├── src/
│   ├── scanners/
│   │   ├── __init__.py
│   │   ├── company_finder.py
│   │   └── contact_scanner.py
│   ├── templates/
│   │   └── index.html
│   ├── app.py
│   ├── business_finder.py
│   ├── parallel_scanner.py
│   └── analyze_results.py
├── .env
├── requirements.txt
└── README.md
```

## Dependencies
- Flask for web interface
- Pandas for data manipulation
- BeautifulSoup for web scraping
- OpenAI GPT for search term generation
- Yelp API for business discovery
- DataTables for interactive tables
- Bootstrap for UI components

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- Yelp Fusion API
- OpenAI GPT-3.5
- DataTables.net
- Bootstrap

## Future Improvements
- [ ] Add more data sources (LinkedIn, Google Maps)
- [ ] Implement lead scoring
- [ ] Add email verification
- [ ] Integrate with CRM systems
- [ ] Add more analytics features

# peterLeads
