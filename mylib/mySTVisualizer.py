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

    # 폰트는 plt로 그리기 전에 잡아둬야 그래프에 반영됨.
    # generate 다 끝난 뒤에 설정하면 안 먹혀서 순서 때문에 한참 헤맸음.
    if font_path:
        set_korean_font_for_matplotlib(font_path)

    # 작은 그래프랑 expander 안의 큰 그래프 코드가 완전히 똑같아서
    # 통째로 복붙해뒀었는데, 한쪽만 고치면 어긋나서 함수로 한 번만 그림.
    def draw(figsize):
        plt.figure(figsize=figsize)
        # barh는 아래에서 위로 쌓여서 그냥 그리면 1등이 맨 밑으로 감.
        # [::-1]로 뒤집어 줘야 1등이 맨 위로 옴.
        plt.barh(x_list[::-1], y_list[::-1])
        if title: plt.title(title)
        if xlabel: plt.xlabel(xlabel)
        if ylabel: plt.ylabel(ylabel)
        plt.tight_layout()
        st.pyplot(plt)
        # pyplot이 만든 figure를 안 닫으면 계속 메모리에 들고 있어서
        # 분석을 반복할수록 figure가 쌓임(경고도 뜸). 그려준 뒤 바로 닫음.
        plt.close()

    draw((6, 4))
    with st.expander("📊 그래프 크게 보기"):
        draw((12, 8))

def visualize_wordcloud(counter, num_words, font_path):
    """워드 클라우드 시각화"""
    # WordCloud는 font_path를 안 주면 한글이 다 네모(□)로 깨져 나옴.
    # 작은 거/큰 거 만드는 코드가 거의 같아서, 해상도만 인자로 받아
    # 함수로 한 번만 만들게 정리(여기도 expander에 복붙돼 있었음).
    def draw(wc_size, figsize):
        wc = WordCloud(
            font_path=font_path,
            max_words=num_words,
            width=wc_size[0],
            height=wc_size[1],
            background_color='ivory'
        ).generate_from_frequencies(counter)
        plt.figure(figsize=figsize)
        plt.imshow(wc)
        plt.axis('off')  # 워드클라우드라 축 눈금은 필요 없음
        st.pyplot(plt)
        plt.close()  # 위 막대그래프랑 같은 이유 - figure 누적 막으려고 닫음

    draw((400, 300), (6, 4))
    with st.expander("☁️ 워드클라우드 크게 보기"):
        draw((800, 600), (10, 6))