
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
        self.db = pd.read_csv(path_db, encoding="utf_8_sig")

        # values
        self.PitcherTeams, self.BatterTeams = [sorted(set(self.db[v])) for v in ["PitcherTeam", "BatterTeam"]]

    def _chose_pitcher(self, BP):
        Team = self.wid_cols[0].selectbox(f"{BP}Team", self.PitcherTeams, index=0)

        Players = self.db.query(f'{BP}Team == @Team')
        Player = self.wid_cols[1].selectbox(BP, Players, index=0)
        PlayerId = self.db.query(f'{BP} == @Player')[f"{BP}Id"].values[0]

        return Team, Player, PlayerId

    def chose_extract_player(self):
        self.BatterTeam, self.Batter, self.BatterId = self._chose_pitcher(BP="Batter")
        self.PitcherTeam, self.Pitcher, self.PitcherId = self._chose_pitcher(BP="Pitcher")
        self.btn_table_show = st.button("Show")

    def fnc_show_table(self):
        self.rule = "Pitcher == @self.Pitcher & Batter == @self.Batter"
        st.write(self.rule)

        if self.btn_table_show:
            st.write(self.db.query(self.rule))


if __name__ == '__main__':
    self = StreamlitTM()
    self.chose_extract_player()
    self.fnc_show_table()

# streamlit run app.py
