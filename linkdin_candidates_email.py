import requests
import pandas as pd
import time

# Config
API_TOKEN = 'apify_api_hhgub8xl3Y8CHe29xnvM5eb1hZhUuc2EM9Df'
ACTOR_ID = 'scraper-mind~linkedin-email-scraper'
ACTOR_INPUT = ACTOR_INPUT = {
    "keywords": ["pharmacy"], ## add your keyword
    "location": "kenya" ## add your country
}
  # Define your input JSON here

# 1. Start actor run
start_url = f'https://api.apify.com/v2/acts/{ACTOR_ID}/runs?token={API_TOKEN}'
start_response = requests.post(start_url, json={"input": ACTOR_INPUT})
start_response.raise_for_status()
run_id = start_response.json()['data']['id']

# 2. Poll until finished
status_url = f'https://api.apify.com/v2/actor-runs/{run_id}?token={API_TOKEN}'
while True:
    status_response = requests.get(status_url).json()
    status = status_response['data']['status']
    if status in ['SUCCEEDED', 'FAILED', 'TIMED-OUT', 'ABORTED']:
        break
    time.sleep(5)

if status != 'SUCCEEDED':
    raise Exception(f"Actor run failed with status: {status}")

# 3. Get dataset ID
dataset_id = status_response['data']['defaultDatasetId']
dataset_url = f'https://api.apify.com/v2/datasets/{dataset_id}/items?token={API_TOKEN}&format=json'

# 4. Download data
dataset_response = requests.get(dataset_url)
dataset_response.raise_for_status()
data = dataset_response.json()

# 5. Save to CSV
df = pd.DataFrame(data)
df.to_csv('apify_results.csv', index=False)
