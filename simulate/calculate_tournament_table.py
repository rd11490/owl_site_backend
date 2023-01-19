import pandas as pd

from simulate.constants import Teams


def calculate_opponent_tie_breakers(table):
    for k in table.keys():
        team_table = table[k]
        opponent_points = 0
        opponent_differential = 0
        for result in team_table['results']:
            opponent_points += table[result['opponent']]['wins']
            opponent_differential += (table[result['opponent']]['maps_won'] - table[result['opponent']]['maps_lost'])
        team_table['opponent_points'] = opponent_points
        team_table['opponent_differential'] = opponent_differential
        team_table['map_differential'] = team_table['maps_won'] - team_table['maps_lost']
        table[k] = team_table
    return table


def calculate_tournament_table(match_results_frame):
    table = build_table(Teams.West22)

    for ind in match_results_frame.index:
        row = match_results_frame.loc[ind, :]
        table = update_table(row, table)
    table = calculate_opponent_tie_breakers(table)
    frame = pd.DataFrame(table.values())
    frame['league_points'] = frame['wins']
    sorted_frame = sort_table(frame)
    return sorted_frame


def build_table(teams):
    table = {}
    for t in teams:
        table[t] = {
            'team': t,
            'wins': 0,
            'losses': 0,
            'maps_won': 0,
            'maps_lost': 0,
            'results': [],  # { 'opponent': <TEAM>, 'score': <-3 to 3>
        }
    return table


def update_table(row, table):
    if row['winner'] == row['team_one']:
        winner = row['team_one']
        loser = row['team_two']

        winner_table = table[winner]
        winner_table['wins'] += 1
        winner_table['maps_won'] += row['team_one_map_wins']
        winner_table['maps_lost'] += row['team_two_map_wins']
        winner_table['results'] = winner_table['results'] + [
            {'opponent': loser, 'score': row['team_one_map_wins'] - row['team_two_map_wins']}]

        loser_table = table[loser]
        loser_table['losses'] += 1
        loser_table['maps_won'] += row['team_two_map_wins']
        loser_table['maps_lost'] += row['team_one_map_wins']
        loser_table['results'] = loser_table['results'] + [
            {'opponent': winner, 'score': row['team_two_map_wins'] - row['team_one_map_wins']}]
    else:
        winner = row['team_two']
        loser = row['team_one']

        winner_table = table[winner]
        winner_table['wins'] += 1
        winner_table['maps_won'] += row['team_two_map_wins']
        winner_table['maps_lost'] += row['team_one_map_wins']
        winner_table['results'] = winner_table['results'] + [
            {'opponent': loser, 'score': row['team_two_map_wins'] - row['team_one_map_wins']}]

        loser_table = table[loser]
        loser_table['losses'] += 1
        loser_table['maps_won'] += row['team_one_map_wins']
        loser_table['maps_lost'] += row['team_two_map_wins']
        loser_table['results'] = loser_table['results'] + [
            {'opponent': winner, 'score': row['team_one_map_wins'] - row['team_two_map_wins']}]
    table[winner] = winner_table
    table[loser] = loser_table
    return table

def sort_ties(group):
    if group.shape[0] == 1:
        group['group_rank'] = 1
        return group
    if group.shape[0] == 2:
        return sort_two_way_tie(group)
    else:
        group['group_rank'] = 1
        return group


def sort_two_way_tie(group):
    t2 = group['team'].values[1]
    results = group['results'].values[0]
    diff_arr = [r['score'] for r in results if r['opponent'] == t2]
    diff = diff_arr[0] if len(diff_arr) > 0 else 0
    if diff == 0:
        group['group_rank'] = 1
        return group
    elif diff > 0:
        group['group_rank'] = [2, 1]
        return group
    else:
        group['group_rank'] = [1, 2]
        return group

def sort_table(frame):
    frame = frame.groupby(by=['wins', 'map_differential']).apply(sort_ties).reset_index()
    frame = frame.sort_values(by=['wins', 'map_differential', 'group_rank', 'opponent_points', 'opponent_differential'], ascending=False)
    frame = frame[
        ['team', 'league_points', 'wins', 'losses', 'map_differential', 'maps_won', 'maps_lost']]
    return frame


"""
def calculate_opponent_tie_breakers(table):
    for k in table.keys():
        team_table = table[k]
        opponent_points = 0
        opponent_differential = 0
        for result in team_table['results']:
            opponent_points += table[result['opponent']]['wins']
            opponent_differential += (table[result['opponent']]['maps_won'] - table[result['opponent']]['maps_lost'])
        team_table['opponent_points'] = opponent_points
        team_table['opponent_differential'] = opponent_differential
        team_table['map_differential'] = team_table['maps_won'] - team_table['maps_lost']
        table[k] = team_table
    return table


def sort_table(frame):
    frame = frame.sort_values(by=['wins', 'map_differential', 'opponent_points', 'opponent_differential'],
                              ascending=False)
    frame = frame[
        ['team', 'wins', 'losses', 'map_differential', 'maps_won', 'maps_lost', 'opponent_points',
         'opponent_differential']]
    return frame
"""
