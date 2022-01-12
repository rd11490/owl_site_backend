test = {
        "teamOrPlayer": "Player",
        "teams": ["Atlanta Reign"],
        "opponentTeams": ["Dallas Fuel"],
        "comp": 0,
        "opponentComp": 0,
        "heroes": ["Ana"],
        "xStatNum": "Critical Hits",
        "xStatDenom": "Shots Hit",
        "yStatNum": "All Damage Done",
        "yStatDenom": "Per 10"
    }

print(test.get('yStatDenom'))
print(test.get('zStatDenom'))
