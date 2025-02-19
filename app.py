import streamlit as st
import google.generativeai as genai
import os

# Configurar API KEY
os.environ["GOOGLE_API_KEY"] = "AIzaSyBOyo1uv7HU_J8xN05PYxanAr8puP8VtW0"
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Aplicar estilos personalizados
st.markdown(
    """
    <style>
        [data-testid="stAppViewContainer"] { max-width: 800px; margin: auto; }
        body { background-color: #121212; color: #E0E0E0; font-family: 'Arial', sans-serif; }
        .chat-container { padding: 15px; border-radius: 12px; background-color: #1E1E1E; width: 100%; margin: auto; }
        .chat-bubble { padding: 12px; border-radius: 18px; margin: 8px 0; max-width: 85%; word-wrap: break-word; }
        .chat-user { background-color: #0057D9; color: white; align-self: flex-end; }
        .chat-bot { background-color: #333; color: #E0E0E0; align-self: flex-start; }
        .chat-wrapper { display: flex; flex-direction: column; align-items: flex-end; }
        .chat-wrapper-bot { display: flex; flex-direction: column; align-items: flex-start; }
        .stTextInput input { background-color: #333; color: white; border-radius: 20px; padding: 10px; font-size: 16px; border: 1px solid #555; }
        .stTextInput input::placeholder { color: #bbb; }
        .send-button { background-color: #0057D9; color: white; border: none; border-radius: 50%; width: 42px; height: 42px; cursor: pointer; transition: 0.3s; font-size: 18px; }
        .send-button:hover { background-color: #003E9B; }
        .new-chat-container { display: flex; justify-content: center; margin-top: 10px; }
        .new-chat-button { background-color: #FF4081; color: white; padding: 8px 15px; border: none; border-radius: 20px; cursor: pointer; font-size: 14px; transition: 0.3s; }
        .new-chat-button:hover { background-color: #E91E63; }
    </style>
    """,
    unsafe_allow_html=True
)

# Inicializar historial de conversación en session_state
st.session_state.setdefault("chat_history", [])

def chat_with_gemini(prompt):
    model = genai.GenerativeModel("gemini-pro")
    return model.generate_content(prompt).text

st.markdown("<h1 style='text-align: center; color: #FF4081;'>¿En qué puedo ayudarte?</h1>", unsafe_allow_html=True)

# Mostrar historial de conversación
with st.container():
    for chat in st.session_state.chat_history:
        role_class = "chat-user" if chat["role"] == "user" else "chat-bot"
        align_class = "chat-wrapper" if chat["role"] == "user" else "chat-wrapper-bot"
        st.markdown(
            f'<div class="{align_class}"><div class="chat-bubble {role_class}">{chat["message"]}</div></div>',
            unsafe_allow_html=True
        )

# Entrada de usuario
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("", placeholder="Escribe tu mensaje...", key="user_input", label_visibility="collapsed")
    submit_button = st.form_submit_button("➤")

if submit_button and user_input.strip():
    st.session_state.chat_history.append({"role": "user", "message": user_input})
    st.session_state.chat_history.append({"role": "assistant", "message": chat_with_gemini(user_input)})
    st.rerun()

# Botón para nueva conversación
st.markdown('<div class="new-chat-container">', unsafe_allow_html=True)
if st.button("Nueva Conversación", key="new_chat", help="Iniciar un nuevo chat"):
    st.session_state.chat_history.clear()
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
