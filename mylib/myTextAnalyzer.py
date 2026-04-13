import pandas as pd
from collections import Counter

def load_corpus_from_csv(data_filename, column):
    """CSV 파일에서 데이터 읽기"""
    data_df = pd.read_csv(data_filename)

    # Null 값 제거
    if data_df[column].isnull().sum():
        data_df.dropna(subset=[column], inplace=True)

    # 데이터 리스트로 변환
    corpus = list(data_df[column])
    return corpus

def tokenize_korean_corpus(corpus, tokenizer, my_tags=None, my_stopwords=None):
    """한글 텍스트 토큰화"""
    all_token = []

    # 텍스트 토큰화
    for text in corpus:
        # 형태소 분석
        raw_tokens = tokenizer(text)

        # 각 단어와 품사 처리
        for word, tag in raw_tokens:
            # 원하는 품사만 필터링
            if my_tags and tag not in my_tags:
                continue

            # 불용어 제외
            if my_stopwords and word in my_stopwords:
                continue

            # 토큰 추가
            all_token.append(word)

    return all_token

def analyze_word_freq(tokens):
    """단어 빈도 계산"""
    return Counter(tokens)