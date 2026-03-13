# MU Transfer & Performance Analysis (OOP EDA)

Proyek ini adalah aplikasi analisis data (Exploratory Data Analysis) menggunakan paradigma Pemrograman Berorientasi Objek (OOP) untuk menganalisis hubungan antara aktivitas transfer pemain Manchester United dengan performa mereka di lapangan selama musim 2024-2026.

## Struktur Proyek

```text
OOP_EDA/
├── dataset/                # File CSV mentah dan bersih
│   ├── mu_matches_clean.csv
│   └── mu_transfers_clean.csv
├── src/                    # Source code Python
│   ├── Dashboard.py        # Antarmuka utama (Streamlit)
│   ├── DataExporter.py     # Script untuk ekspor data ke JSON
│   ├── Load.py             # Class untuk memuat data dari CSV
│   ├── Matches.py          # Logika bisnis untuk data pertandingan
│   ├── Transfers.py        # Logika bisnis untuk data transfer
│   ├── Summary.py          # Class pembantu untuk ringkasan data
│   └── processed_data.json # Hasil ekspor data terpadu
└── README.md
```

## Penjelasan File

### 1. `src/Load.py`
File ini berisi class `Load` yang bertanggung jawab untuk membaca file CSV. Ini adalah layer dasar yang menangani error jika file tidak ditemukan.

### 2. `src/Matches.py`
Berisi class `Matches` dan turunannya (`Home`, `Away`).
*   **Fungsi:** Menghitung statistik pertandingan seperti total poin, *win rate*, gol, dan hasil (W/D/L).
*   **OOP:** Menggunakan *inheritance* untuk memisahkan logika pertandingan kandang dan tandang.

### 3. `src/Transfers.py`
Berisi class `Transfers` dan turunannya (`Paid`, `Loan`).
*   **Fungsi:** Menghitung pengeluaran transfer (*spend*), pendapatan (*income*), dan pengeluaran bersih (*net spend*).
*   **OOP:** Memisahkan tipe transfer berdasarkan biaya (berbayar atau pinjaman).

### 4. `src/DataExporter.py`
Script ini bertindak sebagai pengolah data pusat.
*   **Fungsi:** Menggabungkan logika dari `Matches` dan `Transfers` untuk menghasilkan satu file `processed_data.json`.
*   **Kegunaan:** Mempercepat Dashboard karena data berat sudah dihitung sebelumnya dan disimpan dalam format JSON.

### 5. `src/Dashboard.py`
Aplikasi visualisasi utama menggunakan **Streamlit**.
*   **Fitur:**
    *   Filter berdasarkan musim.
    *   Metrik performa (Poin, Win Rate, Spend).
    *   Grafik tren poin kumulatif.
    *   Analisis korelasi antara belanja pemain dan poin.
    *   Detail breakdown transfer (langsung dari CSV untuk detail pemain).

### 6. `src/Summary.py`
Class utilitas untuk mengambil ringkasan gabungan antara transfer dan performa dalam format DataFrame.

---

## Cara Menjalankan

### 1. Persiapan Data
Pastikan data terbaru sudah diekspor ke format JSON dengan menjalankan:
```bash
python src/DataExporter.py
```

### 2. Menjalankan Dashboard
Jalankan perintah berikut di terminal:
```bash
streamlit run src/Dashboard.py
```

## Teknologi yang Digunakan
*   **Python**: Bahasa pemrograman utama.
*   **Streamlit**: Framework untuk dashboard interaktif.
*   **Pandas**: Manipulasi dan analisis data.
*   **Plotly**: Library grafik interaktif.
*   **JSON**: Format penyimpanan data hasil olahan.
