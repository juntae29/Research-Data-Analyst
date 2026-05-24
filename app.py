import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 1. 웹 페이지 기본 레이아웃 및 제목 설정
st.set_page_config(page_title="Academic Research Data Dashboard", layout="wide")
st.title("📊 Academic Research Data Analyst Dashboard")
st.markdown("---")

# 2. 샘플 학술 데이터 셋 생성 (데이터 파일 부재 시 예외 처리 포함)
@st.cache_data
def load_academic_data():
    # 학술 연구 분석을 위한 가상의 키워드 및 통계 데이터 구성
    words = ["Data Analysis", "Semantic Network", "Statistics", "Research", "Methodology", 
             "Python", "Streamlit", "Visualization", "Algorithm", "Academic", "Text Mining"]
    
    np.random.seed(42)
    data = {
        "Keywords": np.random.choice(words, size=100),
        "Citation_Count": np.random.randint(10, 150, size=100),
        "Relevance_Score": np.random.uniform(0.5, 1.0, size=100),
        "Publication_Year": np.random.choice([2024, 2025, 2026], size=100)
    }
    return pd.DataFrame(data)

df = load_academic_data()

# 3. 사이드바 필터 구성
st.sidebar.header("🔍 Filter Options")
selected_year = st.sidebar.multiselect("Select Publication Year", options=df["Publication_Year"].unique(), default=df["Publication_Year"].unique())

# 필터링 적용
filtered_df = df[df["Publication_Year"].isin(selected_year)]

# 4. 메인 대시보드 시각화 레이아웃 구획 (2분할)
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Research Keywords Word Cloud")
    # 텍스트 마이닝 빈도수 기반 워드클라우드 생성
    text = " ".join(filtered_df["Keywords"])
    if text.strip():
        wordcloud = WordCloud(width=800, height=400, background_color="white", colormap="viridis").generate(text)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation="蝸bilinear")
        ax.axis("off")
        st.pyplot(fig)
    else:
        st.info("No data available for word cloud.")

with col2:
    st.subheader("📈 Citations by Research Metric")
    # 키워드별 평균 인용 횟수 시각화 그래프
    if not filtered_df.empty:
        chart_data = filtered_df.groupby("Keywords")["Citation_Count"].mean().sort_values(ascending=False)
        st.bar_chart(chart_data)
    else:
        st.info("No data available for chart.")

st.markdown("---")

# 5. 하단 데이터 테이블 인출
st.subheader("📋 Filtered Data Table Overview")
st.dataframe(filtered_df, use_container_width=True)