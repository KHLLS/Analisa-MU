import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from Matches import Matches, Home, Away
from Transfers import Transfers, Paid, Loan

st.set_page_config(page_title="MU Transfer Analysis", layout="wide")

# Path Dataset
MATCHES_PATH = '../dataset/mu_matches_clean.csv'
TRANSFERS_PATH = '../dataset/mu_transfers_clean.csv'
SEASONS = ['2024-25', '2025-26']

def load_all():
    return (
        Matches(MATCHES_PATH),
        Home(MATCHES_PATH),
        Away(MATCHES_PATH),
        Transfers(TRANSFERS_PATH),
        Paid(TRANSFERS_PATH),
        Loan(TRANSFERS_PATH)
    )

matches, home, away, transfers, paid, loan = load_all()

# Sidebar
with st.sidebar:
    st.title("MU Transfer Analysis")
    st.divider()
    selected_season = st.selectbox("Choose Season", SEASONS)
    st.divider()
    st.caption("Data: Transfermarkt + Premiere League| 2024–2026")

# Header
st.title("Manchester United — Transfer & Performance Analysis")
st.caption(f"Premier League · Season {selected_season}")
st.divider()

# Get Module
matches.get_data_by_season(selected_season)
home.get_data_by_season(selected_season)
away.get_data_by_season(selected_season)
m_sum = matches.summary_season()
trx_sum = transfers.summary_by_season(selected_season)

all_summaries = []
for s in SEASONS:
    matches.get_data_by_season(s)
    sm = matches.summary_season()
    trx = transfers.summary_by_season(s)
    all_summaries.append({**sm, **trx})
df_summary = pd.DataFrame(all_summaries)
matches.get_data_by_season(selected_season)

# Summary Section
st.subheader(f"Summary Season {selected_season}")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Match", m_sum['total_match'])
c2.metric("Total Poin", m_sum['total_points'])
c3.metric("Total Spend", f"£{trx_sum['total_spend']:.2f}m")
c4.metric("Net Spend", f"£{trx_sum['net_spend']:.2f}m")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Goal", m_sum['total_goals_for'])
c2.metric("Win Rate", f"{m_sum['win_rate']:.2f}%")
c3.metric("Win", m_sum['wins'])
c4.metric("Total Lose", m_sum['losses'])
c5.metric("Total Draw", m_sum['draws'])
st.divider()

# Perform Visualisation
st.subheader("Performance per Season")

col1, col2 = st.columns(2)
with col1:
    fig_points = px.bar(df_summary, x='season', y='total_points', color='season',
        text='total_points', title='Total Points per Season',
        color_discrete_sequence=['#da291c', '#ffd700'])
    fig_points.update_traces(textposition='outside')
    fig_points.update_layout(showlegend=False)
    st.plotly_chart(fig_points, use_container_width=True)

with col2:
    fig_wdl = go.Figure()
    for season, color in zip(SEASONS, ['#da291c', '#ffd700']):
        row = df_summary[df_summary['season'] == season].iloc[0]
        fig_wdl.add_trace(go.Bar(name=season, x=['Win', 'Draw', 'Lose'],
            y=[row['wins'], row['draws'], row['losses']], marker_color=color))
    fig_wdl.update_layout(barmode='group', title='W/D/L per Musim')
    st.plotly_chart(fig_wdl, use_container_width=True)

matches_all = matches.df.sort_values('date').copy()
matches_all['cumulative_points'] = matches_all.groupby('season')['points'].cumsum()
matches_all['matchweek'] = matches_all.groupby('season').cumcount() + 1
fig_trend = px.line(matches_all, x='matchweek', y='cumulative_points', color='season',
    markers=True, title='Cumulative Points Trend per Matchweek',
    color_discrete_sequence=['#da291c', '#ffd700'])
st.plotly_chart(fig_trend, use_container_width=True)
st.divider()

# Korelasi 
st.subheader("Correlation Transfer vs Performa")

col1, col2 = st.columns(2)
with col1:
    fig_corr = px.scatter(df_summary, x='net_spend', y='total_points', color='season',
        size='total_spend', text='season', title='Net Spend vs Total Poin',
        color_discrete_sequence=['#da291c', '#ffd700'],
        labels={'net_spend': 'Net Spend (£m)', 'total_points': 'Total Poin'})
    fig_corr.update_traces(textposition='top center')
    fig_corr.update_layout(showlegend=False)
    st.plotly_chart(fig_corr, use_container_width=True)

with col2:
    fig_spend = px.bar(df_summary, x='season', y=['total_spend', 'total_income'],
        barmode='group', title='Spend vs Income per Musim',
        color_discrete_map={'total_spend': '#da291c', 'total_income': '#2ecc71'},
        labels={'value': '£ Juta', 'variable': 'Tipe'})
    st.plotly_chart(fig_spend, use_container_width=True)

fig_winrate = px.bar(df_summary, x='season', y='win_rate', color='season', text='win_rate',
    title='Win Rate per Season (%)', color_discrete_sequence=['#da291c', '#ffd700'])
fig_winrate.update_traces(texttemplate='%{text}%', textposition='outside')
fig_winrate.update_layout(showlegend=False, yaxis=dict(range=[0, 70]))
st.plotly_chart(fig_winrate, use_container_width=True)
st.divider()

# Padi VS Loan
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
            color_discrete_map={'In': '#da291c', 'Out': '#2ecc71'},
            labels={'fee_million_gbp': '£ Million', 'player_name': 'Player'})
        st.plotly_chart(fig_paid, use_container_width=True)

st.subheader(f"Detail Transfer — {selected_season}")
df_detail = df_trx[['player_name', 'position', 'transfer_type', 'fee_type', 'fee_million_gbp', 'club']].copy()
df_detail.columns = ['Player', 'Position', 'Type', 'Fee Type', 'Fee (£m)', 'Club']
st.dataframe(df_detail.reset_index(drop=True), use_container_width=True)