
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

@st.cache(suppress_st_warning=True)
class StreamlitTM:
    def __init__(self):
        # setting streamlit
        st.title("TrackMan DashBoard")
        self.wid_cols = st.beta_columns(4)

        # read data
        self.ll = pd.read_csv('templates/long_list_tm.csv', encoding="utf_8_sig")
        self.ll.index = self.ll["NPB選手ID"]
        self.ll["nameTM"] = np.nan

        path_db = 'templates/tm_2022_db.csv'
        self.db = pd.read_csv(path_db, encoding="utf-8-sig")
        for bp in ["Pitcher", "Batter"]:
            # TrackMan
            db_id = list(set(self.db[f"{bp}Id"]))
            ind_use = list(set([v for v in db_id if "Unnamed" not in str(v)]))
            self.db.query(f'{bp}Id in @ind_use', inplace=True)
            self.db[f"{bp}Id"] = self.db[f"{bp}Id"].astype(int)

            # LongList
            id_NPB_list = list(set(self.db[f"{bp}Id"]))
            id_NPB_list = [v for v in id_NPB_list if v in self.ll["NPB選手ID"]]
            for id_NPB in id_NPB_list:
                self.ll.loc[id_NPB, "nameTM"] = self.db.query(f'{bp}Id == @id_NPB')[f"{bp}Id"].values[0]
        self.ll.dropna(subset=["nameTM"], inplace=True)

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
        self.teamEN_list = list(self.dic_team.keys())

        self.dic_bp_EN = {bp: {teamEN: list(set(self.db.query(f'{bp}Team == @teamEN')[bp]))
                               for teamEN in self.teamEN_list} for bp in ["Batter", "Pitcher"]}

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

    def _chose_pitcher(self, w_n, bp):
        teamEN = self.wid_cols[w_n].selectbox(f"{bp}Team", self.teamEN_list, index=0)
        Player = self.wid_cols[w_n+1].selectbox(bp, self.dic_bp_EN[bp][teamEN], index=0)
        return teamEN, Player

    @st.cache(suppress_st_warning=True)
    def chose_extract_pitcher(self):
        self.PitcherTeam, self.Pitcher = self._chose_pitcher(w_n=0, bp="Pitcher")

    @st.cache(suppress_st_warning=True)
    def chose_extract_batter(self):
        self.BatterTeam, self.Batter = self._chose_pitcher(w_n=2, bp="Batter")

    def fnc_show_table(self):
        self.rule = f"Pitcher == @self.Pitcher & Batter == @self.Batter"
        self.btn_table_show = st.button("Show")
        if self.btn_table_show:
            db_show = self.db.query(self.rule)
            num = db_show.shape[0]
            if num != 0:
                st.write(db_show[self.col_table])


if __name__ == '__main__':
    st.set_page_config(layout="wide")
    self = StreamlitTM()
    self.chose_extract_pitcher()
    self.chose_extract_batter()
    self.fnc_show_table()

# streamlit run app.py
