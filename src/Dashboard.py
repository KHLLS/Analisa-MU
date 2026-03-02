import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import json
from Transfers import Transfers, Paid, Loan
from MatchManager import MatchManager

st.set_page_config(page_title="MU Analysis & Management", layout="wide")

# Paths & Initialization
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, 'processed_data.json')
TRANSFERS_PATH = os.path.join(BASE_DIR, '..', 'dataset', 'mu_transfers_clean.csv')
MATCHES_CSV = os.path.join(BASE_DIR, '..', 'dataset', 'mu_matches_clean.csv')
SEASONS = ['2024-25', '2025-26']

manager = MatchManager("matches_records.json")
# Inisialisasi data jika JSON masih kosong
if not manager.data:
    manager.import_from_csv(MATCHES_CSV)

@st.cache_data
def load_json_data():
    if os.path.exists(JSON_PATH):
        with open(JSON_PATH, 'r') as f:
            return json.load(f)
    return None

all_data = load_json_data()
transfers = Transfers(TRANSFERS_PATH)

# Sidebar Navigation
with st.sidebar:
    st.title("MU Analysis Tool")
    menu = st.radio("Menu Utama", ["📊 Analysis Dashboard", "⚙️ Manage Matches (CRU)"])
    st.divider()
    
    if menu == "📊 Analysis Dashboard":
        selected_season = st.selectbox("Choose Season", SEASONS)
    st.caption("Data: Transfermarkt + Premiere League| 2024–2026")

# --- MENU: ANALYSIS ---
if menu == "📊 Analysis Dashboard":
    if not all_data:
        st.error("Processed data file not found. Please run 'DataExporter.py' first.")
        st.stop()

    st.title("Manchester United — Transfer & Performance Analysis")
    st.caption(f"Premier League · Season {selected_season}")
    st.divider()

    # Get Season Summary (from JSON)
    season_data = all_data['seasons'].get(selected_season, {})
    all_summaries = [v for k, v in all_data['seasons'].items()]
    df_summary = pd.DataFrame(all_summaries)

    # Summary Section
    st.subheader(f"Summary Season {selected_season}")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Match", season_data.get('total_match', 0))
    c2.metric("Total Poin", season_data.get('total_points', 0))
    c3.metric("Total Spend", f"£{season_data.get('total_spend', 0):.2f}m")
    c4.metric("Net Spend", f"£{season_data.get('net_spend', 0):.2f}m")

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Goal", season_data.get('total_goals_for', 0))
    c2.metric("Win Rate", f"{season_data.get('win_rate', 0):.2f}%")
    c3.metric("Win", season_data.get('wins', 0))
    c4.metric("Total Lose", season_data.get('losses', 0))
    c5.metric("Total Draw", season_data.get('draws', 0))
    st.divider()

    # Visualisations
    st.subheader("Performance per Season")
    col1, col2 = st.columns(2)
    with col1:
        fig_points = px.bar(df_summary, x='season', y='total_points', color='season',
            text='total_points', title='Total Points per Season',
            color_discrete_sequence=['#da291c', '#ffd700'])
        st.plotly_chart(fig_points, use_container_width=True)

    with col2:
        fig_wdl = go.Figure()
        for season, color in zip(SEASONS, ['#da291c', '#ffd700']):
            row = df_summary[df_summary['season'] == season].iloc[0]
            fig_wdl.add_trace(go.Bar(name=season, x=['Win', 'Draw', 'Lose'],
                y=[row['wins'], row['draws'], row['losses']], marker_color=color))
        fig_wdl.update_layout(barmode='group', title='W/D/L per Musim')
        st.plotly_chart(fig_wdl, use_container_width=True)

    df_trend = pd.DataFrame(all_data['cumulative_trends'])
    fig_trend = px.line(df_trend, x='matchweek', y='cumulative_points', color='season',
        markers=True, title='Cumulative Points Trend per Matchweek',
        color_discrete_sequence=['#da291c', '#ffd700'])
    st.plotly_chart(fig_trend, use_container_width=True)
    st.divider()

    # Correlation & Transfer Breakdown
    st.subheader("Correlation Transfer vs Performa")
    col1, col2 = st.columns(2)
    with col1:
        fig_corr = px.scatter(df_summary, x='net_spend', y='total_points', color='season',
            size='total_spend', text='season', title='Net Spend vs Total Poin',
            color_discrete_sequence=['#da291c', '#ffd700'])
        st.plotly_chart(fig_corr, use_container_width=True)
    with col2:
        fig_spend = px.bar(df_summary, x='season', y=['total_spend', 'total_income'],
            barmode='group', title='Spend vs Income per Musim',
            color_discrete_map={'total_spend': '#da291c', 'total_income': '#2ecc71'})
        st.plotly_chart(fig_spend, use_container_width=True)
    st.divider()

    st.subheader("Breakdown Transfer Paid vs Loan")
    df_trx = transfers.df[transfers.df['season'] == selected_season]
    col1, col2 = st.columns(2)
    with col1:
        fee_type_count = df_trx.groupby('fee_type')['player_name'].count().reset_index()
        fig_pie = px.pie(fee_type_count, names='fee_type', values='player_name',
            title=f'Komposition Transfer — {selected_season}',
            color_discrete_sequence=['#da291c', '#ffd700', '#888'])
        st.plotly_chart(fig_pie, use_container_width=True)
    with col2:
        paid_df = df_trx[df_trx['fee_type'] == 'Paid'].dropna(subset=['fee_million_gbp'])
        if not paid_df.empty:
            fig_paid = px.bar(paid_df.sort_values('fee_million_gbp'),
                x='fee_million_gbp', y='player_name', color='transfer_type', orientation='h',
                title=f'Fee Transfer Paid — {selected_season}',
                color_discrete_map={'In': '#da291c', 'Out': '#2ecc71'})
            st.plotly_chart(fig_paid, use_container_width=True)

# --- MENU: MANAGE MATCHES (CRU) ---
else:
    st.title("⚙️ Match Records Management (JSON)")
    st.caption("Gunakan menu ini untuk Menambah, Melihat, dan Mengubah data pertandingan langsung di file JSON.")
    st.divider()

    tab1, tab2, tab3 = st.tabs(["🆕 Create Match", "📝 Update Match", "📖 View All Data"])

    # --- TAB 1: CREATE ---
    with tab1:
        st.subheader("Tambah Pertandingan Baru")
        with st.form("create_form"):
            c1, c2 = st.columns(2)
            d_date = c1.date_input("Tanggal Pertandingan")
            d_season = c2.selectbox("Musim", SEASONS)
            d_opp = c1.text_input("Lawan")
            d_ha = c2.selectbox("Home/Away", ["Home", "Away"])
            d_gf = c1.number_input("Gol MU", min_value=0, step=1)
            d_ga = c2.number_input("Gol Lawan", min_value=0, step=1)
            
            submitted = st.form_submit_button("Simpan Pertandingan")
            if submitted:
                str_date = str(d_date)
                # Hitung hasil & poin secara otomatis
                res = "W" if d_gf > d_ga else ("D" if d_gf == d_ga else "L")
                pts = 3 if res == "W" else (1 if res == "D" else 0)
                
                new_data = {
                    "season": d_season, "opponent": d_opp, "home_away": d_ha,
                    "goals_for": int(d_gf), "goals_against": int(d_ga),
                    "result": res, "points": int(pts)
                }
                
                if manager.create(str_date, new_data):
                    st.success(f"Data Berhasil Disimpan untuk tanggal {str_date}!")
                else:
                    st.error(f"Gagal: Data tanggal {str_date} sudah ada.")

    # --- TAB 2: UPDATE ---
    with tab2:
        st.subheader("Edit Data Pertandingan")
        all_dates = sorted(list(manager.data.keys()), reverse=True)
        selected_date = st.selectbox("Pilih Tanggal yang ingin diubah", all_dates)
        
        if selected_date:
            curr = manager.data[selected_date]
            st.info(f"Mengubah data lawan {curr['opponent']} ({selected_date})")
            
            with st.form("update_form"):
                u_gf = st.number_input("Gol MU", value=int(curr['goals_for']), min_value=0)
                u_ga = st.number_input("Gol Lawan", value=int(curr['goals_against']), min_value=0)
                u_opp = st.text_input("Lawan", value=curr['opponent'])
                
                update_submitted = st.form_submit_button("Perbarui Data")
                if update_submitted:
                    res = "W" if u_gf > u_ga else ("D" if u_gf == u_ga else "L")
                    pts = 3 if res == "W" else (1 if res == "D" else 0)
                    
                    update_payload = {
                        "opponent": u_opp, "goals_for": int(u_gf), 
                        "goals_against": int(u_ga), "result": res, "points": int(pts)
                    }
                    if manager.update(selected_date, update_payload):
                        st.success("Data berhasil diperbarui!")
                        st.rerun()

    # --- TAB 3: READ ---
    with tab3:
        st.subheader("Daftar Record di JSON")
        if manager.data:
            df_json = pd.DataFrame.from_dict(manager.data, orient='index')
            df_json.index.name = "Date"
            st.dataframe(df_json.sort_index(ascending=False), use_container_width=True)
        else:
            st.write("Belum ada data di JSON.")