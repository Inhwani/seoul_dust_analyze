import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def app():
    st.title('탐색적 데이터 분석 (EDA)')
    
    # 데이터 로드
    file_path = '2023daypol.csv'  # 상대 경로 사용
    data = pd.read_csv(file_path, encoding='cp949')  # 인코딩 지정
    
    # 측정일시를 datetime 형식으로 변환
    if '측정일시' in data.columns:
        data['측정일시'] = pd.to_datetime(data['측정일시'], format='%Y%m%d')
        data['년'] = data['측정일시'].dt.year
        data['월'] = data['측정일시'].dt.month
        data['일'] = data['측정일시'].dt.day
    
    # 월과 일을 선택할 수 있는 옵션 제공
    st.write("### 월과 일을 선택하여 데이터 필터링")
    st.write('#### 탐색적 데이터 분석:  수치 요약과 시각화를 사용하여 데이터를 탐색하고 변수 간 잠재적 관계를 찾아내는 프로세스')
    months = sorted(data['월'].unique())
    days = sorted(data['일'].unique())
    
    selected_month = st.selectbox("월 선택", months)
    selected_day = st.selectbox("일 선택", days)
    
    # 측정소명 선택 (복수 선택 가능)
    st.write("### 측정소명을 선택하여 데이터 필터링")
    stations = data['측정소명'].unique()
    selected_stations = st.multiselect("측정소명 선택", stations, default=stations)
    
    # 선택한 월, 일 및 측정소명에 해당하는 데이터 필터링
    filtered_data = data[(data['월'] == selected_month) & 
                         (data['일'] == selected_day) & 
                         (data['측정소명'].isin(selected_stations))]
    
    st.write(f"### 필터링된 데이터 ({selected_month}월 {selected_day}일, 측정소명: {', '.join(selected_stations)})")
    st.write(filtered_data)
    
    # 필터링된 데이터의 통계 요약
    st.write(f"### {selected_month}월 {selected_day}일, 측정소명: {', '.join(selected_stations)}의 데이터 통계 요약")
    st.write(filtered_data.describe())
    
    # 특정 컬럼 선택 및 히스토그램 표시

if __name__ == '__main__':
    app()
