import streamlit as st

def app():
    st.title('2023년 데이터 분석 대시보드')
    st.write("""
    이 대시보드는 2023년 데이터를 다양한 시각화 및 통계 분석을 통해 분석합니다.
    사이드바에서 분석 페이지를 선택할 수 있습니다.
    """)

    st.header("대기 오염 물질 정보")
    
    pollutants = {
        "이산화질소 (NO2)": "자동차 배기가스, 공업용 연소시설, 발전소 등에서 배출되는 기체입니다. 호흡기 질환, 폐 질환, 산성비 등을 유발할 수 있습니다.",
        "오존 (O3)": "태양 복사선과 오염 물질이 반응하여 생성되는 기체입니다. 호흡기 질환, 눈 자극, 폐 기능 저하 등을 유발할 수 있습니다.",
        "일산화탄소 (CO)": "불완전 연소 과정에서 발생하는 기체입니다. 혈액 내 산소 운반을 방해하여 일산화탄소 중독을 유발할 수 있습니다.",
        "아황산가스 (SO2)": "화석 연료 연소, 산업 공정 등에서 배출되는 기체입니다. 호흡기 질환, 눈 자극, 폐 기능 저하 등을 유발할 수 있습니다.",
        "미세먼지 (PM10)": "입자의 크기가 10㎛ 이하인 먼지입니다. 호흡기 질환, 심혈관 질환, 암 등을 유발할 수 있습니다.",
        "초미세먼지 (PM2.5)": "입자의 크기가 2.5㎛ 이하인 먼지입니다. 미세먼지보다 더욱 건강에 해로운 것으로 알려져 있습니다. 호흡기 질환, 심혈관 질환, 암 등을 유발할 수 있습니다."
    }
    
    for pollutant, description in pollutants.items():
        st.subheader(pollutant)
        st.write(description)

if __name__ == '__main__':
    app()
