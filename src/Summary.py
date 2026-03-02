import os
from Transfers import Transfers
from Matches import Matches
import pandas as pd

class Summary:
    def __init__(self,trx_file,matches_file,season):
        self.transfers = Transfers(trx_file)
        self.matches = Matches(matches_file)
        self.season = season
        # Pre-filter matches for the given season
        self.matches.get_data_by_season(self.season)

    def get_matches(self):
        return self.matches.df_filtered
    
    def get_matches_summary(self):
        df_matches_summary = self.matches.summary_season()
        df = pd.DataFrame([df_matches_summary])
        return df
    
    def get_transfers_summary(self):
        df_transfers_summary = self.transfers.summary_by_season(self.season)
        df = pd.DataFrame([df_transfers_summary])
        return df
    
if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    trx_file = os.path.join(BASE_DIR, '..', 'dataset', 'mu_transfers_clean.csv')
    matches_file = os.path.join(BASE_DIR, '..', 'dataset', 'mu_matches_clean.csv')
    summ = Summary(trx_file=trx_file, matches_file=matches_file, season='2024-25')
    # print(summ.get_matches())
    print(f'matches summary: {summ.get_matches_summary()}')
    print(f'transfers summary: {summ.get_transfers_summary()}')
        