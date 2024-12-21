import os
import openai
import streamlit as st

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

# 초기 상태 관리
if "hints" not in st.session_state:
    st.session_state.hints = [
        "이 영화는 크리스토퍼 놀란 감독의 작품으로, 꿈과 현실을 넘나드는 스릴러입니다.",
        "주인공은 꿈속에서 아이디어를 훔치는 전문 도둑으로 활동합니다.",
        "레오나르도 디카프리오가 주연을 맡았으며, 2010년에 개봉되었습니다.",
        "이 영화는 '토템'이라는 물건을 통해 꿈과 현실을 구분합니다.",
        "영화의 마지막 장면은 팽이가 도는 것으로 끝나며, 관객들 사이에 논쟁을 불러일으켰습니다."
    ]
    st.session_state.current_hint_index = 0  # 현재 힌트 번호
    st.session_state.correct = False  # 정답 여부
    st.session_state.movie_title = "인셉션"  # 정답 영화 제목
    st.session_state.user_input = ""  # 사용자의 입력 값
    st.session_state.game_over = False  # 게임 종료 여부

# 함수: 정답 확인
def check_answer(user_answer):
    if user_answer.strip().lower() == st.session_state.movie_title.lower():
        st.session_state.correct = True
        return True
    return False

# 함수: 새 게임 초기화
def reset_game():
    st.session_state.hints = [
        "이 영화는 크리스토퍼 놀란 감독의 작품으로, 꿈과 현실을 넘나드는 스릴러입니다.",
        "주인공은 꿈속에서 아이디어를 훔치는 전문 도둑으로 활동합니다.",
        "레오나르도 디카프리오가 주연을 맡았으며, 2010년에 개봉되었습니다.",
        "이 영화는 '토템'이라는 물건을 통해 꿈과 현실을 구분합니다.",
        "영화의 마지막 장면은 팽이가 도는 것으로 끝나며, 관객들 사이에 논쟁을 불러일으켰습니다."
    ]
    st.session_state.current_hint_index = 0
    st.session_state.correct = False
    st.session_state.user_input = ""
    st.session_state.game_over = False

# 앱 제목
st.title("🎬 영화 제목 맞추기 게임!")

# 게임 종료 여부 확인
if st.session_state.game_over:
    st.error(f"모든 힌트가 끝났습니다. 정답은 **'{st.session_state.movie_title}'**입니다.")
    if st.button("새 게임 시작"):
        reset_game()

# 현재 힌트 출력
elif not st.session_state.correct:
    st.write(f"**힌트 #{st.session_state.current_hint_index + 1}:** {st.session_state.hints[st.session_state.current_hint_index]}")

    # 사용자 입력창
    st.session_state.user_input = st.text_input("영화 제목을 입력하세요:", value=st.session_state.user_input)

    # 정답 확인 버튼
    if st.button("정답 확인"):
        if check_answer(st.session_state.user_input):
            st.success("정답입니다! 정말 뛰어나시군요. 🎉")
            st.write("게임을 다시 시작하려면 아래 버튼을 눌러주세요.")
            if st.button("새 게임 시작"):
                reset_game()
        else:
            st.error("안타깝네요. 매우 근접하셨는데 아직 정답이 아닙니다.")
            if st.session_state.current_hint_index + 1 < len(st.session_state.hints):
                st.session_state.current_hint_index += 1  # 다음 힌트로 넘어감
            else:
                st.session_state.game_over = True  # 모든 힌트 소진
else:
    # 정답을 맞췄을 경우
    if st.button("새 게임 시작"):
        reset_game()
