
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

    def chose_extract_player(self):
        self.PitcherTeam = self._extract_values_to_chose_widget(w_No=0, col="PitcherTeam")
        self.Pitcher = self._extract_values_to_chose_widget(w_No=1, col="Pitcher")
        self.BatterTeam = self._extract_values_to_chose_widget(w_No=2, col="BatterTeam")
        self.Batter = self._extract_values_to_chose_widget(w_No=3, col="Batter")

        self.btn_table_show = st.button("Show")

    def _extract_values_to_chose_widget(self, w_No, col):
        col_values_set = sorted(set(self.db[col]))
        value_out = self.wid_cols[w_No].selectbox(col, col_values_set, index=0)
        return value_out

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
