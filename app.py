
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
        st.title("TrackMan DashBoard")
        self.wid_cols = st.beta_columns(4)

        # read data
        path_db = 'templates/tm_2022_db.csv'
        self.db = pd.read_csv(path_db, encoding="utf-8-sig")

        # values
        self.dic_team = {BP: sorted(set(self.db[f"{BP}Team"])) for BP in ["Pitcher", "Batter"]}

    def _chose_pitcher(self, BP):
        Team = self.wid_cols[0].selectbox(f"{BP}Team", self.dic_team[BP], index=0)
        st.write(Team)

        Players = sorted(set(self.db.query(f'{BP}Team == @Team')[BP]))
        Player = self.wid_cols[1].selectbox(BP, Players, index=0)

        return Team, Player

    def chose_extract_player(self):
        self.PitcherTeam, self.Pitcher = self._chose_pitcher(BP="Pitcher")
        self.BatterTeam, self.Batter = self._chose_pitcher(BP="Batter")
        self.btn_table_show = st.button("Show")

    def fnc_show_table(self):
        self.rule = f"Pitcher == @self.Pitcher & Batter == @self.Batter"
        db_show = self.db.query(self.rule)
        num = db_show.shape[0]

        st.write(self.rule)
        st.write(num)

        if self.btn_table_show & (num == 0):
            st.write(num)


if __name__ == '__main__':
    self = StreamlitTM()
    self.chose_extract_player()
    self.fnc_show_table()

# streamlit run app.py
