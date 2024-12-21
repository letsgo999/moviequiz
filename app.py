import os
import openai
import streamlit as st

# 환경변수에서 API 키 가져오기
openai.api_key = os.getenv("OPENAI_API_KEY")

# 앱의 나머지 코드는 그대로 유지
st.title("🎬 영화 제목 맞추기 게임!")
st.write("제가 제공하는 힌트를 보고 영화 제목을 맞춰보세요! 최대 5개의 힌트를 제공합니다.")

# ChatGPT API 호출 함수 예제
def get_response_from_chatgpt(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # 적합한 GPT-3.5 엔진 사용
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"OpenAI API 호출 중 오류가 발생했습니다: {e}"
