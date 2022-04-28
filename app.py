
import pandas as pd
import matplotlib.pyplot
import streamlit as st


def git_setting():
    print("PUSHED")
    """
    git init
    git add .
    git commit -m "first commit"
    git branch -M main
    git remote add origin https://github.com/Isdakgoe/st-tm.git
    git push -u origin main
    
    """



class StreamlitTM:
    def __init__(self):
        # setting streamlit
        st.set_page_config(layout="wide")
        st.title("TrackMan DashBoard")
        self.wid_cols = st.beta_columns(4)

        # read data
        path_db = 'templates/tm_csv_all_2022_NPB+NPM_update.pickle'
        self.db = pd.read_pickle(path_db)
        for v in self.db.columns:
            print(f"'{v}', ")

        # values
        self.dic_team = {
            "ORI_BUF": "オリックス",
            "CHI_MAR": "ロッテ",
            "TOH_GOL": "楽天",
            "SOF_HAW": "ソフトバンク",
            "SAI_LIO": "西武",
            "HOK_FIG": "日本ハム",

            "YOM_GIA": "巨人",
            "HAN_TIG": "阪神",
            "BAY_STA": "横浜",
            "CHU_DRA": "中日",
            "HIR_CAR": "広島",
            "YAK_SWA": "ヤクルト",

            # "MIN_BUF": "オリックス",
            # "MIN_MAR": "ロッテ",
            # "MIN_EAG": "楽天",
            # "MIN_HAW": "ソフトバンク",
            # "MIN_LIO": "西武",
            # "MIN_FIG": "日本ハム",

            # "MIN_GIA": "巨人",
            # "MIN_TIG": "阪神",
            # "MIN_BAY": "横浜",
            # "MIN_DRA": "中日",
            # "MIN_CAR": "広島",
            # "MIN_SWA": "ヤクルト",
        }
        self.col_table = [
            "Date",
            "Inning",
            "Outs",
            "Balls",
            "Strikes",
            'TaggedPitchType',
            'PitchCall',
            'PlayResult',

            # 'spdP',
            # 'SpinRate',
            # 'Tilt',
            # 'pitX',
            # 'pitY',
            # 'catX',
            # 'catY',
            # 'relX',
            # 'relY',
            # 'relZ',
            #
            # 'spdB',
            # 'dig',
            # 'dis',
            # 'brzY',
        ]

    def _chose_pitcher(self, w_n, BP):
        Team = self.wid_cols[w_n].selectbox(f"{BP}Team", list(self.dic_team.keys()), index=0)
        Players = sorted(set(self.db.query(f'{BP}Team == @Team')[BP]))
        Player = self.wid_cols[w_n+1].selectbox(BP, Players, index=0)
        return Team, Player

    @st.cache
    def chose_extract_player(self):
        self.PitcherTeam, self.Pitcher = self._chose_pitcher(w_n=0, BP="Pitcher")
        self.BatterTeam, self.Batter = self._chose_pitcher(w_n=2, BP="Batter")
        self.btn_table_show = st.button("Show")

    def fnc_show_table(self):
        self.rule = f"Pitcher == @self.Pitcher & Batter == @self.Batter"
        db_show = self.db.query(self.rule)
        num = db_show.shape[0]
        st.write(num)

        if self.btn_table_show & (num != 0):
            st.write(db_show[self.col_table])


if __name__ == '__main__':
    self = StreamlitTM()
    self.chose_extract_player()
    self.fnc_show_table()

# streamlit run app.py
