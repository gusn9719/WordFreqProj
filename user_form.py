import streamlit as st

st.title("Streamlit 기본 API 살펴보기")
st.header("사용자 입력 폼 만들기")

with st.form(key="user_input_form"):
    st.subheader("사용자 입력 폼")
    
    name = st.text_input("이름")
    age = st.number_input("나이", min_value=1, max_value=120)
    agree = st.checkbox("약관에 동의합니다")
    
    submit_button = st.form_submit_button(label="제출")

if submit_button:
    if not name.strip(): # strip() 메서드는 문자열 양쪽의 공백을 제거합니다. 
        st.error("이름을 입력해야 제출할 수 있습니다.")
    elif not agree:
        st.error("약관에 동의해야 제출할 수 있습니다.")
    else:
        st.write(f"이름: {name}, 나이: {age}")
        st.success("약관에 동의했습니다.")