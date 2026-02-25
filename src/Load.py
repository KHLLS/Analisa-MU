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