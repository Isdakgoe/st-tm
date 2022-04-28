
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
st.write(db_summary)

