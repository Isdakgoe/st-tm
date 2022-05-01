
from datetime import datetime
import pandas as pd
import matplotlib.pyplot
import streamlit as st
import numpy as np


def git_setting():
    print("PUSHED")

    # @st.cache(suppress_st_warning=True)

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
        st.title("TrackMan DataBase")
        self.wid_cols = st.beta_columns(4)

        # read data
        self.ll = pd.read_csv('templates/long_list_tm.csv', encoding="utf_8_sig")
        self.ll.index = self.ll["NPB選手ID"]
        self.ll["nameTM"] = np.nan

        path_db = 'templates/TM_info_all_inning_ver4.csv'

        self.col_info = [
            'PitcherId',
            'PitcherTeam',
            'Pitcher',
            'Inning',
            'Date',

            'チーム',
            '選手',
            '背番号#',
            'pos1',
            'pos2',
        ]
        self.col_table = [
            'num_pit',
            'num_fb',

            'spdP_ave',
            'SpinRate_ave',
            'pitY_ave',
            'pitX_ave',
            'SpinAxis_ave',
            'relX_ave',
            'relY_ave',
            'relZ_ave',

            'spdP_max',
            'SpinRate_max',
            'pitY_max',
            'pitX_max',
            'SpinAxis_max',
            'relX_max',
            'relY_max',
            'relZ_max',

            'spdP_std',
            'SpinRate_std',
            'pitY_std',
            'pitX_std',
            'SpinAxis_std',
            'relX_std',
            'relY_std',
            'relZ_std',

            'rate_fb',
            'strike%_fb',
            'miss%_fb',
        ]
        self.db = pd.read_csv(path_db, encoding="utf-8-sig", usecols=self.col_info+self.col_table)
        self.db = self.db[self.db["Inning"] == "all"]
        self.db.index = list(range(self.db.shape[0]))
        # for v in self.db.columns:
        #     print(f"'{v}', ")
        st.dataframe(self.db_show[self.col_table])

        # values
        self.dic_team = {
            "TOH_GOL": "楽天",
            "ORI_BUF": "オリックス",
            "CHI_MAR": "ロッテ",
            "SOF_HAW": "ソフトバンク",
            "SAI_LIO": "西武",
            "HOK_FIG": "日本ハム",

            "YOM_GIA": "巨人",
            "HAN_TIG": "阪神",
            "BAY_STA": "横浜",
            "CHU_DRA": "中日",
            "HIR_CAR": "広島",
            "YAK_SWA": "ヤクルト",
        }
        self.teamEN_list = list(self.dic_team.keys())
        self.Pitchers = sorted(set(self.db["Pitcher"]))

    def _chose_player(self, w_n, bp):
        teamEN = self.wid_cols[w_n].selectbox(f"{bp}Team", ['all']+self.teamEN_list, index=0)
        if teamEN == "all":
            Player = "all"
            self.Batter = "all"
        else:
            Player = self.wid_cols[w_n+1].selectbox(bp, ["all"]+self.dic_bp_EN[bp][teamEN], index=0)
        return teamEN, Player

    def chose_extract_pitcher(self):
        self.Pitcher = self.wid_cols[0].selectbox("Pitcher", ["all"] + self.Pitchers, index=1)
        # self.PitcherTeam, self.Pitcher = self._chose_player(w_n=0, bp="Pitcher")

    def search_rule(self):
        if self.Pitcher == self.Batter == "all":
            st.error('Pitcher and Batter are "all", and please change either one')
            return False

        else:
            if self.Pitcher == "all":
                self.db_show = self.db[self.db["Batter"] == self.Batter]

            elif self.Batter == "all":
                self.db_show = self.db[self.db["Pitcher"] == self.Pitcher]

            else:
                self.db_show = self.db[(self.db["Pitcher"] == self.Pitcher) & (self.db["Batter"] == self.Batter)]

            num = str(self.db_show.shape[0])
            st.write(f"num of pitch = {num}")
            return True

    def fnc_show_table(self):
        st.dataframe(self.db_show[self.col_table])


if __name__ == '__main__':
    st.set_page_config(layout="wide")
    self = StreamlitTM()
    # self.chose_extract_pitcher()

    # self.chose_extract_pitcher()

    # self.btn_table_show = st.button("Show")
    # self.fnc_show_table()
