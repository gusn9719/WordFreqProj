import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from wordcloud import WordCloud

def set_korean_font_for_matplotlib(font_path):
    """matplotlib에서 한글 폰트 설정"""
    # 이름만 꺼내서 rc('font', family=...)에 넣었더니 한글이 다 네모로 깨졌음.
    # matplotlib는 자기 폰트 목록에 등록된 이름만 찾는데, repo 안에 TTF만
    # 있고 등록은 안 돼 있어서 못 찾고 기본 폰트로 떨어진 거였음.
    # addfont()로 폰트 파일 자체를 먼저 등록해야 그 이름이 먹힌다.
    font_manager.fontManager.addfont(font_path)
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font_name)

def visualize_barhgraph(counter, num_words, title=None, xlabel=None, ylabel=None, font_path=None):
    """빈도수를 막대 그래프로 표시"""
    wordcount_list = counter.most_common(num_words)

    x_list = [word for word, count in wordcount_list]
    y_list = [count for word, count in wordcount_list]

    # 폰트는 그리기 전에 잡아둬야 그래프에 반영됨 (끝나고 설정하면 안 먹힘)
    if font_path:
        set_korean_font_for_matplotlib(font_path)

    plt.figure(figsize=(6, 4))
    # barh는 아래에서 위로 쌓여서, [::-1]로 뒤집어야 1등이 맨 위로 옴
    plt.barh(x_list[::-1], y_list[::-1])
    if title: plt.title(title)
    if xlabel: plt.xlabel(xlabel)
    if ylabel: plt.ylabel(ylabel)
    plt.tight_layout()
    st.pyplot(plt)
    # figure 안 닫으면 pyplot이 계속 들고 있어서 분석 반복하면 쌓임 (경고도 뜸)
    plt.close()

def visualize_wordcloud(counter, num_words, font_path):
    """워드 클라우드 시각화"""
    # WordCloud는 font_path를 안 주면 한글이 다 네모(□)로 깨져 나옴
    wc = WordCloud(
        font_path=font_path,
        max_words=num_words,
        width=400,
        height=300,
        background_color='ivory'
    ).generate_from_frequencies(counter)
    plt.figure(figsize=(6, 4))
    plt.imshow(wc)
    plt.axis('off')  # 워드클라우드라 축 눈금은 필요 없음
    st.pyplot(plt)
    plt.close()  # 막대그래프랑 같은 이유 - figure 누적 막으려고 닫음