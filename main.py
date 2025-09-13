import streamlit as st
import pandas as pd
import altair as alt
import os

st.set_page_config(page_title="MBTI World Top10", page_icon="🌍", layout="centered")

st.title("🌍 MBTI 유형별 비율 Top10 국가")
st.write("CSV 파일을 기본적으로 같은 폴더에서 불러오고, 없으면 업로드 기능을 사용합니다.")

# ---- 데이터 로드 ----
@st.cache_data
def load_data(file):
    df = pd.read_csv(file, encoding="utf-8")
    df.columns = [c.strip() for c in df.columns]
    return df

# ---- 기본 파일 체크 ----
DATA_PATH = "countriesMBTI_16types.csv"
if os.path.exists(DATA_PATH):
    df = load_data(DATA_PATH)
    st.success(f"✅ 기본 파일 `{DATA_PATH}` 로드 완료")
else:
    st.warning("⚠️ 기본 데이터 파일을 찾을 수 없습니다. CSV 파일을 업로드하세요.")
    uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])
    if uploaded_file is not None:
        df = load_data(uploaded_file)
        st.success("✅ 업로드한 파일 로드 완료")
    else:
        st.stop()

# ---- MBTI 컬럼 목록 ----
MBTI_TYPES = [c for c in df.columns if c.upper() in {
    "INFJ","INFP","INTJ","INTP","ISFJ","ISFP","ISTJ","ISTP",
    "ENFJ","ENFP","ENTJ","ENTP","ESFJ","ESFP","ESTJ","ESTP"}]
MBTI_TYPES = sorted(MBTI_TYPES, key=lambda x: x.upper())

# ---- 사이드바 ----
st.sidebar.header("⚙️ 옵션")
selected_mbti = st.sidebar.selectbox(
    "MBTI 유형을 선택하세요",
    MBTI_TYPES,
    index=MBTI_TYPES.index("INFP") if "INFP" in MBTI_TYPES else 0
)

# ---- Top10 계산 ----
top10 = df[["Country", selected_mbti]].sort_values(by=selected_mbti, ascending=False).head(10)

# ---- Altair 그래프 ----
chart = (
    alt.Chart(top10)
    .mark_bar(color="steelblue")
    .encode(
        x=alt.X(selected_mbti, title=f"{selected_mbti} 비율", axis=alt.Axis(format=",.2f")),
        y=alt.Y("Country", sort="-x", title="국가"),
        tooltip=["Country", alt.Tooltip(selected_mbti, format=",.4f")]
    )
    .interactive()
)

st.subheader(f"'{selected_mbti}' 유형 비율 Top10 국가")
st.altair_chart(chart, use_container_width=True)

# ---- 데이터 테이블 ----
st.write("📋 Top10 국가 데이터")
st.dataframe(top10.style.format({selected_mbti: "{:.4f}"}))
