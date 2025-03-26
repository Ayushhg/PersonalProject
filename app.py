import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config(layout="wide")
st.title("Early Six Analyis by Ayush Goel")


df_ballByball = pd.read_csv("IPL/Ball_By_Ball_Match_Data.csv")
df_match = pd.read_csv("IPL/Match_info.csv")


batting_team = st.sidebar.selectbox("Choose Batting Team",df_ballByball["BattingTeam"].unique())

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

