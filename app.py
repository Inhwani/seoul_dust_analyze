import streamlit as st
import home
import eda
import statistic
import viz
import pf
import cor
import con
# 페이지 설정
PAGES = {
    "Home": home,
    "EDA": eda,
    "Statistics": statistic,
    "Visualization": viz,
    "past&future": pf,
    "cor": cor,
    "conclusion": con
}

# 사이드바에서 페이지 선택
st.sidebar.title('빅데이터분석프로젝트')

# 사이드바에 사용자 프로필 추가 (예시)
st.sidebar.markdown('''
    ### User Profile
    **Name:** 최인환  
    **학번:** 20222594  
    **Department:** 미세먼지 분석
''')

# 사이드바에 페이지 선택 라디오 버튼
selection = st.sidebar.radio("Select a page:", list(PAGES.keys()), index=0)

# 선택한 페이지 로드
page = PAGES[selection]
page.app()

# 사이드바에 추가적인 정보 추가
st.sidebar.markdown('''
    ### Additional Information
    - [GitHub](https://github.com/inhwani)
    - [Documentation](https://docs.streamlit.io)
    - [Contact Us](abc@naver.com)
''')  # 추가 정보 링크
