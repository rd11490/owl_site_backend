from simulate.constants import Teams
import pandas as pd


def calculate_distribution(results):
    dist = []
    results = results[['team', 'rank', 'sim']]
    for t in Teams.West22:
        out = results[results['team'] == t].groupby(['team', 'rank']).count().reset_index()
        out.columns = ['team', 'rank', 'count']
        total = out['count'].sum()
        out['percent'] = 100 * out['count'] / total
        breakdown = {
            'team': t
        }
        playoff_pct = 0
        for i in range(1, 14):
            if i in out['rank'].values:
                breakdown[i] = out[out['rank'] == i]['percent'].values[0]
                if i <= 8:
                    playoff_pct += out[out['rank'] == i]['percent'].values[0]
            else:
                breakdown[i] = 0

        breakdown['qualify'] = playoff_pct
        dist.append(breakdown)

    dist = pd.DataFrame(dist)
    dist = dist.sort_values(by=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], ascending=False)
    return dist
