import streamlit as st
import os
import pandas as pd
from PIL import Image

# 페이지 설정
st.set_page_config(
    page_title="국내 전기차 기업 근황",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 회사 목록 (stock_info 딕셔너리에서 키값만 사용)
companies_by_category = {
    '전기차': ['현대차', '기아'],
    '배터리': ['에코프로비엠', 'LG화학', '금양', 'SK이노베이션'],
    '2차전지': ['LG 에너지솔루션', '삼성SDI', '엘앤에프', '포스코퓨처엠'],
    '전기차충전': ['포스코DX', 'SK 네트웍스', '솔루엠', '롯데이노베이트']
}

# 좌측에 "주식정보", "재무제표", "뉴스"를 선택하는 radio 버튼 추가
option = st.sidebar.radio(
    "옵션",
    ('주식', '재무제표', '뉴스'),
    index=None
)

# 카테고리 선택
if option in ['주식', '재무제표']:
    category = st.sidebar.selectbox("카테고리", list(companies_by_category.keys()))

    # 선택된 카테고리에 따른 회사 목록 선택
    selected_company = st.selectbox("회사를 선택하세요", companies_by_category[category])

# 아무 옵션도 선택하지 않았을 때 기본 화면 표시
if option is None:
    st.title("기업별 분기별 종가 꺾은선 그래프")
    
    # 앱의 설명
    st.markdown("""
    이 애플리케이션은 각 기업의 분기별 종가를 시각화한 그래프를 보여줍니다.
    왼쪽 사이드바에서 보고 싶은 검색 기준을 선택하세요.
    """)

# "주식정보"가 선택되었을 때
elif option == '주식':
    st.markdown(f'{selected_company}⦁KOSPI')

    # data 폴더에서 선택한 회사의 CSV 파일 가져오기
    data_folder = 'data'
    csv_filename = os.path.join(data_folder, f'{selected_company}_full_daily_prices.csv')

    # CSV 파일이 있는지 확인
    if os.path.exists(csv_filename):
        df = pd.read_csv(csv_filename)

        # 날짜를 datetime 형식으로 변환
        df['날짜'] = pd.to_datetime(df['날짜'])

        # 종가 차이 계산 (오늘 종가 - 어제 종가)
        df['종가 차이'] = df['종가'].diff()

        if not df.empty:
            # 컬럼 생성 - 왼쪽에 종가 변화량, 오른쪽에 테이블
            col1, col2 = st.columns([1, 2])  # 비율로 컬럼 너비 조정 (왼쪽 더 크고 오른쪽 더 작게)

            # 최근 두 날짜의 종가 및 변화량 가져오기
            latest_data = df.iloc[0]  # 가장 최근 날짜
            previous_data = df.iloc[1]  # 그 전날

            # 상승/하락 여부 결정
            change = latest_data['종가'] - previous_data['종가']
            if change > 0:
                arrow = "⬆"
                color = "red"
            elif change < 0:
                arrow = "⬇"
                color = "blue"
            else:
                arrow = "➖"
                color = "gray"

            # 왼쪽 컬럼에 상승률 정보 표시
            with col1:              
                # 가격과 '원'을 구분하여 각각 스타일링 (가격을 더 크게)
                latest_price = f"{latest_data['종가']:,}"
                st.markdown(f"<h2>{latest_price}<span style='font-size: 0.9em;'> KRW</span></h2>", unsafe_allow_html=True)
                
                # 상승/하락 변화량 및 상승률 표시 (상승률을 조금 더 작게)
                percent_change = (change / previous_data['종가']) * 100 if previous_data['종가'] != 0 else 0
                st.markdown(f"<h4 style='color:{color};'>{arrow} {abs(change):,.0f} ({abs(percent_change):.2f}%)<span style='font-size: 0.6em;'> </span></h4>", unsafe_allow_html=True)


            # 오른쪽 컬럼에 CSV 파일 테이블로 표시
            with col2:
                # 테이블에서 날짜 전의 인덱스 숫자와 종가 차이 항목 제거
                df_display = df.drop(columns=['종가 차이']).reset_index(drop=True) 
                # 날짜와 주요 정보만 표시
                st.dataframe(df_display[['날짜', '전일비', '시가', '고가', '저가', '종가', '거래량']])  # 필요한 항목만 표시
                

            # 구분선 추가
            st.markdown("---")

            # 구분선 아래에 종가 그래프 표시
            graph_file = f'{selected_company}_price_trend.png'
            image_path = os.path.join(data_folder, graph_file)

            if os.path.exists(image_path):
                # 이미지 파일 열기 및 표시
                image = Image.open(image_path)
                st.image(image, use_column_width=True)
            else:
                st.write(f"{selected_company}의 종가 그래프를 찾을 수 없습니다.")
        else:
            st.write(f"{selected_company}의 데이터를 찾을 수 없습니다.")
    else:
        st.write(f"{selected_company}의 데이터를 찾을 수 없습니다.")

# "재무제표"가 선택되었을 때
elif option == '재무제표':
    st.markdown(f"<h2><span style='font-size: 0.8em;'>재무제표_영업이익</span></h2>", unsafe_allow_html=True)
                
    
    # data 폴더에서 선택한 회사의 그래프 파일 가져오기
    data_folder = 'data'
    graph_file = f'{selected_company}_영업이익_그래프.png'
    image_path = os.path.join(data_folder, graph_file)

    if os.path.exists(image_path):
        # 이미지 파일 열기 및 표시
        image = Image.open(image_path)
        st.image(image, use_column_width=True)
    else:
        st.write(f"{selected_company}의 영업이익 그래프를 찾을 수 없습니다.")

# "뉴스"가 선택되었을 때
elif option == '뉴스':
    st.title("주식 관련 뉴스")
    
    # 데이터 폴더에서 뉴스 CSV 파일 가져오기
    news_csv_path = os.path.join('data', 'evpost_news.csv')

    if os.path.exists(news_csv_path):
        # CSV 파일 읽기
        news_df = pd.read_csv(news_csv_path)

        # 뉴스 제목과 링크 표시
        for index, row in news_df.iterrows():
            st.markdown(f"[{row['제목']}]({row['링크']})")
    else:
        st.write("뉴스 데이터를 찾을 수 없습니다.")



