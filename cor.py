import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

def app():
    st.title('Correlation Analysis')
    
    # 현재 파일의 디렉토리 경로
    current_dir = os.path.dirname(__file__)
    # CSV 파일의 상대 경로
    file_path = os.path.join(current_dir, '2023daypol.csv')
    # 폰트 파일의 상대 경로
    font_path = os.path.join(current_dir, 'fonts', 'MaruBuri-Regular.ttf')
    
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
    
    # 데이터 전처리: '측정일시' 열 제외
    if '측정일시' in data.columns:
        data = data.drop(columns=['측정일시'])
    
    # 수치형 데이터만 선택하여 상관관계 분석
    numeric_data = data.select_dtypes(include=['float64', 'int64'])

    # 상관관계 분석
    correlation_matrix = numeric_data.corr()

    st.header('Correlation Matrix')
    st.write(correlation_matrix)

    # 상관관계 행렬 히트맵 시각화
    st.header('Correlation Heatmap')
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
    st.pyplot(plt)
    
# `cor.py` 파일의 `app` 함수가 실행되도록 하세요.
if __name__ == "__main__":
    app()
