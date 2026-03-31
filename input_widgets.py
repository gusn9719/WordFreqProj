import streamlit as st 
# Streamlit (Stream(흐름) + lit(가볍게 밝히다) -> 데이터 분석 스크립트를 물 흐르듯 가볍고 빠르게 웹 화면으로 띄워주는 파이썬 라이브러리)

st.title("Streamlit 기본 API 살펴보기")
st.header("Input widgets") 
# Widget (Window(창) + Gadget(도구) -> 화면상에서 사용자가 클릭하거나 값을 입력할 수 있게 해주는 작은 조작 도구들)

# Button (Button(단추) -> 클릭하면 특정 동작을 일회성으로 실행하는 단추)
st.button("버튼")
st.success("clicked button") # 초록색 성공 메시지 출력

st.link_button("Go to gallery", "https://streamlit.io/gallery")

# Radio
ml_radio = st.radio(
    "머신러닝 방법", 
    ("신경망", "랜덤포레스트", "SVM"), 
    index=1 # 인데스 1인 "랜덤포레스트"를 기본 선택값으로 지정
)
st.info(f"나의 선택 : {ml_radio}")

# Checkbox (Check(확인하다) + Box(상자) -> 네모난 상자에 'V' 표시를 하여 해당 항목의 활성화 여부를 확인하는 요소)
st.checkbox("토큰화")

# Selectbox (Select(선택하다) + Box(상자) -> 클릭하면 아래로 펼쳐지는 목록 중 하나를 고를 수 있는 상자)
ml_select = st.selectbox(
    "머신러닝 방법", 
    ("SVM", "랜덤포레스트", "신경망")
)
st.info(ml_select)

# Multiselect (Multi(다중) + Select(선택하다) -> 드롭다운 목록에서 여러 개의 항목을 동시에 선택할 수 있는 입력란)
ml_method_multi = st.multiselect(
    "머신러닝 방법", 
    ["랜덤포레스트", "신경망", "SVM"], 
    default=["랜덤포레스트"] 
)

if ml_method_multi:
    st.info(ml_method_multi)

weight = st.slider("가중치", 0, 10, 5) # 최소 0, 최대 10, 기본값 5
st.info(f"가중치 : {weight}")