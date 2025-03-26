import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config(layout="wide")
st.title("Early Six Analyis by Ayush Goel")


df_ballByball = pd.read_csv("ball_data.csv")
df_match = pd.read_csv("match_data.csv")
df_Ball_Batter = pd.read_csv("ball_data.csv")

batting_team = st.selectbox("Choose Batting Team",df_ballByball["BattingTeam"].unique())

df_ballByball = df_ballByball[df_ballByball["BattingTeam"] == batting_team]

num_unique_ids = df_ballByball["ID"].nunique()
st.write("Total Number of Matches :",num_unique_ids)

df_grouped = df_ballByball.groupby(["ID", "Overs"], as_index=False).agg({"TotalRun": "max"})

df_filtered = df_grouped[df_grouped["Overs"].isin([0, 1])]

df_six_runs = df_filtered[df_filtered["TotalRun"] >= 6]

num_matches_with_early_six = df_six_runs["ID"].nunique()

st.write("Number of Matches with Early Six:", num_matches_with_early_six)

df_merged = df_six_runs.merge(df_match, left_on="ID", right_on="match_number")

df_merged["OpponentTeam"] = df_merged.apply(
    lambda row: row["team2"] if row["team1"] == batting_team else row["team1"], axis=1
)

opponent_counts = df_merged.groupby("OpponentTeam")["ID"].nunique().reset_index()
opponent_counts.columns = ["Opponent Team", "Number of Matches with Early Six"]

st.write("Early Sixes Breakdown by Opponent Team:")
st.dataframe(opponent_counts)

player_selected = st.selectbox("Choose Batting Team",df_Ball_Batter["Batter"].unique())

df_Ball_Batter = df_Ball_Batter[df_Ball_Batter["Batter"] == player_selected]

num_unique_ids = df_Ball_Batter["ID"].nunique()
st.write("Total Number of Matches :",num_unique_ids)

df_grouped = df_Ball_Batter.groupby(["ID", "Overs"], as_index=False).agg({"TotalRun": "max"})

df_filtered = df_grouped[df_grouped["Overs"].isin([0, 1])]

df_six_runs = df_filtered[df_filtered["TotalRun"] >= 6]

num_matches_with_early_six = df_six_runs["ID"].nunique()

st.write("Number of Matches with Early Six:", num_matches_with_early_six)

