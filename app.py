import streamlit as st
import openai
import random
import time
import os
from pathlib import Path

# OpenAI API 키 설정 함수
def setup_openai_api_key():
    # 1. 환경변수에서 확인
    api_key = os.getenv("OPENAI_API_KEY")
    
    # 2. Streamlit secrets에서 확인
    if not api_key:
        try:
            api_key = st.secrets["OPENAI_API_KEY"]
        except:
            api_key = None
    
    # 3. 사이드바에서 입력 받기
    if not api_key:
        api_key = st.sidebar.text_input("OpenAI API 키를 입력하세요:", type="password")
        if not api_key:
            st.error("OpenAI API 키가 필요합니다. API 키를 입력해주세요.")
            st.stop()
    
    return api_key

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
                {"role": "system", "content": """당신은 세계 영화사에 해박한 한국인 영화 전문가입니다. 
                현재 영화 제목 맞추기 게임을 진행중이며, 다음 영화에 대한 힌트를 제공해야 합니다: {current_movie}
                힌트는 반드시 한국어로 제공하되, 구체적이고 재미있게 설명하면서도 정답을 직접적으로 노출하지 않도록 해주세요.
                답변은 반드시 한국어로만 해주세요."""},
                {"role": "user", "content": prompt + " (한국어로 답변해주세요.)"}
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
            "1999년에 개봉한 이 영화는 SF 액션 영화의 역사를 새로 썼다고 평가받는 작품입니다.",
            "주인공은 낮에는 평범한 회사원이지만, 비밀스러운 해커 생활을 하고 있습니다.",
            "빨간색과 파란색 알약 중 하나를 선택하는 장면은 현대 영화사에서 가장 유명한 장면 중 하나가 되었습니다.",
            "우리가 살고 있는 세상이 진짜가 아닐 수도 있다는 충격적인 철학적 질문을 던지는 작품입니다.",
            "존 윅 시리즈로도 유명한 배우가 주연을 맡아 가장 대표적인 작품으로 꼽히는 영화입니다."
        ],
        "인셉션": [
            "2010년 개봉한 이 영화는 꿈과 현실의 경계를 넘나드는 독특한 설정으로 화제를 모았습니다.",
            "주인공은 다른 사람의 꿈에 침투해 정보를 훔치는 특별한 기술을 가진 전문가입니다.",
            "영화의 마지막 장면에 등장하는 물체는 지금도 팬들 사이에서 뜨거운 토론 주제입니다.",
            "꿈속의 꿈속의 꿈... 더 깊이 들어갈수록 시간은 더욱 늘어납니다.",
            "타이타닉으로 유명한 배우가 주연을 맡았습니다."
        ],
        "기생충": [
            "2019년 아카데미 시상식에서 대한민국 영화 최초로 작품상을 수상한 영화입니다.",
            "반지하 가족의 이야기로 시작하여 계단과 높이의 상징성이 돋보이는 작품입니다.",
            "짜파구리가 외신에서도 화제가 되었던 이 영화는 빈부격차를 날카롭게 그려냅니다.",
            "동시대 대한민국의 사회적 계급을 예리하게 파헤친 블랙 코미디입니다.",
            "봉준호 감독의 작품으로, 송강호 배우가 아버지 역을 맡았습니다."
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
            fake_answers = ["쇼생크 탈출", "인터스텔라", "라라랜드", "아바타", "기생충"]
            fake_answer = random.choice([fa for fa in fake_answers if fa != st.session_state.current_movie])
            st.warning(f"흠... 혹시 '{fake_answer}' 아닐까요? 😉")

if __name__ == "__main__":
    main()
