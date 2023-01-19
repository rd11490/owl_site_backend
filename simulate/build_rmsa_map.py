from simulate.constants import Maps, Teams


def build_rmsa_map(frame):
    rmsa = {
        Maps.Control: {},
        Maps.Hybrid: {},
        Maps.Escort: {},
        Maps.Push: {}
    }
    for index in frame.index:
        row = frame.iloc[index]
        rmsa[row['map_type']][row['team']] = {'attack': row['rmsa attack'], 'attack stdev': row['rmsa attack stdev'],
                                              'defend': row['rmsa defend'], 'defend stdev': row['rmsa defend stdev']}

    return rmsa


def build_rmsa_map_coin_flip():
    rmsa = {
        Maps.Control: {},
        Maps.Hybrid: {},
        Maps.Escort: {},
        Maps.Push: {}
    }
    for t in Teams.West22:
        for m in [Maps.Control, Maps.Escort, Maps.Hybrid, Maps.Push]:
            rmsa[m][t] = {'attack': 0, 'attack stdev': 25,
                          'defend': 0, 'defend stdev': 25}

    return rmsa
