
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
        self.PitcherTeams = list(self.dic_team.keys())

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

        # long_list
        self.ll = pd.read_csv('templates/long_list_tm.csv', encoding="utf_8_sig")
        self.ll.index = self.ll["NPB選手ID"]

        # start
        page_list = ["Pitcher-Summary", "Batter-Summary"]
        self.page = st.sidebar.radio("Page for display", page_list, index=0)
        if self.page == page_list[0]:
            self.page_PS()
        else:
            self.page_BS()

    # BS: Batter Summary
    def page_BS(self):
        st.error("NON PAGE")

    # PS: Pitcher Summary
    def page_PS(self):
        # comment
        with st.beta_expander("See explanation"):
            st.write("STR: StrikeCalled + StrikeSwinging + FoulBall + InPlay")
            st.write("STR%: STR / NUM(pt)")
            st.write("MISS%: StrikeSwinging / STR")
            st.write("IVB: Induced Vertical Break (縦変化量) [cm]")
            st.write("HB: Horizontal Break (横変化量) [cm]")
            st.write("RelH: Release Side [cm]")
            st.write("RelS: Release Height [cm]")
            st.write("Ext: Extension [cm]")
        st.write("\n")

        # set widgets
        self.wid_cols = st.beta_columns(3)

        # start
        self.get_csv_PS()
        self.extract_values_PS()
        self.show_table_PS()

    def get_csv_PS(self):
        # set parameters
        self.col_info = [
            'PitcherId',
            'PitcherThrows',
            'PitcherTeam',
            'Pitcher',
            'pt',
            # 'Inning',
            # 'Date',

            'チーム',
            # '選手',
            '背番号#',
            # 'pos1',
            # 'pos2',
        ]
        self.dic_table = {
            'PitcherThrows': "LR",
            'PitcherTeam': "Team",
            '背番号#': "#",
            'Pitcher': "Pitcher",
            'pt': 'pt',

            'num_all': "NUM",
            'num': "NUM(pt)",

            'pt_rate': "pt%",
            'str%': "STR%",
            'miss%': "MiSS%",

            'spdP_ave': "SPD",
            'SpinRate_ave': "SPIN",
            'pitY_ave': "IVB",
            'pitX_ave': "HB",

            'relX_ave': 'RelS',
            'relY_ave': 'RelH',
            'relZ_ave': 'Ext',

            # 'SpinAxis_ave': "MiSS%",

            # 'spdP_max': "SPD\n(MAX)",
            # 'SpinRate_max': "SPIN\n(MAX)",
            # 'pitY_max': "IVB\n(MAX)",
            # 'pitX_max': "HB\n(MAX)",
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

        # read data
        path_db = 'templates/TM_info_all_inning_ver6.csv'
        self.db = pd.read_csv(path_db, encoding="utf-8-sig", usecols=self.col_info+self.col_table_EN)
        # self.db["Pitcher"] = [v.split(', ')[0] for v in self.db["Pitcher"]]
        # self.db.index = [f"[" + v.split('_')[0] + "] " for v in self.db["PitcherTeam"]] \
        #                 + self.db["背番号#"] + " " + self.db["Pitcher"]

        v_replace = 100000
        self.db.fillna(v_replace, inplace=True)
        self.db.loc[:, self.col_table_EN[7:10]] = (self.db.loc[:, self.col_table_EN[7:10]] * 100).astype(int)
        self.db.loc[:, self.col_table_EN[10:14]] = (self.db.loc[:, self.col_table_EN[10:14]]).astype(int)
        self.db.loc[:, self.col_table_EN[14:]] = (self.db.loc[:, self.col_table_EN[14:]] * 100).astype(int)
        self.db.replace({v_replace: np.nan, v_replace*100: np.nan}, inplace=True)
        self.db.rename(columns=self.dic_table, inplace=True)

        """
        for v in self.db.columns:
            print(f"'{v}', ")
        """

    def extract_values_PS(self):
        self.PitcherTeamEN = self.wid_cols[0].multiselect("■ PitcherTeam", self.PitcherTeams[:6], default=["TOH_GOL"])
        self.PitcherTeamJP = [self.dic_team[v] for v in self.PitcherTeamEN]

        self.LR_chosen = self.wid_cols[1].multiselect("■ PitcherThrows", ["Left", "Right"], default=["Left", "Right"])
        self.pt_chosen = self.wid_cols[2].multiselect("■ TaggedPitchType", self.pt_list, default=self.pt_list[0])
        self.col_show = st.multiselect("■ Columns which shows at table below", self.col_table_JP, default=self.col_table_JP)

    def show_table_PS(self):
        df_show = self.db[self.db['チーム'].isin(self.PitcherTeamJP)]
        df_show = df_show[df_show['LR'].isin(self.LR_chosen)]
        df_show = df_show[df_show['pt'].isin(self.pt_chosen)]

        comment = f"{df_show.shape[0]} data is at table below"
        st.write(comment)

        st.dataframe(data=df_show[self.col_show], width=12000, height=450)


if __name__ == '__main__':
    self = StreamlitTM()


