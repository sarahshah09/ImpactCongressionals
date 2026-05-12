import requests
import json
import os

API_KEY = os.getenv('FEC_API_KEY')

# Updated 2026 Official IDs
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
        print(f"--- Processing {race['name']} ---")
        
        # Step A: Get the Specific Candidate Financials
        # Using the /candidate/{id}/totals endpoint is the most accurate
        url = f"https://api.open.fec.gov/v1/candidate/{race['id']}/totals/"
        params = {'api_key': API_KEY, 'cycle': 2026}
        
        try:
            r = requests.get(url, params=params).json()
            impact_results = r.get('results', [])
            
            # If the ID search is empty, the FEC hasn't indexed them yet
            if not impact_results:
                print(f"Warning: No data yet for ID {race['id']}")
                coh = 0
            else:
                coh = impact_results[0].get('last_cash_on_hand_end_period', 0) or 0
            
            # Step B: Get ALL candidates in the district for comparison
            dist_url = "https://api.open.fec.gov/v1/candidates/totals/"
            dist_params = {
                'api_key': API_KEY, 'cycle': 2026, 
                'state': race['state'], 'district': race['dist'],
                'election_full': True
            }
            dist_r = requests.get(dist_url, params=dist_params).json()
            dist_results = dist_r.get('results', [])

            processed = []
            # Add our Impact Candidate
            processed.append({"name": race['name'], "is_impact": True, "coh": float(coh)})

            # Add Rivals
            for cand in dist_results:
                if cand.get('candidate_id') != race['id']:
                    processed.append({
                        "name": cand.get('name', 'Unknown Candidate').title(),
                        "is_impact": False,
                        "coh": float(cand.get('last_cash_on_hand_end_period', 0) or 0)
                    })
            
            # Sort by money so the biggest rival is at the top
            processed.sort(key=lambda x: x['coh'], reverse=True)
            all_data[f"{race['state']}-{race['dist']}"] = processed[:6]
            print(f"Successfully added {len(processed)} candidates.")

        except Exception as e:
            print(f"System Error for {race['state']}: {e}")

    with open('data.json', 'w') as f:
        json.dump(all_data, f, indent=4)
    print("FINISHED: data.json is ready.")

if __name__ == "__main__":
    fetch_data()
