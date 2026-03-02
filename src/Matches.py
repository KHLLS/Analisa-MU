from Load import Load
import pandas as pd
import json
import os

class Matches:
    def __init__(self,dataset):
        self.dataset = Load(dataset)
        self.df = self.dataset.df
        self.df_filter = self.df

    def get_data_by_season(self,season):
        self.season = season
        df = self.df_filter
        self.df_filtered = df[df['season'] == self.season]
        return self.df_filtered
    
    def summary_season(self):
        total_match = len(self.df_filtered)
        total_goals_for = self.df_filtered['goals_for'].sum()
        total_goals_against = self.df_filtered['goals_against'].sum()
        total_wins = len(self.df_filtered[self.df_filtered['result'] == 'W'])
        total_draws = len(self.df_filtered[self.df_filtered['result'] == 'D'])
        total_losses = len(self.df_filtered[self.df_filtered['result'] == 'L'])
        total_points = int(self.df_filtered['points'].sum())
        win_rate = (total_wins / total_match) * 100 if total_match > 0 else 0

        data = {
            'season': self.season,
            'type': self.__class__.__name__,
            'total_match': total_match,
            'total_goals_for': int(total_goals_for),
            'total_goals_against': int(total_goals_against),
            'wins': total_wins,
            'draws': total_draws,
            'losses': total_losses,
            'total_points': total_points,
            'win_rate':win_rate
        }

        return data


class Home(Matches):
    def __init__(self, dataset):
        super().__init__(dataset)
        self.df_filter = self.df[self.df['home_away'] == self.__class__.__name__]

class Away(Matches):
    def __init__(self, dataset):
        super().__init__(dataset)
        self.df_filter = self.df[self.df['home_away'] == self.__class__.__name__]

if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    matches_file = os.path.join(BASE_DIR, '..', 'dataset', 'mu_matches_clean.csv')
    home = Home(matches_file)
    print(home.get_data_by_season('2025-26'))
    print(home.summary_season())
