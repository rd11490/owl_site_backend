from simulate.calculate_tournament_table import calculate_tournament_table
from simulate.constants import Teams
from simulate.predict import predict_matches

import pandas as pd

def simulate_qualifiers(to_predict, manual_results, rmsa):
    all_tables = []
    for i in range(0, 100):
        results = predict_matches(to_predict, rmsa)
        results_frame = pd.DataFrame(results)
        all_results = pd.concat([results_frame, manual_results], ignore_index=True)
        all_results['sim'] = i
        table_frame = calculate_tournament_table(all_results)
        table_frame['sim'] = i
        table_frame['rank'] = list(range(1, len(Teams.West22) + 1))
        all_tables.append(table_frame)
    all_tables = pd.concat(all_tables, axis=0)
    return all_tables