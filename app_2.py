
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

        self.col_info = [
            'PitcherId',
            'PitcherThrows',
            'PitcherTeam',
            'Pitcher',
            'Inning',
            # 'Date',

            # 'チーム',
            # '選手',
            '背番号#',
            # 'pos1',
            # 'pos2',
        ]
        self.dic_table = {
            'num_pit': "NUM",
            'num_fb': "NUM(FB)",

            'rate_fb': "FB%",
            'strike%_fb': "STR%",
            'miss%_fb': "MiSS%",

            'spdP_ave': "SPD",
            'SpinRate_ave': "SPIN",
            'pitY_ave': "IVB",
            'pitX_ave': "HB",
            # 'SpinAxis_ave': "MiSS%",
            # 'relX_ave',
            # 'relY_ave',
            # 'relZ_ave',

            'spdP_max': "SPD\n(MAX)",
            'SpinRate_max': "SPIN\n(MAX)",
            'pitY_max': "IVB\n(MAX)",
            'pitX_max': "HB\n(MAX)",
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
        }
        self.col_table_EN = list(self.dic_table.keys())
        self.col_table_JP = list(self.dic_table.values())

        path_db = 'templates/TM_info_all_inning_ver5.csv'
        self.db = pd.read_csv(path_db, encoding="utf-8-sig", usecols=self.col_info+self.col_table_EN)
        self.db = self.db[self.db["Inning"] == "all"]
        self.db.index = self.db["背番号#"] + " " + [v.split(', ')[0] for v in self.db["Pitcher"]]   # list(range(self.db.shape[0]))
        self.db.rename(columns=self.dic_table, inplace=True)
        self.PitcherTeams = list(self.dic_team.keys())

        """
        for v in self.db.columns:
            print(f"'{v}', ")
        """

    def chose_pitcher_team(self):
        PitcherTeam_show = self.PitcherTeams[:6]
        self.PitcherTeam = st.multiselect("PitcherTeam", PitcherTeam_show, default=PitcherTeam_show)

        self.LR_list = st.multiselect("PitcherThrows", ["Left", "Right"], default=["Left", "Right"])

    def show_table(self):
        df_show = self.db[self.db['PitcherTeam'].isin(self.PitcherTeam)]
        df_show = df_show[df_show['PitcherThrows'].isin(self.LR_list)]

        comment = f"num-player = {df_show.shape[0]}"
        st.write(comment)

        st.dataframe(data=df_show[self.col_table_JP], width=8000, height=450)


if __name__ == '__main__':
    self = StreamlitTM()
    self.get_csv()
    self.chose_pitcher_team()
    self.show_table()

