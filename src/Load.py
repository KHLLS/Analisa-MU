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
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    matches_file = os.path.join(BASE_DIR, '..', 'dataset', 'mu_matches_clean.csv')
    transfers_file = os.path.join(BASE_DIR, '..', 'dataset', 'mu_transfers_clean.csv')
    load_matches = Load(matches_file)
    load_transfers = Load(transfers_file)
    print(load_matches.df)
    print(load_transfers.df)