import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from K_sub_main import *


if 'page' not in st.session_state:
    st.session_state['page'] = 'HOME'

menus = {"HOME": home, "지역별 인구 변화": kchange, "지역별 인구 비교": kbigyo, "연도별 변화": kyear, "지도": ksido}


with st.sidebar:
    sidebar_style = """
        <style>
            .sidebar .sidebar-content {
                background-color: #3498db;
                color: white;
            }
        </style>
    """
    st.markdown(sidebar_style, unsafe_allow_html=True)
    for menu in menus.keys():
        if st.button(menu, use_container_width=True, type='primary' if st.session_state['page']==menu else 'secondary'):
            st.session_state['page']=menu
            st.rerun()

for menu in menus.keys():
    if st.session_state['page']==menu:
        menus[menu]()