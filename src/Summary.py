from Transfers import Transfers
from Matches import Matches
import pandas as pd

class Summary:
    def __init__(self,trx_file,matches_file,season):
        self.transfers = Transfers(trx_file)
        self.matches = Matches(matches_file)
        self.season = season

    def get_matches(self):
        df_matches = pd.DataFrame(self.matches.get_data_by_season(self.season))
        return df_matches
    
    def get_matches_summary(self):
        df_matches_summary = self.matches.summary_season()
        df = pd.DataFrame([df_matches_summary])
        return df
    
    def get_transfers_summary(self):
        df_transfers_summary = self.transfers.summary_by_season(self.season)
        df = pd.DataFrame([df_transfers_summary])
        return df
    
summ = Summary(trx_file='../dataset/mu_transfers_clean.csv',matches_file='../dataset/mu_matches_clean.csv',season='2024-25')
# print(summ.get_matches())
# print(summ.get_matches_summary())
print(f'transfers summary: {summ.get_transfers_summary()}')
        