import requests
import json
import os

API_KEY = os.getenv('FEC_API_KEY')

# Official IA Impact IDs for 2026
TARGET_RACES = [
    {"state": "AZ", "dist": "01", "name": "Amish Shah", "id": "H4AZ01221"},
    {"state": "NJ", "dist": "07", "name": "Tina Shah", "id": "H4NJ07191"},
    {"state": "NJ", "dist": "12", "name": "Jay Vaingankar", "id": "H4NJ12167"},
    {"state": "FL", "dist": "21", "name": "Pia Dandiya", "id": "H6FL21151"},
    {"state": "NY", "dist": "07", "name": "Vichal Kumar", "id": "H4NY07204"}
]

def fetch_data():
    all_data = {}
    for race in TARGET_RACES:
        print(f"Syncing {race['name']} ({race['state']}-{race['dist']})...")
        
        # Step 1: Get the Endorsed Candidate's Data
        url = f"https://api.open.fec.gov/v1/candidate/{race['id']}/totals/"
        params = {'api_key': API_KEY, 'cycle': 2026}
        
        try:
            r = requests.get(url, params=params).json()
            impact_stats = r.get('results', [{}])[0]
            
            # Step 2: Get the Rivals in that same district
            rival_url = "https://api.open.fec.gov/v1/candidates/totals/"
            rival_params = {
                'api_key': API_KEY, 'cycle': 2026, 
                'state': race['state'], 'district': race['dist'],
                'election_full': True, 'sort': '-cash_on_hand_end_period'
            }
            rival_r = requests.get(rival_url, params=rival_params).json()
            rival_results = rival_r.get('results', [])

            processed = []
            # Add Endorsed Candidate first
            processed.append({
                "name": race['name'],
                "is_impact": True,
                "coh": impact_stats.get('last_cash_on_hand_end_period', 0) or 0
            })

            # Add Top 5 Rivals (excluding our candidate)
            for cand in rival_results:
                if cand.get('candidate_id') != race['id']:
                    processed.append({
                        "name": cand.get('name', 'Unknown'),
                        "is_impact": False,
                        "coh": cand.get('last_cash_on_hand_end_period', 0) or 0
                    })
            
            all_data[f"{race['state']}-{race['dist']}"] = processed[:6]
            
        except Exception as e:
            print(f"Error: {e}")

    with open('data.json', 'w') as f:
        json.dump(all_data, f, indent=4)

if __name__ == "__main__":
    fetch_data()
