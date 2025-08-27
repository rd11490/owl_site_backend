# owl_site_backend
Backend for owl site


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

### scrape_win_rates
**Type:** Scheduled (CloudWatch Events) & API Gateway (POST)
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