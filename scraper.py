import requests
import json
import os

# 1. Setup - This gets your secret key from GitHub's settings
API_KEY = os.getenv('FEC_API_KEY')

# 2. Your "Impact 5" Targets
# We use State and District to find the "Full Field" of rivals automatically
TARGET_RACES = [
    {"state": "AZ", "dist": "01", "endorsed": "Amish Shah"},
    {"state": "NJ", "dist": "07", "endorsed": "Tina Shah"},
    {"state": "NJ", "dist": "12", "endorsed": "Jay Vaingankar"},
    {"state": "FL", "dist": "21", "endorsed": "Pia Dandiya"},
    {"state": "NY", "dist": "07", "endorsed": "Vichal Kumar"}
]

def get_race_data(state, district, endorsed_name):
    print(f"Fetching data for {state}-{district}...")
    url = "https://api.open.fec.gov/v1/candidates/totals/"
    params = {
        'api_key': API_KEY,
        'cycle': 2026,
        'state': state,
        'district': district,
        'election_full': True,
        'sort': '-cash_on_hand_end_period' # Get the wealthiest candidates first
    }
    
    try:
        response = requests.get(url, params=params)
        results = response.json().get('results', [])
        
        # We only want the top 6 (Our candidate + Top 5 Rivals)
        processed_candidates = []
        for cand in results[:6]:
            processed_candidates.append({
                "name": cand['name'],
                "id": cand['candidate_id'],
                "is_endorsed": endorsed_name.upper() in cand['name'].upper(),
                "receipts": cand['receipts'],
                "spent": cand['disbursements'],
                "coh": cand['last_cash_on_hand_end_period'],
                "updated": cand['coverage_end_date']
            })
        return processed_candidates
    except Exception as e:
        print(f"Error fetching {state}-{district}: {e}")
        return []

# 3. Main execution loop
def main():
    final_dashboard_data = {}
    
    for race in TARGET_RACES:
        race_id = f"{race['state']}-{race['dist']}"
        final_dashboard_data[race_id] = get_race_data(
            race['state'], 
            race['dist'], 
            race['endorsed']
        )

    # 4. Save to data.json
    # This file is what your website will read to show the charts
    with open('data.json', 'w') as f:
        json.dump(final_dashboard_data, f, indent=4)
    print("Success: data.json updated.")

if __name__ == "__main__":
    main()
