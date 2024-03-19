import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import folium
import matplotlib.pyplot as plt
import seaborn as sns
import time
import numpy as np


sns.set_theme(style='whitegrid', font_scale=1.5)
sns.set_palette('Set2', n_colors=10)
plt.rc('font', family='Malgun Gothic')

plt.rc('axes', unicode_minus=False)
from matplotlib.cm import get_cmap

# Get the 'tab10' colormap
tab10 = get_cmap('tab10')

SIDOS={'SEOUL':'서울특별시', 'BUSAN':'부산광역시','DAEGU':'대구광역시','INCHEON':'인천광역시','GWANGJU':'광주광역시','DAEJEON':'대전광역시','ULSAN':'울산광역시','SEJONG':'세종특별자치시', 'GYEONGGI':'경기도', 'GANGWON':'강원도', 'CHUNGBUK':'충청북도','CHUNGNAM':'충청남도','JEONBUK':'전라북도', 'JEONNAM':'전라남도', 'GYEONGBUK':'경상북도', 'GYEONGNAM':'경상남도', 'JEJU':'제주특별자치도'}

@st.cache_data
def get_datas():
    data = pd.read_csv("k_population.csv", index_col=0)
    return data

data = get_datas()

@st.cache_data
def k_datas():
    data = pd.read_csv("k_bddm.csv", index_col=0)
    return data

k_data = k_datas()

def txt_gen(txt):
    for t in list(txt):
        yield t
        time.sleep(0.1)

def home():
    st.subheader("지역별 인구 변화 (2022년)")
    st.info("해당 정보는 2022년도 자료 기반 출생, 죽음, 결혼, 이혼의 내용을 포함하고 있습니다.")
    st.image("down.jpg", caption="2022년도 자료 기반 인구 변화 그래프", width=700)


def kchange():
    st.title("분석 현황")
    tmp = data.copy()

    st.dataframe(tmp)
    st.info("지역별 출생, 사망, 그에 따른 자연 증가, 결혼, 이혼 정보를 나타냅니다.") 

    st.subheader('각 카테고리 별 인구 변화')
    tmp = tmp.groupby('Area').mean()
    col = st.selectbox('카테고리 선택',tmp.columns[:])
    whole_values = tmp[tmp.index!=2020].groupby('Area')[[col]].mean()
    colors = [tab10.colors[i % 10] for i in range(len(whole_values))]

    fig, ax = plt.subplots()
    plt.xticks(rotation=45, fontsize=8)
    ax.set_title(col, fontsize=12)
    ax.bar(whole_values.index.astype(str), whole_values[col], color=colors)
    overall_average = whole_values[col].mean()
    ax.axhline(y=overall_average, color='gray', linestyle='--', linewidth=2)
    st.pyplot(fig)


def kbigyo(): 
    tmp = data.copy()
    st.title("지역별 인구 비교")
    st.info('지역별 출생, 사망, 그에 따른 인구 감소, 결혼, 이혼 정보 비교')

    selected_area = st.sidebar.selectbox('지역 선택', data['Area'])
    selected_data = data[data['Area'] == selected_area]


    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.subheader(f'{selected_area}의 출생, 사망자, 자연 증가, 결혼, 이혼')
    plt.figure(figsize=(6, 6))
    sns.barplot(data=selected_data[['출생', '사망자', '자연 증가', '결혼', '이혼']], palette='viridis')
    st.pyplot()


def kyear():
    st.title("연도별 추이상황")
    k_tmp = k_data.copy()

    st.dataframe(k_tmp)
    st.info("연도별 출생, 죽음, 결혼 이혼 정보를 나타냅니다.") 
    k_data.set_index('title', inplace=True)
    st.line_chart(k_data, use_container_width=True, width=800, height=700)


def ksido():
    tmp = data.groupby('Area').mean()
    tmp.index = [SIDOS[idx] for idx in tmp.index]
    tmp.reset_index(inplace=True)
    tiles = ['CartoDB dark_matter', 'OpenStreetMap']
    with st.sidebar:
        st.divider()
        t = st.sidebar.radio('Map', tiles)
        col = st.selectbox('컬럼 선택',tmp.columns[1:])

    map = folium.Map(location=[36.194012, 127.5019596], zoom_start=7, scrollWheelZoom=True, tiles=t)
    choropleth = folium.Choropleth(
        geo_data='SIDO_MAP_2022_cp949.json',
        data=tmp,
        columns=('index', col),
        key_on='feature.properties.CTP_KOR_NM',
        line_opacity=0.8,
        highlight=True
    )
    choropleth.geojson.add_to(map)
    st_map = st_folium(map, width=700, height=600)