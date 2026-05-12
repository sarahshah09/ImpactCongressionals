import requests
import json
import os

API_KEY = os.getenv('FEC_API_KEY')

# Core 5 Districts
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
        print(f">>> Fetching: {race['state']}-{race['dist']}...")
        
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
            r = requests.get(url, params=params, timeout=15)
            r.raise_for_status()
            data = r.json()
            results = data.get('results', [])
            
            print(f"Found {len(results)} candidates in {race['state']}-{race['dist']}")
            
            processed = []
            for cand in results[:8]: # Grab top 8 to be safe
                name = cand.get('name', 'Unknown')
                # Safety check: ensure coh is a number
                coh = cand.get('last_cash_on_hand_end_period')
                if coh is None: coh = 0
                
                processed.append({
                    "name": name,
                    "is_impact": race['impact'].upper() in name.upper(),
                    "coh": float(coh)
                })
            
            all_data[f"{race['state']}-{race['dist']}"] = processed
            
        except Exception as e:
            print(f"!!! Error in {race['state']}: {str(e)}")
            all_data[f"{race['state']}-{race['dist']}"] = []

    # Final Save
    with open('data.json', 'w') as f:
        json.dump(all_data, f, indent=4)
    print("DONE: data.json has been written.")

if __name__ == "__main__":
    fetch_data()
