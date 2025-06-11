# app.py
import streamlit as st
import google.generativeai as genai
import random
import os
from dotenv import load_dotenv

# 환경변수 로드 (로컬에서는 .env / Streamlit Cloud에서는 Secrets 사용 가능)
load_dotenv()
genai.configure(api_key=os.getenv("GENAI_API_KEY"))

# 모델 초기화
model = genai.GenerativeModel('gemini-pro')

# System prompt 설계
SYSTEM_PROMPT = """
너는 학습자의 비판적 사고 촉진을 돕는 Socratic Scaffolding 챗봇 'BoA'야.
목표는 학습자가 자신의 주장과 논리를 점검하고 개선하도록 돕는 거야.
대답은 항상 질문 형태로 이어져야 하고, 반론과 자기 점검 질문을 포함해.
정답을 직접 제시하지 말고 Socratic 방식으로 사고를 유도해.
"""

# genai API 호출 함수 → BoA용 변경
def call_genai(user_input):
    try:
        full_prompt = f"{SYSTEM_PROMPT}\n\n사용자 질문: {user_input}\n\nBoA의 응답:"
        
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"⚠️ 오류 발생: {e}"

# Streamlit 앱
st.title("🐍 BoA: Socratic Scaffolding 챗봇")

# Starter or 자유 질문
starter_options = [
    "AI가 진짜 예술을 창조할 수 있을까?",
    "AI는 인간보다 윤리적일 수 있을까?",
    "인간의 직관 vs AI의 계산, 어느 쪽을 믿을까?"
]
starter_choice = random.choice(starter_options)

st.subheader("Starter 질문 또는 자유 질문으로 시작하세요.")
user_question = st.text_input("질문 입력:", placeholder=starter_choice)

# 대화 시작
if st.button("대화 시작하기") and user_question:
    with st.spinner("BoA가 사고를 유도하는 중..."):
        response = call_genai(user_question)
    st.write("🗣️ **BoA:**")
    st.write(response)

    # 간단한 대화 로그 (세션 state 이용)
    if 'chat_log' not in st.session_state:
        st.session_state.chat_log = []
    st.session_state.chat_log.append({"user": user_question, "bot": response})

# 대화 로그 출력
if 'chat_log' in st.session_state:
    st.subheader("📝 대화 기록")
    for entry in st.session_state.chat_log:
        st.write(f"**너:** {entry['user']}")
        st.write(f"**BoA:** {entry['bot']}")
