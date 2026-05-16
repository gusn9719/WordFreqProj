import streamlit as st
import pandas as pd
import os
from mylib import myTextAnalyzer as ta
from mylib import mySTVisualizer as sv

st.set_page_config(layout="wide")

st.title("단어 빈도 시각화")

# Okt 안에 JVM이 통째로 들어있어서, 분석 버튼 누를 때마다 새로 만들면
# Streamlit Cloud에서 메모리가 못 버티고 터졌음(MemoryError).
# cache_resource로 딱 한 번만 만들어서 계속 재사용하게 바꿈.
# 거기에 힙 기본값 1024MB가 클라우드엔 너무 커서 512로 줄임.
@st.cache_resource
def load_tokenizer():
    from konlpy.tag import Okt
    return Okt(max_heap_size=512).pos

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
        # read_csv가 업로드 버퍼를 끝까지 읽어버려서, seek(0)으로 되감아 두지
        # 않으면 분석할 때 다시 read_csv 했을 때 빈 값이 나와서 한참 헤맸음.
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
    # 파일 없는데 분석을 누르면 아래 분석 코드에서 그대로 에러가 남.
    # 미리 경고만 띄우고 버튼 값도 False로 꺼서 분석 블록에 안 들어가게 막음.
    if analyze_btn and not data_file:
        st.warning("먼저 CSV 파일을 업로드해주세요")
        analyze_btn = False

# 분석 처리
# Streamlit은 버튼 누를 때마다 스크립트를 처음부터 다시 돌림. 그래서 결과를
# 여기서 바로 그리기만 하면, "데이터 확인"이나 "불용어 설정" 같은 다른 버튼을
# 누른 순간 analyze_btn이 False가 되면서 그래프가 통째로 사라졌음.
# → 분석은 버튼 눌렀을 때만 하고, 결과는 session_state에 넣어둔 다음
#   아래에서 그걸 보고 그리게 분리함. 그러면 rerun 돼도 안 없어짐.
if data_file and analyze_btn:

    # 불용어 반영
    # 입력이 "a, b, c"처럼 쉼표로 이어붙은 한 덩어리로 들어와서, split(",")으로
    # 쪼개고 strip()으로 공백을 떼야 단어별로 걸러짐. 끝에 쉼표가 더 붙거나
    # 입력이 비면 ''가 끼는데, if w.strip()로 빼버림.
    stopwords = None
    if "stopwords" in st.session_state:
        stopwords = [w.strip() for w in st.session_state.stopwords.split(",") if w.strip()]

    # 파일에서 데이터 읽어오기
    corpus = ta.load_corpus_from_csv(data_file, column_name)

    with st.spinner("분석 중..."):
        # 형태소 분석기 (위에서 캐시해둔 JVM 그대로 재사용)
        tokenizer = load_tokenizer()
        # .pos는 (단어, 품사) 튜플을 줌. 조사·어미까지 세면 의미가 없어서
        # 명사·동사·형용사만 남기려고 태그를 추려둠.
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

    # 결과만 세션에 보관 (tokens 전체는 무거우니 개수만 저장)
    st.session_state["analysis"] = {"counter": counter, "total": len(tokens)}

# 저장된 결과가 있으면 어떤 rerun이든 다시 그려줌
if "analysis" in st.session_state:
    result = st.session_state["analysis"]
    counter = result["counter"]

    # 한글 폰트 경로 설정 (그릴 때만 필요)
    font_path = os.path.join(os.getcwd(), "SEOULHANGANGB.TTF")

    # 분석 결과 요약 표시
    col1, col2 = st.columns(2)
    col1.metric("총 단어 수", result["total"])
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
