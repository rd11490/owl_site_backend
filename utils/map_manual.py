"""
converts
{
    sim: True/False
    teamOne: str,
    teamOneWins?: int,
    teamTwo: str,
    teamTwoWins?: int,
}
into
{
    team_one: str,
    team_one_map_wins: int,
    team_two: str,
    team_two_map_wins: int,
    winner: str,
    loser: str
}
"""
def map_manual(manual):
    return {
        'team_one': manual['teamOne'],
        'team_one_map_wins': manual['teamOneWins'],
        'team_two': manual['teamTwo'],
        'team_two_map_wins': manual['teamTwoWins'],
        'winner': manual['teamTwo'] if manual['teamTwoWins'] > manual['teamOneWins'] else manual['teamOne'],
        'loser': manual['teamTwo'] if manual['teamTwoWins'] < manual['teamOneWins'] else manual['teamOne']
    }

def map_schedule(sched):
    return {
        'team_one': sched['teamOne'],
        'team_two': sched['teamTwo']
    }