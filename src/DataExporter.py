import json
import os
import pandas as pd
from Matches import Matches
from Transfers import Transfers

class DataExporter:
    def __init__(self, matches_path, transfers_path, seasons):
        self.matches = Matches(matches_path)
        self.transfers = Transfers(transfers_path)
        self.seasons = seasons
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

    def export_all(self):
        all_data = {
            "seasons": {},
            "cumulative_trends": []
        }

        # 1. Process Season Summaries
        for season in self.seasons:
            # Matches Summary
            self.matches.get_data_by_season(season)
            m_sum = self.matches.summary_season()
            
            # Transfers Summary
            t_sum = self.transfers.summary_by_season(season)
            
            # Combine into season key
            all_data["seasons"][season] = {**m_sum, **t_sum}

        # 2. Process Trends (for the line chart)
        # We use the full dataframe from matches to calculate cumulative points
        df_matches = self.matches.df.sort_values('date').copy()
        df_matches['cumulative_points'] = df_matches.groupby('season')['points'].cumsum()
        df_matches['matchweek'] = df_matches.groupby('season').cumcount() + 1
        
        # Select relevant columns for JSON to keep it lightweight
        trend_data = df_matches[['date', 'season', 'matchweek', 'cumulative_points']].to_dict(orient='records')
        all_data["cumulative_trends"] = trend_data

        # 3. Save to JSON
        output_path = os.path.join(self.base_dir, "processed_data.json")
        with open(output_path, "w") as f:
            json.dump(all_data, f, indent=4)
        
        print(f"Data successfully exported to {output_path}")

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    m_path = os.path.join(BASE_DIR, '..', 'dataset', 'mu_matches_clean.csv')
    t_path = os.path.join(BASE_DIR, '..', 'dataset', 'mu_transfers_clean.csv')
    seasons = ['2024-25', '2025-26']
    
    exporter = DataExporter(m_path, t_path, seasons)
    exporter.export_all()
