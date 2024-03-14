import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import folium
import matplotlib.pyplot as plt
import seaborn as sns
import time

sns.set_theme(style='whitegrid', font_scale=1.5)
sns.set_palette('Set2', n_colors=10)
# plt.rc('font', family='AppleGothic')
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

def txt_gen(txt):
    for t in list(txt):
        yield t
        time.sleep(0.1)

def home():
    APP_SUB_TITLE = '대한민국 지역별 인구 조사'
    # st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)
    st.subheader("인구 정보")
    st.info("지역별 인구 변화 (2022년)")
    st.divider()
    txt = "현재 데이터는 2022년도 지역별 인구 변화 정보를 나타냅니다."

    st.write_stream(txt_gen(txt))
    if st.button("next",use_container_width=True):
        st.session_state['page']='지역별 인구 변화'
        st.rerun()

def kchange():
    st.title("분석 현황")
    tmp = data.copy()

    st.dataframe(tmp)
    st.info("지역별 출생, 사망, 그에 따른 인구 감소, 결혼, 이혼 정보를 나타냅니다.")

    st.subheader('각 카테고리 별 인구 변화')
    st.info('그래프는 순서대로 서울, 부산, 대구, 인천, 광주, 대전, 울산, 세종, 경기, 강원, 충북, 충남, 전북, 전남, 경북, 경남, 제주를 나타냅니다.')
    tmp = tmp.groupby('Area').mean()
    col = st.selectbox('지역 선택',tmp.columns[:])
    whole_values = tmp[tmp.index!=2020].groupby('Area')[[col]].mean()
    st.download_button('Download',whole_values.to_csv(encoding='euc-kr'), 'test.csv')
    colors = [tab10.colors[i % 10] for i in range(len(whole_values))]

    fig, ax = plt.subplots()
    plt.xticks(rotation=45, fontsize=8)  # x축 눈금 레이블의 글꼴 크기를 8로 설정합니다.
    ax.set_title(col, fontsize=12)  # 그래프 제목의 글꼴 크기를 12로 설정합니다.
    ax.bar(whole_values.index.astype(str), whole_values[col], color=colors)
    overall_average = whole_values[col].mean()
    ax.axhline(y=overall_average, color='gray', linestyle='--', linewidth=2)
    st.pyplot(fig)

    if st.button("next",use_container_width=True):
        st.session_state['page']='지역별 인구 비교'
        st.rerun()

def kbigyo():
    pass

def ksido():
    pass