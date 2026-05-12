import requests
import json
import os

API_KEY = os.getenv('FEC_API_KEY')

# Official 2026 Committee IDs (These are the actual bank accounts)
TARGET_RACES = [
    {"state": "AZ-01", "name": "Amish Shah", "cmte": "C00836510"},
    {"state": "NJ-07", "name": "Tina Shah", "cmte": "C00851832"},
    {"state": "NJ-12", "name": "Jay Vaingankar", "cmte": "C00845552"},
    {"state": "FL-21", "name": "Pia Dandiya", "cmte": "C00854422"},
    {"state": "NY-07", "name": "Vichal Kumar", "cmte": "C00850230"}
]

def fetch_data():
    all_data = {}
    for race in TARGET_RACES:
        print(f"Fetching {race['name']}...")
        
        # Pull totals directly from the committee's filing
        url = f"https://api.open.fec.gov/v1/committee/{race['cmte']}/totals/"
        params = {'api_key': API_KEY, 'cycle': 2026}
        
        try:
            r = requests.get(url, params=params).json()
            results = r.get('results', [])
            
            # If the 2026 cycle is empty, we check the latest available
            if not results:
                print(f"No 2026 data for {race['name']}, checking 2024 leftover...")
                params['cycle'] = 2024
                r = requests.get(url, params=params).json()
                results = r.get('results', [])

            coh = 0
            if results:
                coh = results[0].get('last_cash_on_hand_end_period', 0) or 0

            # For now, let's just get our candidate on the board
            all_data[race['state']] = [{
                "name": race['name'],
                "is_impact": True,
                "coh": float(coh)
            }]
            
        except Exception as e:
            print(f"Error: {e}")

    with open('data.json', 'w') as f:
        json.dump(all_data, f, indent=4)
    print("Done!")

if __name__ == "__main__":
    fetch_data()
