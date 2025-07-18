import pandas as pd
import requests
from io import StringIO
import re

def convert_gsheets_url(url):
    """Convert Google Sheets sharing URL to CSV export URL"""
    if 'docs.google.com/spreadsheets' in url:
        match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', url)
        if match:
            spreadsheet_id = match.group(1)
            return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv"
    return url

def load_data_from_url(url):
    """Load CSV data from URL"""
    try:
        csv_url = convert_gsheets_url(url)
        response = requests.get(csv_url)
        response.raise_for_status()
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data)
        return df, None
    except Exception as e:
        return None, str(e)

def validate_data_structure(df):
    """Validate that the DataFrame has the expected columns"""
    required_columns = [
        'first_name', 'last_name', 'email', 'disc_profile'
    ]
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"
    
    return True, "Data structure is valid"
