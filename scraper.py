import requests
import json
import os

API_KEY = os.getenv('FEC_API_KEY')

# Core 5 Districts - Using just Last Names for maximum matching
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
        print(f"Searching {race['state']}-{race['dist']}...")
        
        # We use the 'candidates' search which is more reliable for finding people
        url = "https://api.open.fec.gov/v1/candidates/search/"
        params = {
            'api_key': API_KEY,
            'cycle': 2026,
            'state': race['state'],
            'district': race['dist'],
            'office': 'H', # House
            'is_active_candidate': True,
            'per_page': 50
        }
        
        try:
            r = requests.get(url, params=params, timeout=15)
            results = r.json().get('results', [])
            
            processed = []
            for cand in results:
                name = cand.get('name', 'Unknown')
                # Check for Impact candidate by last name
                is_impact = race['impact'].upper() in name.upper()
                
                # Note: 'totals' inside candidate search is often more populated
                # We prioritize 'last_cash_on_hand_end_period'
                total_data = cand.get('principal_committees', [{}])[0]
                
                processed.append({
                    "name": name,
                    "is_impact": is_impact,
                    "coh": cand.get('cash_on_hand', 0) or 0,
                    "receipts": cand.get('total_receipts', 0) or 0
                })
            
            # Sort by who has the most money so rivals appear at the top
            processed.sort(key=lambda x: x['coh'], reverse=True)
            all_data[f"{race['state']}-{race['dist']}"] = processed[:8]
            
        except Exception as e:
            print(f"Error in {race['state']}: {e}")
            all_data[f"{race['state']}-{race['dist']}"] = []

    with open('data.json', 'w') as f:
        json.dump(all_data, f, indent=4)
    print("Update Complete.")

if __name__ == "__main__":
    fetch_data()
