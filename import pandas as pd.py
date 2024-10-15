import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 데이터 읽기
df = pd.read_csv("삼성SDI_daily_prices.csv")

# 날짜 형식 변환
df['날짜'] = pd.to_datetime(df['날짜'])

# 그래프 스타일 설정
sns.set(style="whitegrid")

# 그래프 그리기
plt.figure(figsize=(12, 6))
plt.plot(df['날짜'], df['종가'], marker='o', linestyle='-', color='b', label='종가')

# 그래프 제목 및 레이블 설정
plt.title('삼성SDI 종가 변동 추이', fontsize=16)
plt.xlabel('날짜', fontsize=14)
plt.ylabel('종가 (원)', fontsize=14)
plt.xticks(rotation=45)  # x축 레이블 회전
plt.legend()  # 범례 추가
plt.tight_layout()  # 레이아웃 조정

# 그래프 출력
plt.show()