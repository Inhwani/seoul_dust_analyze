import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

def app():
    st.title("Past & Future Data Visualization")
    
    # 현재 파일의 디렉토리 경로
    current_dir = os.path.dirname(__file__)
    # 파일의 상대 경로
    file_path = os.path.join(current_dir, 'year_pol.csv')
    
    # Load the data
    data = pd.read_csv(file_path, encoding='cp949')
    
    # Exclude specific stations
    excluded_stations = ['구로구2', '송파구2','홍지문']
    data = data[~data['측정소명'].isin(excluded_stations)]
    
    # Sidebar for user input
    selected_station = st.selectbox('Select Station', data['측정소명'].unique())

    # Filter data based on selection
    filtered_data = data[(data['측정소명'] == selected_station) & (data['측정년도'] >= 2016) & (data['측정년도'] <= 2024)]

    if not filtered_data.empty:
        st.write(f"### Data for {selected_station} from 2016 to 2024")
        st.dataframe(filtered_data)

        # Plotting the selected data
        cols_to_plot = ['이산화질소농도(ppm)', '오존농도(ppm)', '일산화탄소농도(ppm)', 
                        '아황산가스(ppm)', '미세먼지(㎍/㎥)', '초미세먼지(㎍/㎥)']

        fig, ax = plt.subplots(figsize=(10, 6))
        for col in cols_to_plot:
            ax.plot(filtered_data['측정년도'], filtered_data[col], label=col)
        ax.set_xlabel('Year')
        ax.set_ylabel('Concentration')
        ax.set_title(f'Pollutant Levels from 2016 to 2024 - {selected_station}')
        ax.legend()
        st.pyplot(fig)
    else:
        st.write("No data available for the selected station.")

if __name__ == "__main__":
    app()
