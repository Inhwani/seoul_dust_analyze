import pandas as pd
import matplotlib.pyplot as plt
import folium
import streamlit as st
import streamlit.components.v1 as components
import os

def load_data(file_path):
    try:
        data = pd.read_csv(file_path, encoding='cp949')
        return data
    except Exception as e:
        print(f"Failed to load data: {e}")
        return None

def app():
    # 현재 파일의 디렉토리 경로
    current_dir = os.path.dirname(__file__)
    # 데이터 파일의 상대 경로
    data_file_path = os.path.join(current_dir, '2023daypol.csv')
    # 데이터 로드
    data = load_data(data_file_path)
    if data is None:
        st.error("Failed to load data.")
        return
    
    st.write('## 측정소간 초미세먼지, 미세먼지 차이 비교')
    
    # '측정일시' 열을 datetime 형식으로 변환
    data['측정일시'] = pd.to_datetime(data['측정일시'], format='%Y%m%d', errors='coerce')
    data['미세먼지농도(㎍/㎥)'] = pd.to_numeric(data['미세먼지농도(㎍/㎥)'], errors='coerce')
    data['초미세먼지농도(㎍/㎥)'] = pd.to_numeric(data['초미세먼지농도(㎍/㎥)'], errors='coerce')
    
    # 미세먼지가 80이 넘는 날짜를 계산
    data['date'] = data['측정일시'].dt.date
    high_dust_data = data[data['미세먼지농도(㎍/㎥)'] > 80]
    unique_dates_per_station_pm10 = high_dust_data.groupby(['측정소명', 'date']).size().reset_index(name='count')
    unique_dates_per_station_pm10 = unique_dates_per_station_pm10.groupby('측정소명').size().sort_values(ascending=False)
    
    # 초미세먼지가 35가 넘는 날짜를 계산
    high_dust_data_pm25 = data[data['초미세먼지농도(㎍/㎥)'] > 35]
    unique_dates_per_station_pm25 = high_dust_data_pm25.groupby(['측정소명', 'date']).size().reset_index(name='count')
    unique_dates_per_station_pm25 = unique_dates_per_station_pm25.groupby('측정소명').size().sort_values(ascending=False)
    
    # 미세먼지 히스토그램 그리기
    plt.figure(figsize=(12, 6))
    unique_dates_per_station_pm10.plot(kind='bar', color='skyblue')
    plt.xlabel('측정소명')
    plt.ylabel('고유 날짜 수')
    plt.title('미세먼지가 80 이상인 날짜 수')
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(plt.gcf())
    # 초미세먼지 히스토그램 그리기
    plt.figure(figsize=(12, 6))
    unique_dates_per_station_pm25.plot(kind='bar', color='salmon')
    plt.xlabel('측정소명')
    plt.ylabel('고유 날짜 수')
    plt.title('초미세먼지가 35 이상인 날짜 수')
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(plt.gcf())

    # '산'과 '대로'가 포함된 측정소명을 그룹으로 나누기
    산_group = unique_dates_per_station_pm25[unique_dates_per_station_pm25.index.str.contains('산')]
    대로_group = unique_dates_per_station_pm25[unique_dates_per_station_pm25.index.str.contains('대로')]
    기타_group = unique_dates_per_station_pm25[~unique_dates_per_station_pm25.index.str.contains('산|대로')]

    # 파이 차트 데이터 준비
    pie_data = pd.Series({
        '산 그룹': 산_group.sum(),
        '대로 그룹': 대로_group.sum(),
        '기타 그룹': 기타_group.sum()
    })

    # 파이 차트 그리기
    plt.figure(figsize=(8, 8))
    pie_data.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=['lightblue', 'lightgreen', 'lightcoral'])
    plt.ylabel('')
    plt.title('초미세먼지가 35 이상인 날짜 수 - 그룹별')
    plt.tight_layout()
    st.pyplot(plt.gcf())

    # 서울 미세먼지 측정소 위치 데이터
    locations = [
        {"측정소명": "강남구", "위도": 37.5174, "경도": 127.0473},
        {"측정소명": "홍릉로", "위도": 37.5917, "경도": 127.0196},
        {"측정소명": "행주", "위도": 37.6067, "경도": 126.9304},
        {"측정소명": "항동", "위도": 37.5409, "경도": 127.0657},
        {"측정소명": "한강대로", "위도": 37.5257, "경도": 126.9654},
        {"측정소명": "청계천로", "위도": 37.5691, "경도": 127.0057},
        {"측정소명": "천호대로", "위도": 37.5384, "경도": 127.1247},
        {"측정소명": "중랑구", "위도": 37.5955, "경도": 127.0925},
        {"측정소명": "중구", "위도": 37.5641, "경도": 126.9977},
        {"측정소명": "종로구", "위도": 37.5723, "경도": 126.9877},
        {"측정소명": "종로", "위도": 37.5716, "경도": 126.9984},
        {"측정소명": "정릉로", "위도": 37.6121, "경도": 127.0118},
        {"측정소명": "자연사박물관", "위도": 37.5906, "경도": 127.0094},
        {"측정소명": "은평구", "위도": 37.6071, "경도": 126.9199},
        {"측정소명": "용산", "위도": 37.5299, "경도": 126.9655},
        {"측정소명": "올림픽공원", "위도": 37.5203, "경도": 127.1210},
        {"측정소명": "영등포로", "위도": 37.5272, "경도": 126.9076},
        {"측정소명": "영등포구", "위도": 37.5265, "경도": 126.8959},
        {"측정소명": "양천구", "위도": 37.5169, "경도": 126.8660},
        {"측정소명": "신촌로", "위도": 37.5596, "경도": 126.9427},
        {"측정소명": "송파", "위도": 37.5088, "경도": 127.1046},
        {"측정소명": "세곡", "위도": 37.4704, "경도": 127.0555},
        {"측정소명": "성동구", "위도": 37.5591, "경도": 127.0415},
        {"측정소명": "성북구", "위도": 37.6068, "경도": 127.0228},
        {"측정소명": "화랑로", "위도": 37.6191, "경도": 127.0805},
        {"측정소명": "서초구", "위도": 37.4837, "경도": 127.0324}
    ]
    
    # 지도 생성
    m = folium.Map(location=[37.5502, 126.982], zoom_start=12)
    folium.TileLayer('openstreetmap').add_to(m)

    # 측정소 위치 아이콘 추가
    for location in locations:
        name = location["측정소명"]
        lat = location["위도"]
        lon = location["경도"]
        folium.Marker([lat, lon], popup=name).add_to(m)

    # 지도 저장
    m.save('seoul_air_quality.html')

       # Streamlit을 사용하여 HTML 파일을 표시
    st.title('서울 미세먼지 측정소 지도')
    components.html(open('seoul_air_quality.html', 'r', encoding='utf-8').read(), height=600)

# 앱 실행
if __name__ == '__main__':
    app()