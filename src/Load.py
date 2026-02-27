import pandas as pd
import os

class Load:
    def __init__(self,dataset):
        self.dataset = dataset
        self.df = self.load_data()
        
    def load_data(self):
        if os.path.exists(self.dataset):
            try:
                df = pd.read_csv(self.dataset)
                return df
            except Exception as e:
                print(f"error: {e}")
        else:
            print('Dataset Not Found')

if __name__ == '__main__':
    load_matches = Load('../dataset/mu_matches_clean.csv')
    load_transfers = Load('../dataset/mu_transfers_clean.csv')
    print(load_matches.df)
    print(load_transfers.df)