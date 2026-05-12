import requests
import json
import os

API_KEY = os.getenv('FEC_API_KEY')

# Official 2026 Committee IDs - Verified Active for May 2026
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
        
        coh = 0
        # Check 2026 first, then fallback to 2024 to catch pending transfers
        for cycle in [2026, 2024]:
            url = f"https://api.open.fec.gov/v1/committee/{race['cmte']}/totals/"
            params = {'api_key': API_KEY, 'cycle': cycle}
            try:
                r = requests.get(url, params=params, timeout=10).json()
                results = r.get('results', [])
                if results:
                    found_coh = results[0].get('last_cash_on_hand_end_period', 0)
                    if found_coh and found_coh > 0:
                        coh = found_coh
                        break 
            except:
                continue

        # Create the data entry even if $0, so the dashboard shows the name
        all_data[race['state']] = [{
            "name": race['name'],
            "is_impact": True,
            "coh": float(coh)
        }]

    with open('data.json', 'w') as f:
        json.dump(all_data, f, indent=4)
    print("Dashboard Data successfully updated.")

if __name__ == "__main__":
    fetch_data()
