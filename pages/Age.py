import pandas as pd
import plotly.express as px
import koreanize_matplotlib
import streamlit as st

st.set_page_config(
    page_title="연령별 교통사고 발생건수 분석",
    page_icon="🚕",
    layout="wide",
)
st.markdown("""### 🚗연령별 교통사고 분석👶""")

@st.cache
def load_rest_data():
    age_month = pd.read_csv("use_data_age/연령_월별.csv", encoding="cp949")
    age_day = pd.read_csv("use_data_age/연령_요일별.csv", encoding="cp949")
    age_time = pd.read_csv("use_data_age/연령_시간별.csv", encoding="cp949")
    age_acc = pd.read_csv("use_data_age/연령_사고유형별.csv", encoding="cp949")
    age_law = pd.read_csv("use_data_age/연령_법규위반별.csv", encoding="cp949")
    age_license = pd.read_csv("use_data_age/연령_날씨별.csv", encoding="cp949")
    
    return age_month, age_day, age_time, age_acc, age_law, age_license

age_month, age_day, age_time, age_acc, age_law, age_license = load_rest_data()

"""
🔸 20세 이하와 61-64세 이하 운전자는 연령 폭이 좁아 교통사고 발생 건수가 적게 나타났다.
\n🔸 분석에 해당 연령이 필요해서 따로 처리하지 않았다.  
#
"""

"""
\n 
#### 연령별 교통사고 발생건수
**- 가설** : \n교통사고 발생량이 많은 특정 연령이 있을 것이다."""

age_hist0 = px.histogram(age_month, x="연령", y="발생건수", histfunc="sum", title="연령별 교통사고 발생 건수", width=800, height=400)
age_hist0

"""
**분석 결과** : 51-60세 운전자의 교통사고 건수가 높게 기록되었다. 
\n 그렇지만 이 차트를 보고 고령 운전자의 교통사고 비율이 높다고 판단할 수는 없다.
\n 분석에 사용한 데이터는 가해자의 연령을 기준으로 교통사고 발생 건수를 조사한 것으로, 
\n 각 연령대의 교통사고 가해자 비율이 아니다.
#
\n 51-60세 운전자가 다른 연령대에 비해 사고를 많이 발생키시는 것인지
\n 해당 운전자가 많은 것인지 명확하지 않아 가설을 검증할 수 없다.  
#
#
"""


st.markdown("""#### 운전자 연령별 월별 교통사고 발생건수""")
st.markdown("""**가설** : 여름 휴가를 가는 8월과 눈으로 인해 많이 나는 겨울에 사고 건수가 높을 것이다. """)

age_line0 = px.line(age_month, y="발생건수", x="월", 
              color="연령", width=800, height=500, markers=True)
age_line0

"""
**분석 결과** : 모든 연령대에 있어 교통사고 발생 건수는 4월, 8월, 10-11월이 높게 나타났다.
\n 운전자의 연령과 사고 발생 월은 서로 그다지 영향을 주지 않는다.  
#
"""


"""
#### 20세 이하 운전자의 월별 교통사고 발생 건수  
**가설** : 20세 이하 운전자의 경우 연말과 연초, 11 ~ 2월 동안 사고 건수가 많을 것이다.
\n 수능이 끝난 뒤 면허를 취득한 20세 이하 운전자들의 사고가 집중될 것이라 예상했다.
"""

# 20세 이하 운전자만 추출
under_age = age_month.loc[age_month["연령"] == "20세이하"]
age_bar0 = px.bar(under_age, x="월", y="발생건수", title='20세 이하 운전자의 월별 교통사고 발생 건수', width=900, height=400)
age_bar0

"""
\n **분석 결과** : 연말과 연초를 기점으로 점차 사고 건수가 늘어나고 특히 2월과 3월 사이에 큰 폭으로 상승
\n 설정했던 가설과 달리 오히려 연말과 연초에 사고 건수가 가장 적었다.
\n 면허를 취득하는 시기와 실제로 도로에 나오는 시기 사이의 갭을 고려하지 않아서 생긴 차이같다.
\n **인사이트** : 20세 이하 운전자의 사고 건수는 4월과 7월이 가장 많다.
\n 이는 국내 여행 성수기와 일치한다.  
#
"""


"""
#### 운전자 연령별 시간별 교통사고 발생 건수  
\n **가설** : 직장인이 많은 30-40대 운전자들은 출퇴근 시간에 교통사고가 일어났을 것이다.  
"""

# 합계 제외하고 가져오기
age_time_line = age_time.loc[age_time["연령"] != "합계"]

age_area1 = px.area(age_time_line, x="시간", y="발생건수", color='연령', title='운전자 연령별 시간대별 교통사고 발생 건수', 
            width=900, height=700, facet_col="연령", facet_col_wrap=2)
age_area1

"""
**분석 결과** : 가설대로 30-40대 운전자들은 출퇴근 시간에 높은 사고 건수를 기록했다. 
\n 또한 흡사한 그래프 형태를 통해 두 연령대의 운전자들의 생활 시간이 유사함을 알 수 있다.   
#
"""


"""
#### 20-40대 운전자의 시간별 교통사고 발생 건수  
\n **가설** : 20대와 30대 운전자의 요일별 교통사고 발생 건수에 차이가 있었던 것처럼 시간별 발생 건수에도 차이가 있을 것이다.
"""

age_2040_col = (age_time_line["연령"] == "21~30세") | (age_time_line["연령"] == "31~40세") | (age_time_line["연령"] == "41~50세")
age_2040_time = age_time_line[age_2040_col]

age_line5 = px.line(age_2040_time, x="시간", y="발생건수",color="연령", title='20~40대 운전자의 시간대별 교통사고 발생 건수 비교', width=900, height=400, markers=True)
age_line5

"""
**분석 결과** : 20-40대 운전자들의 시간대별 교통사고 발생 건수는 거의 흡사한 양상을 보인다.
\n 오전에는 출근 시간인 8-10시에, 오후에는 퇴근 시간인 18-20시에 피크를 찍는다.
\n 직장에 다니는 주요 경제활동인구라는 공통점을 가지고 있기 때문이다.  
#
"""


"""
#### 51-60세 운전자와 65세 이상 운전자의 시간별 교통사고 발생 건수 
\n**가설** : 50대 운전자의 수가 많으니 사고량도 더 많겠지만, 사고 발생 시간에는 차이가 없을 것이다.
"""
# 해당 연령대만 잘라오기
age_5060_col = (age_time_line["연령"] == "51~60세") | (age_time_line["연령"] == "61~64세") | (age_time_line["연령"] == "65세이상")
age_5060 = age_time_line[age_5060_col]

age_line6 = px.line(age_5060, x="시간", y="발생건수",color="연령", title='50~60대 운전자의 시간대별 교통사고 발생 건수 비교', width=900, height=400, markers=True)
age_line6

"""
**분석 결과** : 61~64세 운전자보다 65세 이상 운전자의 교통사고 발생 건수가 많다는 점이 눈에 띄는데
\n 연령 범위가 더 넓어서 나타나는 현상일 수 있으므로 유의미한 지표는 아니다.
\n 51-60세, 61-64세 운전자는 20-40대 운전자와 마찬가지로 출퇴근 시간에 높은 사고 건수를 기록했다.
\n 그러나 65세 이상 운전자는 10-12시, 14-16시에 피크를 찍어, 출퇴근 시간이 있는 직장인은 아니라고 추측할 수 있다.

\n 실제로 한국의 정년퇴직 나이를 분석한 기사에 따르면
\n 한국인이 '주된 일자리(가장 오랜 기간 일한 일자리)'에서 퇴직하는 연령은 평균 49.3세이다. 
\n 이들 대부분은 퇴직 후에도 경제활동 지속을 위해 재취업을 원하는데 반해, 
\n 65세 이상은 9-6 정규직 형태의 취업은 잘 이뤄지지 않음을 확인할 수 있다.  
#
\n 기사 출처 : https://www.donga.com/news/Economy/article/all/20220309/112238197/1  
\n 기사 출처 : http://www.seniorsinmun.com/news/articleView.html?idxno=44364  
#
"""

""" 
#### 결론
\n 운전자 연령이 교통사고에 미치는 영향은 예상했던 것보다 크지 않았다.
\n 대부분의 분석에서 연령이 아닌 외부 변수에 의해 차이가 발생했다. 
\n 오히려 그 점에서 볼 때, 파악하기 어려운 지표인 연령별 실질 운전자수를
\n 연령별 교통사고 발생 건수로 대체해서 활용할 수 있겠다는 인사이트를 얻었다.  
#
"""
