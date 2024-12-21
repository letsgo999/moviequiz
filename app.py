import os
import openai
import streamlit as st

# 환경변수에서 OpenAI API 키 가져오기
openai.api_key = os.getenv("OPENAI_API_KEY")

# 힌트 데이터 및 상태 초기화
if "hints" not in st.session_state:
    st.session_state.hints = [
        "이 영화는 크리스토퍼 놀란 감독의 작품으로, 꿈과 현실을 넘나드는 스릴러입니다.",
        "주인공은 꿈속에서 아이디어를 훔치는 전문 도둑으로 활동합니다.",
        "레오나르도 디카프리오가 주연을 맡았으며, 2010년에 개봉되었습니다.",
        "이 영화는 '토템'이라는 물건을 통해 꿈과 현실을 구분합니다.",
        "영화의 마지막 장면은 팽이가 도는 것으로 끝나며, 관객들 사이에 논쟁을 불러일으켰습니다."
    ]
    st.session_state.current_hint_index = 0  # 현재 힌트 인덱스
    st.session_state.correct = False  # 정답 여부
    st.session_state.movie_title = "인셉션"  # 정답 영화 제목

# 제목 표시
st.title("🎬 영화 제목 맞추기 게임!")

# 현재 힌트를 표시
if st.session_state.current_hint_index < len(st.session_state.hints):
    st.write(f"**힌트:** {st.session_state.hints[st.session_state.current_hint_index]}")
else:
    st.error("더 이상 힌트가 없습니다! 정답을 맞혀주세요!")

# 사용자 입력창
user_input = st.text_input("정답을 입력해보세요!", key="user_input")

# [정답 확인] 버튼
if st.button("정답 확인"):
    # 사용자가 입력한 답과 정답 비교
    if user_input.strip().lower() == st.session_state.movie_title.lower():
        st.session_state.correct = True
        st.success("정답입니다! 정말 뛰어나시군요. 🎉 혹시 다른 영화로 게임을 계속할까요?")
    else:
        st.session_state.current_hint_index += 1  # 다음 힌트로 이동
        if st.session_state.current_hint_index < len(st.session_state.hints):
            st.warning("안타깝네요. 매우 근접하셨는데 아직 정답이 아닙니다! 다음 힌트를 들어보세요.")
        else:
            st.error(f"모든 힌트가 끝났습니다. 정답은 **'{st.session_state.movie_title}'**입니다! 다음에 다시 도전해보세요.")

# 정답을 맞췄다면 새로운 게임을 시작할지 여부를 묻기
if st.session_state.correct:
    if st.button("새 게임 시작하기"):
        # 게임 상태 초기화
        st.session_state.current_hint_index = 0
        st.session_state.correct = False
        st.session_state.user_input = ""
        st.experimental_rerun()
