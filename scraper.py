import requests
import json
import os

API_KEY = os.getenv('FEC_API_KEY')

# Simplified list to ensure matches
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
        
        # We use the search endpoint first to get all candidates in the district
        url = "https://api.open.fec.gov/v1/candidates/totals/"
        params = {
            'api_key': API_KEY,
            'cycle': 2026,
            'state': race['state'],
            'district': race['dist'],
            'election_full': True,
            'sort': '-cash_on_hand_end_period',
            'per_page': 20
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code != 200:
                print(f"Error {response.status_code} for {race['state']}")
                all_data[f"{race['state']}-{race['dist']}"] = []
                continue

            data = response.json()
            results = data.get('results', [])
            
            processed = []
            for cand in results:
                cand_name = cand.get('name', 'Unknown Candidate')
                # Check if this is the Impact candidate
                is_impact = race['impact'].upper() in cand_name.upper()
                
                processed.append({
                    "name": cand_name,
                    "is_impact": is_impact,
                    "coh": cand.get('last_cash_on_hand_end_period') or 0,
                    "receipts": cand.get('receipts') or 0
                })
            
            # Save the results (Top 10 to be safe)
            all_data[f"{race['state']}-{race['dist']}"] = processed[:10]
            
        except Exception as e:
            print(f"Failed {race['state']}: {str(e)}")
            all_data[f"{race['state']}-{race['dist']}"] = []

    # Write the file
    with open('data.json', 'w') as f:
        json.dump(all_data, f, indent=4)
    print("Dashboard Data Saved.")

if __name__ == "__main__":
    fetch_data()
