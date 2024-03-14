import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from K_pages import *

# 상태 저장
if 'page' not in st.session_state:
    st.session_state['page'] = 'HOME'

menus = {"HOME": home, "지역별 인구 변화": kchange, "지역별 인구 비교": kbigyo, "지도": ksido}

with st.sidebar:
    for menu in menus.keys():
        if st.button(menu, use_container_width=True, type='primary' if st.session_state['page']==menu else 'secondary'):
            st.session_state['page']=menu
            st.rerun()

for menu in menus.keys():
    if st.session_state['page']==menu:
        menus[menu]()