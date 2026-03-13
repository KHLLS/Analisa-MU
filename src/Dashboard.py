import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import json
from Transfers import Transfers, Paid, Loan
from MatchManager import MatchManager
from DataExporter import DataExporter

st.set_page_config(page_title="MU Analysis & Management", layout="wide")

# Paths
MATCHES_JSON = 'matches_records.json'
JSON_PATH = 'processed_data.json'
TRANSFERS_PATH = '../dataset/mu_transfers_clean.csv'
MATCHES_CSV = '../dataset/mu_matches_clean.csv'
SEASONS = ['2024-25', '2025-26']

def regenerate():
    exporter = DataExporter(MATCHES_JSON, TRANSFERS_PATH, SEASONS)
    exporter.export_all()

def load_json_data():
    if os.path.exists(JSON_PATH):
        with open(JSON_PATH, 'r') as f:
            return json.load(f)
    return None

# Init MatchManager
manager = MatchManager("matches_records.json")
if not manager.data:
    manager.import_from_csv(MATCHES_CSV)
    regenerate()

all_data  = load_json_data()
transfers = Transfers(TRANSFERS_PATH)

# Sidebar
with st.sidebar:
    st.title("MU Analysis Tool")
    menu = st.radio("Menu Utama", ["📊 Analysis Dashboard", "⚙️ Manage Matches (CRUD)"])
    st.divider()
    if menu == "📊 Analysis Dashboard":
        selected_season = st.selectbox("Choose Season", SEASONS)
    st.caption("Data: Transfermarkt + Premier League | 2024–2026")

# MENU: ANALYSIS DASHBOARD
if menu == "📊 Analysis Dashboard":
    if not all_data:
        st.error("Processed data not found. Please run DataExporter.py first.")
        if st.button("Generate Data Sekarang"):
            regenerate()
            st.rerun()
        st.stop()

    st.title("Manchester United — Transfer & Performance Analysis")
    st.caption(f"Premier League · Season {selected_season}")
    st.divider()

    season_data  = all_data['seasons'].get(selected_season, {})
    all_summaries = [v for k, v in all_data['seasons'].items()]
    df_summary   = pd.DataFrame(all_summaries)
    goal_transfers = transfers.summary_by_season(selected_season)

    # KPI
    st.subheader(f"Summary Season {selected_season}")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Match",  season_data.get('total_match', 0))
    c2.metric("Total Points", season_data.get('total_points', 0))
    c3.metric("Total Spend",  f"£{season_data.get('total_spend', 0):.2f}m")
    c4.metric("Net Spend",    f"£{season_data.get('net_spend', 0):.2f}m")
    c5.metric("Goals From Transfers Player", f"{goal_transfers['goal']}")

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Goals",    season_data.get('total_goals_for', 0))
    c2.metric("Win Rate", f"{season_data.get('win_rate', 0):.2f}%")
    c3.metric("Wins",     season_data.get('wins', 0))
    c4.metric("Losses",   season_data.get('losses', 0))
    c5.metric("Draws",    season_data.get('draws', 0))
    st.divider()

    # Performance
    st.subheader("Performance per Season")
    col1, col2 = st.columns(2)
    with col1:
        fig_points = px.bar(df_summary, x='season', y='total_points', color='season',
            text='total_points', title='Total Points per Season',
            color_discrete_sequence=['#da291c', '#ffd700'])
        st.plotly_chart(fig_points, width='stretch')
    with col2:
        fig_wdl = go.Figure()
        for season, color in zip(SEASONS, ['#da291c', '#ffd700']):
            row = df_summary[df_summary['season'] == season].iloc[0]
            fig_wdl.add_trace(go.Bar(name=season, x=['Win', 'Draw', 'Lose'],
                y=[row['wins'], row['draws'], row['losses']], marker_color=color))
        fig_wdl.update_layout(barmode='group', title='W/D/L per Season')
        st.plotly_chart(fig_wdl, width='stretch')

    df_trend = pd.DataFrame(all_data['cumulative_trends'])
    fig_trend = px.line(df_trend, x='matchweek', y='cumulative_points', color='season',
        markers=True, title='Cumulative Points Trend per Matchweek',
        color_discrete_sequence=['#da291c', '#ffd700'])
    st.plotly_chart(fig_trend, width='stretch')
    st.divider()

    # Correlation
    st.subheader("Correlation Transfer vs Performance")
    col1, col2 = st.columns(2)
    with col1:
        fig_corr = px.scatter(df_summary, x='net_spend', y='total_points', color='season',
            size='total_spend', text='season', title='Net Spend vs Total Points',
            color_discrete_sequence=['#da291c', '#ffd700'])
        st.plotly_chart(fig_corr, width='stretch')
    with col2:
        fig_spend = px.bar(df_summary, x='season', y=['total_spend', 'total_income'],
            barmode='group', title='Spend vs Income per Season',
            color_discrete_map={'total_spend': '#da291c', 'total_income': '#2ecc71'})
        st.plotly_chart(fig_spend, width='stretch')
    st.divider()

    # Transfer Breakdown
    st.subheader("Breakdown Transfer Paid vs Loan")
    df_trx = transfers.df[transfers.df['season'] == selected_season]
    col1, col2 = st.columns(2)
    with col1:
        fee_type_count = df_trx.groupby('fee_type')['player_name'].count().reset_index()
        fig_pie = px.pie(fee_type_count, names='fee_type', values='player_name',
            title=f'Transfer Composition — {selected_season}',
            color_discrete_sequence=['#da291c', '#ffd700', '#888'])
        st.plotly_chart(fig_pie, width='stretch')
    with col2:
        paid_df = df_trx[df_trx['fee_type'] == 'Paid'].dropna(subset=['fee_million_gbp'])
        if not paid_df.empty:
            fig_paid = px.bar(paid_df.sort_values('fee_million_gbp'),
                x='fee_million_gbp', y='player_name', color='transfer_type', orientation='h',
                title=f'Paid Transfer Fee — {selected_season}',
                color_discrete_map={'In': '#da291c', 'Out': '#2ecc71'})
            st.plotly_chart(fig_paid, width='stretch')

# MENU: MANAGE MATCHES (CRUD)
else:
    st.title("⚙️ Match Records Management (CRUD)")
    st.caption("Add, view, edit, and delete match data directly in the JSON file.")
    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs(["🆕 Create", "📝 Update", "📖 Read", "🗑️ Delete"])

    # CREATE
    with tab1:
        st.subheader("Add New Match")
        with st.form("create_form"):
            c1, c2 = st.columns(2)
            d_date   = c1.date_input("Match Date")
            d_season = c2.selectbox("Season", SEASONS)
            d_opp    = c1.text_input("Opponent")
            d_ha     = c2.selectbox("Home/Away", ["Home", "Away"])
            d_gf     = c1.number_input("MU Goals", min_value=0, step=1)
            d_ga     = c2.number_input("Opponent Goals", min_value=0, step=1)

            submitted = st.form_submit_button("Save Match")
            if submitted:
                str_date = str(d_date)
                res = "W" if d_gf > d_ga else ("D" if d_gf == d_ga else "L")
                pts = 3 if res == "W" else (1 if res == "D" else 0)
                new_data = {
                    "season": d_season, "opponent": d_opp, "home_away": d_ha,
                    "goals_for": int(d_gf), "goals_against": int(d_ga),
                    "result": res, "points": int(pts)
                }
                if manager.create(str_date, new_data):
                    regenerate()
                    st.success(f"Match on {str_date} saved! Dashboard updated.")
                    st.rerun()
                else:
                    st.error(f"Failed: Data for {str_date} already exists.")

    # UPDATE
    with tab2:
        st.subheader("Edit Match Data")
        all_dates = sorted(list(manager.data.keys()), reverse=True)
        selected_date = st.selectbox("Select Date to Edit", all_dates)

        if selected_date:
            curr = manager.data[selected_date]
            st.info(f"Editing match vs {curr.get('opponent', 'Unknown')} on {selected_date}")

            with st.form("update_form"):
                u_gf  = st.number_input("MU Goals", value=int(curr.get('goals_for', 0)), min_value=0)
                u_ga  = st.number_input("Opponent Goals", value=int(curr.get('goals_against', 0)), min_value=0)
                u_opp = st.text_input("Opponent", value=curr.get('opponent', ''))

                update_submitted = st.form_submit_button("Update Data")
                if update_submitted:
                    res = "W" if u_gf > u_ga else ("D" if u_gf == u_ga else "L")
                    pts = 3 if res == "W" else (1 if res == "D" else 0)
                    update_payload = {
                        "opponent": u_opp, "goals_for": int(u_gf),
                        "goals_against": int(u_ga), "result": res, "points": int(pts)
                    }
                    if manager.update(selected_date, update_payload):
                        regenerate()
                        st.success("Data updated! Dashboard updated.")
                        st.rerun()

    # READ
    with tab3:
        st.subheader("All Match Records")
        if manager.data:
            df_json = pd.DataFrame.from_dict(manager.data, orient='index')
            df_json.index.name = "Date"
            st.dataframe(df_json.sort_index(ascending=False), use_container_width=True)
            st.caption(f"Total records: {len(manager.data)}")
        else:
            st.write("No data found in JSON.")

    # DELETE
    with tab4:
        st.subheader("Delete Match Data")
        all_dates_del = sorted(list(manager.data.keys()), reverse=True)

        if all_dates_del:
            del_date = st.selectbox("Select Date to Delete", all_dates_del, key="del")

            if del_date:
                curr_del = manager.data.get(del_date, {})
                st.warning(f"You are about to delete: **{del_date}** vs **{curr_del.get('opponent', 'Unknown')}** — Result: {curr_del.get('result', 'N/A')}")

            if st.button("🗑️ Delete", type="primary"):
                if manager.delete(del_date):
                    regenerate()
                    st.success(f"Data for {del_date} deleted! Dashboard updated.")
                    st.rerun()
        else:
            st.write("No data available to delete.")

