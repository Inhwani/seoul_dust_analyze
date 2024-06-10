import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

def app():
    st.title('통계 분석')
    
    # 현재 파일의 디렉토리 경로
    current_dir = os.path.dirname(__file__)
    # CSV 파일의 상대 경로
    file_path = os.path.join(current_dir, '2023daypol.csv')
    # 폰트 파일의 절대 경로
    font_path = os.path.abspath(os.path.join(current_dir, 'fonts', 'MaruBuri-Regular.ttf'))

    # CSV 파일 로드
    try:
        data = pd.read_csv(file_path, encoding='cp949')
    except FileNotFoundError:
        st.error("CSV 파일을 찾을 수 없습니다. 경로를 확인하세요.")
        return

    # 폰트 로드 시도
    try:
        if not os.path.isfile(font_path):
            st.error(f"폰트 파일을 찾을 수 없습니다: {font_path}")
            return

        # 폰트 등록 및 설정
        fm.fontManager.addfont(font_path)
        font_prop = fm.FontProperties(fname=font_path)
        plt.rcParams['font.family'] = font_prop.get_name()
        plt.rcParams['axes.unicode_minus'] = False  # 마이너스 폰트 설정
        
        # st.write(f"폰트 파일이 정상적으로 로드되었습니다: {font_prop.get_name()}")
    except RuntimeError as e:
        st.error(f"폰트 파일을 로드하는 중 오류가 발생했습니다: {e}")
        return

    # 데이터 로드
    dust_data = pd.read_csv(file_path, encoding='cp949')  # 인코딩 지정

    # '측정일시' 열을 datetime 형식으로 변환
    dust_data['측정일시'] = pd.to_datetime(dust_data['측정일시'], format="%Y%m%d")

    # 서울시 미세먼지 농도 시계열 그래프 그리기
    st.write("### 서울시 미세먼지 농도")
    x = dust_data['측정일시']
    y1 = dust_data['미세먼지농도(㎍/㎥)']

    fig1, ax1 = plt.subplots(figsize=(8, 6))
    ax1.plot(x, y1, label='미세먼지농도')

    # 기준축으로 80에 주황색 선 그리기
    ax1.axhline(y=80, color='orange', linestyle='--', label='나쁨')

    # 기준축으로 150에 빨간색 선 그리기
    ax1.axhline(y=150, color='red', linestyle='--', label='매우나쁨')

    # 80을 넘는 값에 주황색 마커 찍기
    mask = y1 > 80
    ax1.scatter(x[mask], y1[mask], color='darkorange', marker='o')

    # 150을 넘는 값에 빨간색 마커 찍기
    mask = y1 > 150
    ax1.scatter(x[mask], y1[mask], color='red', marker='o')

    ax1.grid(True, axis='y')
    ax1.set_xlabel('측정일시')
    ax1.set_ylabel('농도')
    ax1.set_title('서울시 미세먼지농도')
    ax1.legend()
    plt.xticks(rotation=45)

    st.pyplot(fig1)

    # 서울시 초미세먼지 농도 시계열 그래프 그리기
    st.write("### 서울시 초미세먼지 농도")
    y2 = dust_data['초미세먼지농도(㎍/㎥)']

    fig2, ax2 = plt.subplots(figsize=(8, 6))
    ax2.plot(x, y2, label='초미세먼지농도', color='blue')

    # 기준축으로 35에 주황색 선 그리기
    ax2.axhline(y=35, color='orange', linestyle='--', label='나쁨')

    # 기준축으로 75에 빨간색 선 그리기
    ax2.axhline(y=75, color='red', linestyle='--', label='매우나쁨')

    # 35을 넘는 값에 주황색 마커 찍기
    mask = y2 > 35
    ax2.scatter(x[mask], y2[mask], color='darkorange', marker='o')

    # 75을 넘는 값에 빨간색 마커 찍기
    mask = y2 > 75
    ax2.scatter(x[mask], y2[mask], color='red', marker='o')

    ax2.grid(True, axis='y')
    ax2.set_xlabel('측정일시')
    ax2.set_ylabel('농도')
    ax2.set_title('서울시 초미세먼지농도')
    ax2.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig2)

    # 고유한 날짜 계산
    dust_data['date'] = dust_data['측정일시'].dt.date

    # 월별로 그룹화하여 미세먼지 농도가 80을 초과하는 고유한 날짜 계산
    unique_dates_pm10 = dust_data[dust_data['미세먼지농도(㎍/㎥)'] > 80].groupby(dust_data['측정일시'].dt.month)['date'].nunique()

    # 월별로 그룹화하여 초미세먼지 농도가 35를 초과하는 고유한 날짜 계산
    unique_dates_pm25 = dust_data[dust_data['초미세먼지농도(㎍/㎥)'] > 35].groupby(dust_data['측정일시'].dt.month)['date'].nunique()

    # 히스토그램 그리기
    st.write("### 월별 미세먼지 및 초미세먼지 농도 초과 고유 날짜 수")
    fig3, ax3 = plt.subplots(figsize=(12, 6))

    ax3.bar(unique_dates_pm10.index - 0.2, unique_dates_pm10.values, width=0.4, color='orange', alpha=0.7, label='미세먼지 > 80')
    ax3.bar(unique_dates_pm25.index + 0.2, unique_dates_pm25.values, width=0.4, color='red', alpha=0.7, label='초미세먼지 > 35')

    ax3.set_xlabel('월')
    ax3.set_ylabel('고유 날짜 수')
    ax3.set_title('월별 미세먼지 및 초미세먼지 농도 초과 고유 날짜 수')
    ax3.legend()
    ax3.set_xticks(unique_dates_pm10.index)  # 월 표시를 위해 x축 값 설정

    st.pyplot(fig3)

if __name__ == '__main__':
    app()
