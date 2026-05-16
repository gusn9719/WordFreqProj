import pandas as pd
from collections import Counter

def load_corpus_from_csv(data_filename, column):
    """CSV 파일에서 데이터 읽기"""
    data_df = pd.read_csv(data_filename)

    # NaN이 섞인 행이 있으면 Okt가 float을 받았다고 에러를 뱉음.
    # 그래서 토큰화에 넘기기 전에 빈 행을 미리 떨어뜨려 둠.
    if data_df[column].isnull().sum():
        data_df.dropna(subset=[column], inplace=True)

    # 데이터 리스트로 변환
    corpus = list(data_df[column])
    return corpus

def tokenize_korean_corpus(corpus, tokenizer, my_tags=None, my_stopwords=None):
    """한글 텍스트 토큰화"""
    all_token = []

    for text in corpus:
        # 사용자가 숫자 컬럼을 골라버리면 Okt가 int/float를 받고 죽음.
        # NaN은 위에서 drop했어도 숫자 셀은 그대로라, 여기서 str로 맞춰 줌.
        raw_tokens = tokenizer(str(text))

        # .pos는 (단어, 품사) 튜플 리스트를 줌. 조사·어미까지 다 세면
        # 빈도가 의미 없어져서, 넘겨받은 태그(명사·동사·형용사)만 남김.
        for word, tag in raw_tokens:
            if my_tags and tag not in my_tags:
                continue

            # 불용어는 여기서 한 번 더 걸러냄
            if my_stopwords and word in my_stopwords:
                continue

            all_token.append(word)

    return all_token

def analyze_word_freq(tokens):
    """단어 빈도 계산"""
    return Counter(tokens)