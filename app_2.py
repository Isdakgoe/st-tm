
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
        self.dic_pt = {'Fastball': ["ストレート", '#fbf401', ["o", "o"]],

                       'Sinker': ["シンカー", '#00ff00', [">", "<"]],
                       'Cutter': ["カット", '#cc6601', ["3", "4"]],
                       'Slider': ["スライダー", '#ff99cc', ["<", ">"]],

                       'Curveball': ["カーブ", '#ff0200', ["^", "^"]],
                       'Splitter': ["フォーク", '#0700ff', [",", ","]],
                       'ChangeUp': ["チェンジアップ", '#c0c0c0', ["D", "D"]],
                       'Knuckleball': ["ナックル", '#eeeeee', ["*", "*"]],
                       'Other': ["その他", '#eeeeee', ["h", "h"]],

                       'all': ["全球種", '#000000', [".", "."]],
                       }  # 'Undefined', '#eeeeee', "h"],
        self.pt_list = list(self.dic_pt.keys())[:-2]

    def get_csv(self):
        # read data
        self.ll = pd.read_csv('templates/long_list_tm.csv', encoding="utf_8_sig")
        self.ll.index = self.ll["NPB選手ID"]

        self.col_info = [
            'PitcherId',
            'PitcherThrows',
            'PitcherTeam',
            'Pitcher',
            'pt',
            # 'Inning',
            # 'Date',

            # 'チーム',
            # '選手',
            '背番号#',
            # 'pos1',
            # 'pos2',
        ]
        self.dic_table = {
            'num_all': "NUM",
            'num': "NUM(FB)",

            'pt_rate': "pt%",
            'str%': "STR%",
            'miss%': "MiSS%",

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

        path_db = 'templates/TM_info_all_inning_ver6.csv'
        self.db = pd.read_csv(path_db, encoding="utf-8-sig", usecols=self.col_info+self.col_table_EN)
        self.db.index = self.db["背番号#"] + " " + [v.split(', ')[0] for v in self.db["Pitcher"]]   # list(range(self.db.shape[0]))
        self.db.fillna(1000000, inplace=True)
        self.db.loc[:, self.col_table_EN[2:5]] = (self.db.loc[:, self.col_table_EN[2:5]] * 100).astype(int)
        self.db.loc[:, self.col_table_EN[5:]] = (self.db.loc[:, self.col_table_EN[5:]]).astype(int)
        self.db.replace({1000000: np.nan}, inplace=True)

        self.db.rename(columns=self.dic_table, inplace=True)
        self.PitcherTeams = list(self.dic_team.keys())

        """
        for v in self.db.columns:
            print(f"'{v}', ")
        """

    def chose_pitcher_team(self):
        self.PitcherTeam = st.multiselect("PitcherTeam", self.PitcherTeams[:6], default=self.PitcherTeams[:6])

        self.LR_chosen = st.multiselect("PitcherThrows", ["Left", "Right"], default=["Left", "Right"])

        self.pt_chosen = st.multiselect("TaggedPitchType", self.pt_list, default=self.pt_list)

    def show_table(self):
        df_show = self.db[self.db['PitcherTeam'].isin(self.PitcherTeam)]
        df_show = df_show[df_show['PitcherThrows'].isin(self.LR_chosen)]
        df_show = df_show[df_show['pt'].isin(self.pt_chosen)]

        comment = f"{df_show.shape[0]} data is at table below"
        st.write(comment)

        st.dataframe(data=df_show[self.col_table_JP], width=8000, height=450)


if __name__ == '__main__':
    self = StreamlitTM()
    self.get_csv()
    self.chose_pitcher_team()
    self.show_table()

