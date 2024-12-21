import streamlit as st
import openai
import random
import time
import os
from pathlib import Path
from googletrans import Translator

# 번역기 초기화
translator = Translator()

# OpenAI API 키 설정 함수
def setup_openai_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets["OPENAI_API_KEY"]
        except:
            api_key = None
    if not api_key:
        api_key = st.sidebar.text_input("OpenAI API 키를 입력하세요:", type="password")
        if not api_key:
            st.error("OpenAI API 키가 필요합니다. API 키를 입력해주세요.")
            st.stop()
    return api_key

def translate_to_korean(text):
    try:
        result = translator.translate(text, dest='ko')
        return result.text
    except Exception as e:
        st.error(f"번역 중 오류가 발생했습니다: {str(e)}")
        return text

def get_ai_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"""You are a movie expert. 
                Provide a hint for the movie: {st.session_state.current_movie}
                Make it specific but don't reveal the answer directly."""},
                {"role": "user", "content": prompt}
            ]
        )
        hint = response.choices[0].message.content
        # 힌트를 한글로 번역
        korean_hint = translate_to_korean(hint)
        return korean_hint
    except Exception as e:
        return f"Error: {str(e)}"

def initialize_session_state():
    if 'current_movie' not in st.session_state:
        st.session_state.current_movie = None
    if 'hints' not in st.session_state:
        st.session_state.hints = []
    if 'hint_count' not in st.session_state:
        st.session_state.hint_count = 0
    if 'give_up_count' not in st.session_state:
        st.session_state.give_up_count = 0

def generate_new_movie():
    sample_movies = [
        {"en": "The Matrix", "ko": "매트릭스"},
        {"en": "Inception", "ko": "인셉션"},
        {"en": "Parasite", "ko": "기생충"},
        {"en": "Oldboy", "ko": "올드보이"},
        {"en": "The Lord of the Rings", "ko": "반지의 제왕"},
        {"en": "Frozen", "ko": "겨울왕국"},
        {"en": "Avengers", "ko": "어벤져스"},
        {"en": "Titanic", "ko": "타이타닉"},
        {"en": "Contact", "ko": "컨택트"}
    ]
    movie = random.choice(sample_movies)
    # 세션에 영어 제목도 저장
    st.session_state.current_movie_en = movie["en"]
    return movie["ko"]

def get_next_hint(movie):
    hints_template = {
        "매트릭스": [
            "1999년에 개봉한 이 영화는 SF 액션 영화의 역사를 새로 썼다고 평가받는 작품입니다.",
            "주인공은 낮에는 평범한 회사원이지만, 비밀스러운 해커 생활을 하고 있습니다.",
            "빨간색과 파란색 알약 중 하나를 선택하는 장면은 현대 영화사에서 가장 유명한 장면 중 하나가 되었습니다.",
            "우리가 살고 있는 세상이 진짜가 아닐 수도 있다는 충격적인 철학적 질문을 던지는 작품입니다.",
            "존 윅 시리즈로도 유명한 배우가 주연을 맡아 가장 대표적인 작품으로 꼽히는 영화입니다."
        ]
    }
    
    if movie in hints_template and st.session_state.hint_count < len(hints_template[movie]):
        hint = hints_template[movie][st.session_state.hint_count]
        st.session_state.hint_count += 1
        return hint
    else:
        # 미리 정의되지 않은 영화의 경우 AI로 힌트 생성하고 번역
        return get_ai_response(f"Give me hint #{st.session_state.hint_count + 1} for the movie '{st.session_state.current_movie_en}'")

def main():
    st.title("🎬 영화 제목 맞추기 퀴즈")
    
    # OpenAI API 키 설정
    api_key = setup_openai_api_key()
    openai.api_key = api_key
    
    initialize_session_state()
    
    # 새 게임 시작
    if st.session_state.current_movie is None:
        st.session_state.current_movie = generate_new_movie()
        st.session_state.hint_count = 0
        st.session_state.hints = []
        st.session_state.give_up_count = 0
    
    # 현재 힌트 표시
    if len(st.session_state.hints) < 5:
        if len(st.session_state.hints) <= st.session_state.hint_count:
            new_hint = get_next_hint(st.session_state.current_movie)
            st.session_state.hints.append(new_hint)
    
    # 힌트들 표시
    for i, hint in enumerate(st.session_state.hints, 1):
        st.info(f"💡 힌트 {i}: {hint}")
    
    # 사용자 입력
    with st.form(key="answer_form"):
        user_answer = st.text_input("영화 제목을 맞춰보세요:")
        submit_button = st.form_submit_button("정답 확인")
        
        if submit_button and user_answer:
            if user_answer.lower() == st.session_state.current_movie.lower():
                st.success("🎉 정답입니다! 정말 뛰어나시군요.")
                if st.button("새 게임 시작"):
                    st.session_state.current_movie = None
                    st.experimental_rerun()
            else:
                st.error("😅 안타깝네요. 매우 근접하셨는데 아직 정답이 아닙니다.")
                if len(st.session_state.hints) < 5:
                    st.write("💪 포기하지 마세요! 다음 힌트를 확인하고 다시 도전해보세요!")
    
    # 포기하기 옵션
    if st.button("정답 공개"):
        st.session_state.give_up_count += 1
        if st.session_state.give_up_count >= 3:
            st.warning(f"정답은 '{st.session_state.current_movie}' 입니다!")
            if st.button("새 게임 시작하기"):
                st.session_state.current_movie = None
                st.experimental_rerun()
        else:
            fake_answers = ["쇼생크 탈출", "인터스텔라", "라라랜드", "아바타", "터미네이터"]
            fake_answer = random.choice([fa for fa in fake_answers if fa != st.session_state.current_movie])
            st.warning(f"흠... 혹시 '{fake_answer}' 아닐까요? 😉")

if __name__ == "__main__":
    main()
