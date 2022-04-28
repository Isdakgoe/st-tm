
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


class StreamlitTM:
    def __init__(self):
        # setting streamlit
        st.set_page_config(layout="wide")
        st.title("Visualizing Central Limit Theorem")
        self.wid_cols = st.beta_columns(3)

        # read data
        path_db_summary = 'templates/DB_PitchType_NPB_2022.csv'
        self.db_summary = pd.read_csv(path_db_summary, encoding="utf-8-sig")

    def chose_extract_player(self):
        PitcherTeam_list = sorted(set(self.db_summary["PlayerTeam"]))
        PlayerTeam = self.wid_cols[0].selectbox("PlayerTeam", PitcherTeam_list, index=0)

        Pitcher_list = sorted(set(self.db_summary.query('PlayerTeam == @PlayerTeam')["Player"]))
        self.Player = self.wid_cols[1].selectbox("Player", Pitcher_list, index=0)

        self.btn_table_show = self.wid_cols[2].button("Show")

    def fnc_show_table(self):
        if self.btn_table_show:
            db_summary_show = self.db_summary.query('Player == @self.Player')
            st.write(db_summary_show)


self = StreamlitTM()
self.chose_extract_player()
self.fnc_show_table()

# if __name__ == '__main__':
