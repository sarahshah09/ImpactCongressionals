import requests
import json
import os

API_KEY = os.getenv('FEC_API_KEY')

# Updated list with exact district matching
TARGET_RACES = [
    {"state": "AZ", "dist": "01", "impact": "Shah"},
    {"state": "NJ", "dist": "07", "impact": "Shah"},
    {"state": "NJ", "dist": "12", "impact": "Vaingankar"},
    {"state": "FL", "dist": "21", "impact": "Dandiya"},
    {"state": "NY", "dist": "07", "impact": "Kumar"}
]

def fetch_data():
    all_data = {}
    for race in TARGET_RACES:
        print(f"Syncing {race['state']}-{race['dist']}...")
        # This endpoint gets the financial totals for all candidates in that district
        url = "https://api.open.fec.gov/v1/candidates/totals/"
        params = {
            'api_key': API_KEY,
            'cycle': 2026,
            'state': race['state'],
            'district': race['dist'],
            'election_full': True,
            'sort': '-cash_on_hand_end_period'
        }
        
        try:
            response = requests.get(url, params=params).json()
            results = response.get('results', [])
            
            processed = []
            for cand in results:
                # Logic: Is this an IA Impact candidate?
                is_impact = race['impact'].upper() in cand['name'].upper()
                
                processed.append({
                    "name": cand['name'],
                    "is_impact": is_impact,
                    "coh": cand['last_cash_on_hand_end_period'] or 0,
                    "receipts": cand['receipts'] or 0,
                    "updated": cand['coverage_end_date']
                })
            
            # We only keep the top 6 total to keep the dashboard clean
            all_data[f"{race['state']}-{race['dist']}"] = processed[:6]
            
        except Exception as e:
            print(f"Error in {race['state']}: {e}")
            
    with open('data.json', 'w') as f:
        json.dump(all_data, f, indent=4)

if __name__ == "__main__":
    fetch_data()
