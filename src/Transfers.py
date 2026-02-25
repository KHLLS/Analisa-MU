import pandas as pd
from Load import Load
import os


class Transfers:
    def __init__(self,dataset):
        self.dataset = Load(dataset)
        self.df = self.dataset.df

    def get_info(self,season,trx_type):
        df = self.df
        df_filtered = df[
            (df['fee_type'] == self.__class__.__name__) &
            (df['season'] == season) &
            (df['transfer_type'] == trx_type)
            ]
        return df_filtered

class Paid(Transfers):
    def __init__(self, dataset):
        super().__init__(dataset)

class Loan(Transfers):
    def __init__(self, dataset):
        super().__init__(dataset)
    
    # def summary(self):
    #     pass
        

paid  = Paid('../dataset/mu_transfers_clean.csv')
loan  = Loan('../dataset/mu_transfers_clean.csv')
# load  = Load()
# print(Trx.d)
print(paid.get_info(season='2025-26',trx_type='In'))
print(loan.get_info(season='2025-26',trx_type='Out'))
