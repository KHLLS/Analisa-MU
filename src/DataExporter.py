import json
import pandas as pd
from Transfers import Transfers

class DataExporter:
    def __init__(self, matches_json_path, transfers_path, seasons):
        self.matches_json_path = matches_json_path
        self.transfers = Transfers(transfers_path)
        self.seasons = seasons

    def _load_matches_df(self):
        with open(self.matches_json_path, 'r') as f:
            data = json.load(f)
        df = pd.DataFrame.from_dict(data, orient='index')
        df.index.name = 'date'
        df = df.reset_index()
        df['date'] = pd.to_datetime(df['date'])
        df['goals_for'] = pd.to_numeric(df['goals_for'], errors='coerce').fillna(0).astype(int)
        df['goals_against'] = pd.to_numeric(df['goals_against'], errors='coerce').fillna(0).astype(int)
        df['points'] = pd.to_numeric(df['points'], errors='coerce').fillna(0).astype(int)
        df['clean_sheet'] = (df['goals_against'] == 0).astype(int)
        return df

    def export_all(self):
        df_matches = self._load_matches_df()
        all_data = {
            "seasons": {},
            "cumulative_trends": []
        }

        # 1. Process Season Summaries
        for season in self.seasons:
            df_season = df_matches[df_matches['season'] == season]
            if df_season.empty:
                continue
            total_match = len(df_season)
            wins   = int((df_season['result'] == 'W').sum())
            draws  = int((df_season['result'] == 'D').sum())
            losses = int((df_season['result'] == 'L').sum())
            points = int(df_season['points'].sum())
            m_sum = {
                'season'              : season,
                'total_match'         : total_match,
                'total_goals_for'     : int(df_season['goals_for'].sum()),
                'total_goals_against' : int(df_season['goals_against'].sum()),
                'wins'                : wins,
                'draws'               : draws,
                'losses'              : losses,
                'total_points'        : points,
                'win_rate'            : round(wins / total_match * 100, 1),
                'clean_sheets'        : int(df_season['clean_sheet'].sum())
            }
            t_sum = self.transfers.summary_by_season(season)
            all_data["seasons"][season] = {**m_sum, **t_sum}

        # 2. Process Trends
        df_sorted = df_matches.sort_values('date').copy()
        df_sorted['date'] = df_sorted['date'].astype(str)
        df_sorted['cumulative_points'] = df_sorted.groupby('season')['points'].cumsum()
        df_sorted['matchweek'] = df_sorted.groupby('season').cumcount() + 1
        all_data["cumulative_trends"] = df_sorted[
            ['date', 'season', 'matchweek', 'cumulative_points']
        ].to_dict(orient='records')

        return all_data  # ← return dict, bukan save ke file
