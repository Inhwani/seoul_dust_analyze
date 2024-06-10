import pandas as pd
import os

def load_data():
    # 현재 파일의 디렉토리 경로
    current_dir = os.path.dirname(__file__)
    # 파일의 상대 경로
    file_path = os.path.join(current_dir, '2023daypol.csv')
    
    # 데이터 로드
    data = pd.read_csv(file_path, encoding='cp949')  # 인코딩 지정
    return data

def preprocess_data(data):
    data = data.dropna()
    return data
