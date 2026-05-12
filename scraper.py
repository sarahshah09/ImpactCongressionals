import requests
import json
import os

# Get key from GitHub Secrets
API_KEY = os.getenv('FEC_API_KEY')

# Impact 5 Configuration - Use strings for district to ensure '07' stays '07'
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
        # Endpoint for financial totals
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
            response = requests.get(url, params=params)
            response.raise_for_status() # This prevents "Exit Code 1" by catching errors early
            data = response.json()
            results = data.get('results', [])
            
            processed = []
            for cand in results:
                # Name matching logic
                is_impact = race['impact'].upper() in cand.get('name', '').upper()
                
                processed.append({
                    "name": cand.get('name', 'Unknown'),
                    "is_impact": is_impact,
                    "coh": cand.get('last_cash_on_hand_end_period') or 0,
                    "receipts": cand.get('receipts') or 0,
                    "updated": cand.get('coverage_end_date', 'N/A')
                })
            
            # Save the top 6 (Impact candidate + 5 rivals)
            all_data[f"{race['state']}-{race['dist']}"] = processed[:6]
            
        except Exception as e:
            print(f"Error in {race['state']}-{race['dist']}: {e}")
            # Ensure the race key exists even if the fetch failed
            all_data[f"{race['state']}-{race['dist']}"] = []

    with open('data.json', 'w') as f:
        json.dump(all_data, f, indent=4)
    print("Successfully wrote data.json")

if __name__ == "__main__":
    fetch_data()
