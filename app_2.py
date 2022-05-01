
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
        st.set_page_config(layout="wide")
        st.title("TrackMan DataBase")
        self.wid_cols = st.beta_columns(4)

        # parameters
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

    def get_csv(self):
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
            # 'relX_ave',
            # 'relY_ave',
            # 'relZ_ave',

            'spdP_max',
            'SpinRate_max',
            'pitY_max',
            'pitX_max',
            # 'SpinAxis_max',
            # 'relX_max',
            # 'relY_max',
            # 'relZ_max',

            # 'spdP_std',
            # 'SpinRate_std',
            # 'pitY_std',
            # 'pitX_std',
            # 'SpinAxis_std',
            # 'relX_std',
            # 'relY_std',
            # 'relZ_std',

            'rate_fb',
            'strike%_fb',
            'miss%_fb',
        ]
        self.db = pd.read_csv(path_db, encoding="utf-8-sig", usecols=self.col_info+self.col_table)
        self.db = self.db[self.db["Inning"] == "all"]
        self.db.index = self.db["Pitcher"]    # list(range(self.db.shape[0]))
        self.PitcherTeams = list(self.dic_team.keys())
        # for v in self.db.columns:
        #     print(f"'{v}', ")

        # values
        self.teamEN_list = list(self.dic_team.keys())
        self.Pitchers = sorted(set(self.db["Pitcher"]))

    def chose_pitcher_team(self):
        PitcherTeam_show = ["all"] + self.PitcherTeams[:6]
        self.PitcherTeam = self.wid_cols[0].multiselect("PitcherTeam", PitcherTeam_show, default=PitcherTeam_show)
        if self.PitcherTeam == "all":
            df_show = self.db
        else:
            df_show = self.db[self.db["PitcherTeam"] == self.PitcherTeam]

        st.dataframe(df_show[self.col_table].style.highlight_max(axis=0), 1000, 1000)


if __name__ == '__main__':
    self = StreamlitTM()
    self.get_csv()
    self.chose_pitcher_team()
