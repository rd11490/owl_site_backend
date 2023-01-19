import numpy as np

from simulate.constants import Maps

map_rotation = [Maps.Control, Maps.Hybrid, Maps.Escort, Maps.Push, Maps.Control]

def predict_matches(schedule, rmsa_for_lookup):
    results_arr = []
    for ind in schedule.index:
        match = schedule.loc[ind, :]
        match_result = predict_match(match['team_one'], match['team_two'], map_rotation, rmsa_for_lookup, 3)
        results_arr.append(match_result)
    return results_arr

def predict_match(team_one, team_two, map_order, rmsa, maps_to_win=3):
    # initialize each team to have 0 projected wins
    team_one_projected_wins = 0
    team_two_projected_wins = 0

    projected_winner = None
    loser = None

    # iterate over the game mode order, determine the expected winner of the game mode, increment wins, and continue
    # until one team reaches 3 wins
    for map_type in map_order:
        team_one_attack = rmsa[map_type][team_one]['attack']
        team_one_attack_stdev = rmsa[map_type][team_one]['attack stdev']
        team_one_defend = rmsa[map_type][team_one]['defend']
        team_one_defend_stdev = rmsa[map_type][team_one]['defend stdev']

        team_two_attack = rmsa[map_type][team_two]['attack']
        team_two_attack_stdev = rmsa[map_type][team_two]['attack stdev']
        team_two_defend = rmsa[map_type][team_two]['defend']
        team_two_defend_stdev = rmsa[map_type][team_two]['defend stdev']

        team_one_attack_estimate = np.random.normal(team_one_attack, team_one_attack_stdev)
        team_one_defend_estimate = np.random.normal(team_one_defend, team_one_defend_stdev)

        team_two_attack_estimate = np.random.normal(team_two_attack, team_two_attack_stdev)
        team_two_defend_estimate = np.random.normal(team_two_defend, team_two_defend_stdev)

        # estimate the map score for each team on the map
        team_one_attack_expected = team_one_attack_estimate - team_two_defend_estimate
        team_two_attack_expected = team_two_attack_estimate - team_one_defend_estimate

        # use estimated map score to determine the map winner
        if team_one_attack_expected > team_two_attack_expected:
            team_one_projected_wins += 1
        else:
            team_two_projected_wins += 1

        # break once a team reaches 3 map wins
        if team_one_projected_wins >= maps_to_win:
            projected_winner = team_one
            loser = team_two
            break

        if team_two_projected_wins >= maps_to_win:
            projected_winner = team_two
            loser = team_one
            break
    return {
        'team_one': team_one,
        'team_one_map_wins': team_one_projected_wins,
        'team_two': team_two,
        'team_two_map_wins': team_two_projected_wins,
        'winner': projected_winner,
        'loser': loser
    }