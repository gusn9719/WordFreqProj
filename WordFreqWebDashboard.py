import streamlit as st
import pandas as pd
import os
from mylib import myTextAnalyzer as ta
from mylib import mySTVisualizer as sv

st.set_page_config(layout="wide")

st.title("단어 빈도 시각화")

# 모달 함수들
@st.dialog("데이터 확인하기" , width="large")
def show_data_modal(df):
    preview_count = st.slider("확인할 데이터 수", 5, 50, 10)
    st.dataframe(df.head(preview_count))

@st.dialog("불용어 설정" , width="large")
def show_stopwords_modal():
    # 기존에 저장된 불용어가 있다면 불러오기
    current_stopwords = st.session_state.get("stopwords", "")

    stopwords_input = st.text_area(
        "불용어 입력 (쉼표로 구분)",
        value=current_stopwords
    )

    if st.button("저장"):
        st.session_state.stopwords = stopwords_input
        st.rerun()  # 저장 후 새로고침하면서 모달 닫힘

# 사이드바 설정
with st.sidebar:
    st.header("파일 선택")

    data_file = st.file_uploader("CSV 파일 업로드", type=['csv'])


    # 파일이 있을 때만 컬럼 선택
    if data_file:
        df = pd.read_csv(data_file)
        data_file.seek(0)
        # 컬럼 선택 (사이드바)
        column_name = st.selectbox("데이터 컬럼 선택", df.columns)

    # 명령 버튼
    if st.button("데이터 파일 확인", key="data_preview_btn"):
        if not data_file:
            st.warning("먼저 CSV 파일을 업로드해주세요")
        else:
            show_data_modal(df)

    if st.button("불용어 설정", key="stopwords_btn"):
        if not data_file:
            st.warning("먼저 CSV 파일을 업로드해주세요")
        else:
            show_stopwords_modal()

    

    st.header("분석 옵션")

    # 빈도수 그래프 표시 여부
    show_bar = st.checkbox("빈도수 그래프", value=True)
    graph_word_count = st.slider("그래프 단어 수", 10, 50, 20)

    # 워드클라우드 표시 여부
    show_wc = st.checkbox("워드 클라우드", value=True)
    wc_word_count = st.slider("워드클라우드 단어 수", 20, 500, 100)

    # 분석 시작 버튼
    analyze_btn = st.button("분석 시작", key="analyze_btn")
    if analyze_btn and not data_file:
        st.warning("먼저 CSV 파일을 업로드해주세요")
        analyze_btn = False

# 데이터 파일 미리보기
# (dialog 데코레이터 사용으로 제거됨)

# 불용어 설정
# (dialog 데코레이터 사용으로 제거됨)

# 분석 처리
if data_file and analyze_btn:

    # 불용어 반영
    stopwords = None
    if "stopwords" in st.session_state:
        stopwords = [w.strip() for w in st.session_state.stopwords.split(",")]

    # 한글 폰트 경로 설정
    font_path = os.path.join(os.getcwd(), "SEOULHANGANGB.TTF")

    # 파일에서 데이터 읽어오기
    corpus = ta.load_corpus_from_csv(data_file, column_name)

    with st.spinner("분석 중..."):
        # 형태소 분석기 설정
        from konlpy.tag import Okt
        tokenizer = Okt().pos
        # 명사, 동사, 형용사만 뽑으려고
        my_tags = ['Noun', 'Verb', 'Adjective']

        # 텍스트 토큰화
        tokens = ta.tokenize_korean_corpus(
            corpus,
            tokenizer,
            my_tags=my_tags,
            my_stopwords=stopwords
        )

        # 단어 빈도 계산
        counter = ta.analyze_word_freq(tokens)

    # 분석 결과 요약 표시
    col1, col2 = st.columns(2)
    col1.metric("총 단어 수", len(tokens))
    col2.metric("고유 단어 수", len(counter))

    if show_bar:
        st.subheader("빈도수 그래프")
        sv.visualize_barhgraph(
            counter,
            graph_word_count,
            font_path=font_path
        )

    if show_wc:
        st.subheader("워드 클라우드")
        sv.visualize_wordcloud(
            counter,
            wc_word_count,
            font_path=font_path
        )