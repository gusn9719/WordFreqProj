import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from wordcloud import WordCloud

def set_korean_font_for_matplotlib(font_path):
    """matplotlib에서 한글 폰트 설정"""
    # 폰트 이름 추출
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    # 기본 폰트 설정
    rc('font', family=font_name)

def visualize_barhgraph(counter, num_words, title=None, xlabel=None, ylabel=None, font_path=None):
    """빈도수를 막대 그래프로 표시"""
    # 상위 단어들 선택
    wordcount_list = counter.most_common(num_words)

    # 단어와 빈도 분리
    x_list = [word for word, count in wordcount_list]
    y_list = [count for word, count in wordcount_list]

    # 한글 폰트 적용
    if font_path:
        set_korean_font_for_matplotlib(font_path)

    # 작은 크기로 기본 표시
    plt.figure(figsize=(6,4))
    plt.barh(x_list[::-1], y_list[::-1])  # 역순 정렬

    # 라벨 설정
    if title: plt.title(title)
    if xlabel: plt.xlabel(xlabel)
    if ylabel: plt.ylabel(ylabel)

    plt.tight_layout()
    st.pyplot(plt)

    # 확대 보기 옵션
    with st.expander("📊 그래프 크게 보기"):
        plt.figure(figsize=(12,8))
        plt.barh(x_list[::-1], y_list[::-1])

        if title: plt.title(title, fontsize=16)
        if xlabel: plt.xlabel(xlabel, fontsize=12)
        if ylabel: plt.ylabel(ylabel, fontsize=12)

        plt.tight_layout()
        st.pyplot(plt)

def visualize_wordcloud(counter, num_words, font_path):
    """워드 클라우드 시각화"""
    # 워드 클라우드 설정
    wc = WordCloud(
        font_path=font_path,
        max_words=num_words,
        width=400,
        height=300,
        background_color='ivory'
    )

    # 빈도 데이터를 이미지로 변환
    wc = wc.generate_from_frequencies(counter)

    # 작은 크기로 기본 표시
    plt.figure(figsize=(6,4))
    plt.imshow(wc)
    plt.axis('off')  # 축 숨기기

    st.pyplot(plt)

    # 확대 보기 옵션
    with st.expander("☁️ 워드클라우드 크게 보기"):
        # 큰 크기로 워드클라우드 생성
        wc_large = WordCloud(
            font_path=font_path,
            max_words=num_words,
            width=800,
            height=600,
            background_color='ivory'
        ).generate_from_frequencies(counter)

        plt.figure(figsize=(10,6))
        plt.imshow(wc_large)
        plt.axis('off')

        st.pyplot(plt)