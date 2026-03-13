import json
import os
import pandas as pd

class MatchManager:
    def __init__(self, json_filename="matches_records.json"):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.json_path = os.path.join(self.base_dir, json_filename)
        self.data = self._load_json()

    def _load_json(self):
        if os.path.exists(self.json_path):
            with open(self.json_path, 'r') as f:
                return json.load(f)
        return {}

    def _save_json(self):
        with open(self.json_path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def import_from_csv(self, csv_path):
        if not os.path.exists(csv_path):
            print(f"Error: File {csv_path} tidak ditemukan.")
            return

        df = pd.read_csv(csv_path)
        if 'date' not in df.columns:
            print("Error: Kolom 'date' tidak ditemukan di CSV.")
            return

        records = df.set_index('date').to_dict(orient='index')
        self.data.update(records)
        self._save_json()
        print(f"Berhasil mengimpor {len(records)} data dari CSV ke JSON.")

    def create(self, date, match_details):
        if date in self.data:
            print(f"Gagal: Data untuk tanggal {date} sudah ada. Gunakan update().")
            return False
        
        self.data[date] = match_details
        self._save_json()
        print(f"Data baru berhasil ditambahkan untuk tanggal: {date}")
        return True
    
    def read(self, date=None):
        if date:
            return self.data.get(date, "Data tidak ditemukan.")
        return self.data

    def update(self, date, new_details):
        if date not in self.data:
            print(f"Gagal: Data untuk tanggal {date} tidak ditemukan.")
            return False

        self.data[date].update(new_details)
        self._save_json()
        print(f"Data untuk tanggal {date} berhasil diperbarui.")
        return True
    
    def delete(self,date):
        if date not in self.data:
            print(f"Gagal: Data untuk tanggal {date} tidak ditemukan.")
            return False
        del self.data[date]
        self._save_json()
        return True


if __name__ == "__main__":
    manager = MatchManager()
    
    csv_file = os.path.join(os.path.dirname(__file__), '..', 'dataset', 'mu_matches_clean.csv')
    if not manager.data: 
        manager.import_from_csv(csv_file)

    new_match = {
        "season": "2025-26",
        "opponent": "Liverpool",
        "home_away": "Away",
        "goals_for": 2,
        "goals_against": 1,
        "result": "W",
        "points": 3
    }
    # manager.create("2026-03-05", new_match)

    print("Cek Data Tanggal 2026-03-05:")
    print(manager.read("2026-03-05"))

    update_data = {
        "goals_for": 3,
        "result": "W"
    }
    # manager.update("2026-03-05", update_data)
    
    print("Data Sebelum Delete:")
    print(manager.read("2026-03-05"))

    manager.delete("2026-03-05")
    print("Data Setelah Delete:")
    print(manager.read("2026-03-05"))

