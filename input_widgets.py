import streamlit as st

st.title("Streamlit 기본 API 살펴보기")
st.header("Input widgets")
# 입력 위젯들 하나씩 연습

# 버튼은 누른 그 실행 때만 True (보통 if st.button(): 로 받음)
st.button("버튼")
st.success("clicked button") # 초록색 성공 메시지

st.link_button("Go to gallery", "https://streamlit.io/gallery")

# 라디오 - 보기 중 하나만
ml_radio = st.radio(
    "머신러닝 방법",
    ("신경망", "랜덤포레스트", "SVM"),
    index=1 # 기본 선택값 = 인덱스 1 ("랜덤포레스트")
)
st.info(f"나의 선택 : {ml_radio}")

# 체크박스 - 체크 True / 해제 False
st.checkbox("토큰화")

# 셀렉트박스 - 드롭다운에서 하나, 고른 값 반환
ml_select = st.selectbox(
    "머신러닝 방법",
    ("SVM", "랜덤포레스트", "신경망")
)
st.info(ml_select)

# 멀티셀렉트 - 여러 개 선택, 리스트로 반환 (radio랑 헷갈렸던 부분)
ml_method_multi = st.multiselect(
    "머신러닝 방법", 
    ["랜덤포레스트", "신경망", "SVM"], 
    default=["랜덤포레스트"] 
)

if ml_method_multi:
    st.info(ml_method_multi)

weight = st.slider("가중치", 0, 10, 5) # 최소 0, 최대 10, 기본값 5
st.info(f"가중치 : {weight}")