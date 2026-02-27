import pandas as pd
from Load import Load


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

    def summary_by_season(self,season):
        df = self.df
        df_filtered = df[df['season'] == season]
        total_in = len(df_filtered[df_filtered['transfer_type'] == 'In'])
        total_out = len(df_filtered[df_filtered['transfer_type'] == 'Out'])
        total_spend = df_filtered[df_filtered['transfer_type'] == 'In']['fee_million_gbp'].sum()
        total_income = df_filtered[df_filtered['transfer_type'] == 'Out']['fee_million_gbp'].sum()
        net_spend = total_spend - total_income

        return {
            'season': season,
            'total_player_in': total_in,
            'total_player_out': total_out,
            'total_spend': total_spend,
            'total_income': total_income,
            'net_spend': net_spend
        }
    
class Paid(Transfers):
    def __init__(self, dataset):
        super().__init__(dataset)

class Loan(Transfers):
    def __init__(self, dataset):
        super().__init__(dataset)

if __name__ == '__main__':
    paid  = Paid('../dataset/mu_transfers_clean.csv')
    loan  = Loan('../dataset/mu_transfers_clean.csv')
    # print(paid.get_info(season='2025-26',trx_type='In'))
    print(paid.summary_by_season('2024-25'))
    # print(loan.get_info(season='2025-26',trx_type='Out'))
