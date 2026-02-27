import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

if 'history' not in st.session_state:
    st.session_state.history = []
if 'last_action' not in st.session_state:
    st.session_state.last_action = None
if 'api_responses' not in st.session_state:
    st.session_state.api_responses = []


def check_api():
    try:
        requests.get(f"{API_URL}/health", timeout=2)
        return True
    except:
        return False


def call_api(action):
    if not st.session_state.get('user_input'):
        st.warning("Введите текст")
        return

    if not check_api():
        st.error("API не запущен. Запустите: python api.py")
        return

    st.session_state.last_action = action

    try:
        response = requests.post(
            f"{API_URL}/process",
            json={"text": st.session_state.user_input, "action": action},
            timeout=5
        )

        if response.status_code == 200:
            data = response.json()
            st.session_state.result = data['response']
            st.session_state.history.append({
                "text": st.session_state.user_input,
                "action": action,
                "response": data['response']
            })
            st.rerun()
    except Exception as e:
        st.error(f"Ошибка: {e}")


with st.sidebar:
    api_status = "🟢" if check_api() else "🔴"
    st.write(f"API: {api_status}")

    st.button("Диагностика", on_click=call_api, args=("diagnostic",))
    st.button("Рекомендации", on_click=call_api, args=("recommend",))
    st.button("Объяснить", on_click=call_api, args=("explain",))
    st.button("Вопрос", on_click=call_api, args=("question",))

    if st.button("Сброс"):
        st.session_state.clear()
        st.rerun()

    if st.session_state.history:
        st.write("---")
        st.write("История:")
        for item in st.session_state.history[-3:]:
            st.caption(f"{item['action']}: {item['text'][:20]}...")


st.title("Project")


user_input = st.text_input("Введите текст:", key="user_input")

if 'result' in st.session_state and st.session_state.result:
    st.write("---")
    st.write("Запрос", st.session_state.user_input)
    st.write("Ответ", st.session_state.result)
