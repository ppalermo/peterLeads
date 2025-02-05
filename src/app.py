from flask import Flask, render_template, jsonify, send_file
import json
import pandas as pd
import io
from datetime import datetime

app = Flask(__name__)

def load_companies():
    with open('discovered_companies.json', 'r') as f:
        return json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/companies')
def get_companies():
    companies = load_companies()
    return jsonify(companies)

@app.route('/api/export-csv')
def export_csv():
    companies = load_companies()
    df = pd.DataFrame(companies)
    
    # Create CSV in memory
    output = io.StringIO()
    df.to_csv(output, index=False)
    
    # Create the response
    mem_file = io.BytesIO()
    mem_file.write(output.getvalue().encode('utf-8'))
    mem_file.seek(0)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return send_file(
        mem_file,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'companies_{timestamp}.csv'
    ) 