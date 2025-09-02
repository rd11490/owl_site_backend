
# owl_site_backend
Backend for owl site

## Running Tests Locally

Tests are located in the `tests/` directory and use pytest. To run all tests locally:

```bash
pip install -r requirements.txt
pip install pytest
PYTHONPATH=src pytest
```

If you use a virtual environment, activate it before installing dependencies.

To run a specific test file:
```bash
PYTHONPATH=src pytest tests/handlers/test_query_data.py
```

To see test coverage (optional):
```bash
pip install pytest-cov
PYTHONPATH=src pytest --cov=src
```

## Deployment

To deploy:

serverless deploy

## Handlers Overview

### get_faceit_rosters
**Type:** API Gateway (GET)
**Path:** /faceitRosters
**Description:**
Returns rosters for Faceit and WARA tournaments. Reads roster CSVs from S3 and returns them as JSON objects grouped by tournament name.
**Response Data Model:**
```
{
	"OWCS 2025: NA Stage 1 - Open Qualifiers": [ { ...roster fields... } ],
	"OWCS JAPAN OPEN 2025 Stage1": [ { ...roster fields... } ],
	...
}
```

### get_setup
**Type:** API Gateway (GET)
**Path:** /setup
**Description:**
Returns Overwatch setup data for a given season (teams, comps, heroes, maps, stats, etc). Reads multiple CSVs from S3 and returns them as lists.
**Query Parameters:**
- `season`: (optional) Season year (e.g., 2018, 2019, 2020, 2022, 2023)
**Response Data Model:**
```
{
	"comps": [ { ...composition fields... } ],
	"heroes": [ "Hero1", "Hero2", ... ],
	"mapNames": [ "Map1", "Map2", ... ],
	"mapTypes": [ "Type1", "Type2", ... ],
	"players": [ { ...player fields... } ],
	"stats": [ "Stat1", "Stat2", ... ],
	"stages": [ "Stage1", "Stage2", ... ],
	"teams": [ "Team1", "Team2", ... ]
}
```

### query_data
**Type:** API Gateway (POST)
**Path:** /query
**Description:**
Returns Overwatch stats data filtered and aggregated by season, aggregation type, teams, players, heroes, maps, etc. Reads hero data CSVs from S3 and applies filters/aggregation.
**Request Data Model:**
```
{
	"season": "2023",
	"aggregation": "PLAYER", // or TEAM, HERO, TEAMANDHERO, PLAYERANDHERO
	"teams": ["Team1", ...],
	"players": ["Player1", ...],
	"stages": ["Stage1", ...],
	"opponentTeams": ["Team2", ...],
	"composition": ["Comp1", ...],
	"opponentComposition": ["Comp2", ...],
	"mapTypes": ["Type1", ...],
	"mapNames": ["Map1", ...],
	"heroes": ["Hero1", ...],
	"stats": ["Stat1", ...]
}
```
**Response Data Model:**
```
{
	"data": [ { ...aggregated stats... } ],
	"stats": [ "Stat1", "Stat2", ... ]
}
```

### query_win_rates
**Type:** API Gateway (POST)
**Path:** /queryWinRates
**Description:**
Returns Overwatch win rate data filtered by date, region, map, hero, and rank. Reads win rate CSVs from S3 and returns grouped results for each hero/map/rank/region combination.
**Request Data Model:**
```
{
	"dateRange": { "min": "2024-01-01", "max": "2024-12-31" },
	"region": ["Americas", "Asia", "Europe"],
	"map": ["Map1", "Map2"],
	"hero": ["Hero1", "Hero2"],
	"rank": ["All", "Diamond"]
}
```
**Response Data Model:**
```
[
	{
		"hero": "Hero1",
		"map": "Map1",
		"rank": "Diamond",
		"region": "Americas",
		"data": [
			{ "winRate": 0.52, "pickRate": 0.13, "date": "2024-01-01" },
			...
		]
	},
	...
]
```
**Type:** Scheduled (CloudWatch Events)
**Path:** /scrapeWinRates
**Description:**
Fetches Overwatch win rate data from Blizzard API for all tiers/maps/regions, aggregates results, and writes CSVs to S3. Scheduled runs are region-specific and run every 4 hours.
**Request Data Model (API):**
```
{
	"region": "Americas" // or "Asia", "Europe"
}
```
**Response:**
- Writes CSV to S3 bucket, returns status message.