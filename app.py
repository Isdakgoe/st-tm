
import pandas as pd
import matplotlib.pyplot
import streamlit as st


def git_setting():
    print("PUSHED")
    # git init
    # heroku git:remote -a st-tm
    # git add .
    # git commit -am "コメント"
    # git push heroku master
    # git remote add heroku https://git.heroku.com/st-tm.git


st.title("Visualizing Central Limit Theorem")

path_db_summary = 'templates/DB_PitchType_NPB_2022.csv'
db_summary = pd.read_csv(path_db_summary, encoding="utf-8-sig")

PitcherTeam_list = sorted(set(db_summary["PlayerTeam"]))
PlayerTeam = st.selectbox("PlayerTeam", PitcherTeam_list, index=0)

Pitcher_list = set(db_summary.query('PlayerTeam == @PlayerTeam')["Pitcher"])
Player = st.selectbox("Player", Pitcher_list, index=0)

btn_table_show = st.button("Show")
if btn_table_show:
    db_summary_show = db_summary.query('Player == @Player')
    st.write(db_summary_show)

