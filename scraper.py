import requests
import json
import os

API_KEY = os.getenv('FEC_API_KEY')

# Verified 2026 Committee IDs
TARGET_RACES = [
    {"state": "AZ-01", "name": "Amish Shah", "cmte": "C00836510"},
    {"state": "NJ-07", "name": "Tina Shah", "cmte": "C00851832"},
    {"state": "NJ-12", "name": "Jay Vaingankar", "cmte": "C00929802"},
    {"state": "FL-21", "name": "Pia Dandiya", "cmte": "C00854422"},
    {"state": "NY-07", "name": "Vichal Kumar", "cmte": "C00850230"}
]

def fetch_data():
    all_data = {}
    for race in TARGET_RACES:
        print(f"Syncing {race['name']}...")
        
        # We look at the 'reports' endpoint - it's the most reliable source of truth
        url = f"https://api.open.fec.gov/v1/committee/{race['cmte']}/reports/"
        params = {
            'api_key': API_KEY,
            'cycle': 2026,
            'sort': '-coverage_end_date',
            'per_page': 1
        }
        
        try:
            r = requests.get(url, params=params, timeout=15).json()
            report = r.get('results', [{}])[0]
            
            # Grab Cash on Hand from the most recent filing
            coh = report.get('cash_on_hand_close_ytd', 0) or 0
            
            all_data[race['state']] = [{
                "name": race['name'],
                "is_impact": True,
                "coh": float(coh)
            }]
            print(f"Found ${coh} for {race['name']}")
            
        except Exception as e:
            print(f"Error for {race['name']}: {e}")

    with open('data.json', 'w') as f:
        json.dump(all_data, f, indent=4)

if __name__ == "__main__":
    fetch_data()
