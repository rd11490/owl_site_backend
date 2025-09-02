import datetime
import requests
import pandas as pd
import os
import json



def fetch_win_rates(params):
    print(f"Fetching win rates with params: {params}")
    url = "https://overwatch.blizzard.com/en-us/rates/data/"
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    rows = []
    today = datetime.date.today().isoformat()
    for rate in data.get("rates", []):
        cell = rate.get('cells', {})
        row = {
            "name": cell.get("name"),
            "pickrate": cell.get("pickrate"),
            "winrate": cell.get("winrate"),
            **params,
            "date": today
        }
        rows.append(row)
    df = pd.DataFrame(rows)
    return df

REGION_LIST = ["Americas", "Asia", "Europe"]
TIER_LIST = [
    "Bronze", "Silver", "Gold", "Platinum", "Diamond", "Master", "Grandmaster", "All"
]
MAP_LIST = [
    "all-maps", "antarctic-peninsula", "busan", "ilios", "lijang-tower", "nepal", "oasis", "samoa",
    "circuit-royal", "dorado", "havana", "junkertown", "rialto", "route-66", "shambali-monastery",
    "watchpoint-gibraltar", "aatlis", "new-junk-city", "suravasa", "blizzard-world", "eichenwalde",
    "hollywood", "kings-row", "midtown", "numbani", "paraiso", "colosseo", "esperanca",
    "new-queen-street", "runasapi"
]

def scrape_win_rates(event, context):
    bucket = os.environ.get('OWL_SITE_DATA_BUCKET')
    region = None
    # Support both scheduled and HTTP (API Gateway) input
    if event:
        # API Gateway (HTTP) event: region is in event['body'] as JSON string
        if 'body' in event and event['body']:
            try:
                body = json.loads(event['body'])
                region = body.get('region')
            except Exception as e:
                print(f"Error parsing body: {e}")
        # Scheduled event: region is top-level key
        elif 'region' in event:
            region = event.get('region')
    if region not in REGION_LIST:
        print(f"No valid region provided in event: {event}. Exiting.")
        return {
            "statusCode": 400,
            "body": f"No valid region provided. Valid options: {REGION_LIST}"
        }
    region_dfs = []
    for tier in TIER_LIST:
        for map_name in MAP_LIST:
            params = {
                "input": "PC",
                "map": map_name,
                "region": region,
                "role": "All",
                "rq": "2",
                "tier": tier
            }
            try:
                df = fetch_win_rates(params)
                if not df.empty:
                    region_dfs.append(df)
            except Exception as e:
                print(f"Error for params {params}: {e}")
    if region_dfs:
        region_df = pd.concat(region_dfs, ignore_index=True)
        filename = f"overwatch_win_rates_{region.lower()}.csv"
        s3_path = f"s3://{bucket}/{filename}"
        # Try to read existing CSV from S3
        try:
            existing_df = pd.read_csv(s3_path)
            combined_df = pd.concat([existing_df, region_df], ignore_index=True)
            print(f"Appending to existing {s3_path}, total rows: {len(combined_df)}")
        except Exception as e:
            combined_df = region_df
            print(f"No existing file or error reading {s3_path}: {e}. Writing new file.")
        # Drop duplicates before saving
    # Only use name, map, region, tier, and date for deduplication
    index_cols = ["name", "map", "region", "tier", "date"]
    deduped_df = combined_df.drop_duplicates(subset=index_cols)
    deduped_df.to_csv(s3_path, index=False)
    print(f"Saved {s3_path} with {len(deduped_df)} rows after dropping duplicates.")
    else:
        print(f"No data collected for region {region}.")
