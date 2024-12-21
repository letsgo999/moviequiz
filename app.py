import streamlit as st
import openai
import random
import time
import os

# OpenAI API 설정
openai.api_key = st.secrets["OPENAI_API_KEY"]

def initialize_session_state():
    if 'current_movie' not in st.session_state:
        st.session_state.current_movie = None
    if 'hints' not in st.session_state:
        st.session_state.hints = []
    if 'hint_count' not in st.session_state:
        st.session_state.hint_count = 0
    if 'give_up_count' not in st.session_state:
        st.session_state.give_up_count = 0
    if 'messages' not in st.session_state:
        st.session_state.messages = []

def get_ai_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """당신은 세계 영화사에 해박한 영화 전문가입니다. 
                현재 영화 제목 맞추기 게임을 진행중이며, 다음 영화에 대한 힌트를 제공해야 합니다: {current_movie}
                힌트는 구체적이되 정답을 직접적으로 노출하지 않도록 해주세요."""},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def generate_new_movie():
    # 실제 구현시에는 데이터베이스나 목록에서 선택하도록 수정
    sample_movies = [
        "매트릭스",
        "인셉션",
        "타이타닉",
        "반지의 제왕",
        "겨울왕국",
        "어벤져스",
        "기생충",
        "올드보이",
        "컨택트"
    ]
    return random.choice(sample_movies)

def get_next_hint(movie):
    hints_template = {
        "매트릭스": [
            "1999년에 개봉한 이 영화는 SF 액션의 새로운 지평을 열었습니다.",
            "주인공은 프로그래머이자 해커입니다.",
            "'빨간 알약'과 '파란 알약'이라는 상징적인 장면이 유명합니다.",
            "영화의 주요 테마는 현실과 가상현실의 경계에 관한 것입니다.",
            "키아누 리브스가 주연을 맡았습니다."
        ]
    }
    
    if movie in hints_template and st.session_state.hint_count < len(hints_template[movie]):
        hint = hints_template[movie][st.session_state.hint_count]
        st.session_state.hint_count += 1
        return hint
    else:
        # 미리 정의되지 않은 영화의 경우 AI로 힌트 생성
        return get_ai_response(f"영화 '{movie}'에 대한 {st.session_state.hint_count + 1}번째 힌트를 제공해주세요.")

def main():
    st.title("🎬 영화 제목 맞추기 퀴즈")
    
    # API 키 확인
    if "OPENAI_API_KEY" not in st.secrets:
        st.error("OpenAI API 키가 설정되지 않았습니다. Streamlit 클라우드에서 환경변수를 설정해주세요.")
        st.stop()
    
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
            fake_answers = ["쇼생크 탈출", "인터스텔라", "라라랜드", "아바타", "기생충"]
            fake_answer = random.choice([fa for fa in fake_answers if fa != st.session_state.current_movie])
            st.warning(f"흠... 혹시 '{fake_answer}' 아닐까요? 😉")

if __name__ == "__main__":
    main()
