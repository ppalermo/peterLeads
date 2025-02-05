# peterLeads

A tool to discover and analyze potential business leads in Southern California, with a focus on mid-sized companies that might need digital marketing and tech solutions.

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
- Website URLs and social media
- Contact forms detection
- WHOIS information

### 3. Web Interface
- Interactive data table with sorting and filtering
- Quick stats overview
- CSV export functionality
- Real-time data refresh
- Mobile responsive design

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/peterLeads.git
cd peterLeads
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

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

## Usage

1. Find Businesses:
```bash
PYTHONPATH=. python src/business_finder.py
```

2. Scan Websites:
```bash
PYTHONPATH=. python src/parallel_scanner.py
```

3. View Results:
```bash
PYTHONPATH=. FLASK_APP=src/app.py flask run
```
Then visit http://localhost:5000

## API Keys Needed

- [Yelp Fusion API](https://www.yelp.com/developers/documentation/v3)
- [OpenAI API](https://platform.openai.com/)
- [Google Custom Search API](https://developers.google.com/custom-search)

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

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
