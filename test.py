
import datetime
import requests
import pandas as pd
import time


# Region constants
REGION_AMERICAS = "Americas"
REGION_ASIA = "Asia"
REGION_EUROPE = "Europe"
REGION_LIST = [
    REGION_AMERICAS,
    REGION_ASIA,
    REGION_EUROPE
]

# Tier constants
TIER_BRONZE = "Bronze"
TIER_SILVER = "Silver"
TIER_GOLD = "Gold"
TIER_PLATINUM = "Platinum"
TIER_DIAMOND = "Diamond"
TIER_MASTER = "Master"
TIER_GRANDMASTER = "Grandmaster"
TIER_ALL = "All"
TIER_LIST = [
    TIER_BRONZE,
    TIER_SILVER,
    TIER_GOLD,
    TIER_PLATINUM,
    TIER_DIAMOND,
    TIER_MASTER,
    TIER_GRANDMASTER,
    TIER_ALL
]

# Map constants
MAP_ALL = "all-maps"
MAP_ANTARCTIC_PENINSULA = "antarctic-peninsula"
MAP_BUSAN = "busan"
MAP_ILIOS = "ilios"
MAP_LIJIANG_TOWER = "lijiang-tower"
MAP_NEPAL = "nepal"
MAP_OASIS = "oasis"
MAP_SAMOA = "samoa"
MAP_CIRCUIT_ROYAL = "circuit-royal"
MAP_DORADO = "dorado"
MAP_HAVANA = "havana"
MAP_JUNKERTOWN = "junkertown"
MAP_RIALTO = "rialto"
MAP_ROUTE_66 = "route-66"
MAP_SHAMBALI_MONASTERY = "shambali-monastery"
MAP_WATCHPOINT_GIBRALTAR = "watchpoint-gibraltar"
MAP_AATLIS = "aatlis"
MAP_NEW_JUNK_CITY = "new-junk-city"
MAP_SURAVASA = "suravasa"
MAP_BLIZZARD_WORLD = "blizzard-world"
MAP_EICHENWALDE = "eichenwalde"
MAP_HOLLYWOOD = "hollywood"
MAP_KINGS_ROW = "kings-row"
MAP_MIDTOWN = "midtown"
MAP_NUMBANI = "numbani"
MAP_PARAISO = "paraiso"
MAP_COLOSSEO = "colosseo"
MAP_ESPERANCA = "esperanca"
MAP_NEW_QUEEN_STREET = "new-queen-street"
MAP_RUNASAPI = "runasapi"
MAP_LIST = [
    MAP_ALL,
    MAP_ANTARCTIC_PENINSULA,
    MAP_BUSAN,
    MAP_ILIOS,
    MAP_LIJIANG_TOWER,
    MAP_NEPAL,
    MAP_OASIS,
    MAP_SAMOA,
    MAP_CIRCUIT_ROYAL,
    MAP_DORADO,
    MAP_HAVANA,
    MAP_JUNKERTOWN,
    MAP_RIALTO,
    MAP_ROUTE_66,
    MAP_SHAMBALI_MONASTERY,
    MAP_WATCHPOINT_GIBRALTAR,
    MAP_AATLIS,
    MAP_NEW_JUNK_CITY,
    MAP_SURAVASA,
    MAP_BLIZZARD_WORLD,
    MAP_EICHENWALDE,
    MAP_HOLLYWOOD,
    MAP_KINGS_ROW,
    MAP_MIDTOWN,
    MAP_NUMBANI,
    MAP_PARAISO,
    MAP_COLOSSEO,
    MAP_ESPERANCA,
    MAP_NEW_QUEEN_STREET,
    MAP_RUNASAPI
]
def fetch_win_rates(params):
    """
    Make API call to Overwatch win rates endpoint and return a DataFrame of results.
    params: dict of query parameters
    """
    print(f"Fetching win rates with params: {params}")
    url = "https://overwatch.blizzard.com/en-us/rates/data/"
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    rows = []
    today = datetime.date.today().isoformat()
    for rate in data.get("rates", []):
        # The correct key is likely 'calls', not 'cells'
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


# Iterate over all combinations and collect results, saving one CSV per region
for region in REGION_LIST:
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
        # Try to read existing file and append
        try:
            existing_df = pd.read_csv(filename)
            # Use params as index to prevent duplicates
            index_cols = ["input", "map", "region", "role", "rq", "tier"]
            combined_df = pd.concat([existing_df, region_df], ignore_index=True)
            combined_df = combined_df.drop_duplicates(subset=index_cols)
        except FileNotFoundError:
            combined_df = region_df
        combined_df.to_csv(filename, index=False)
        print(f"Saved {filename} with {len(combined_df)} rows.")
    else:
        print(f"No data collected for region {region}.")
    time.sleep(5)
