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
        [data-testid="stAppViewContainer"] { max-width: 850px; margin: auto; }
        body { background-color: #0F172A; color: #F8FAFC; font-family: 'Verdana', sans-serif; }
        .chat-container { padding: 15px; border-radius: 10px; background-color: #1E293B; width: 100%; margin: auto; }
        .chat-bubble { padding: 12px; border-radius: 14px; margin: 8px 0; max-width: 90%; word-wrap: break-word; }
        .chat-user { background-color: #2563EB; color: white; align-self: flex-end; }
        .chat-bot { background-color: #374151; color: #F8FAFC; align-self: flex-start; }
        .chat-wrapper { display: flex; flex-direction: column; align-items: flex-end; }
        .chat-wrapper-bot { display: flex; flex-direction: column; align-items: flex-start; }
        .stTextInput input { background-color: #1E293B; color: white; border-radius: 10px; padding: 10px; font-size: 16px; border: 1px solid #475569; }
        .stTextInput input::placeholder { color: #94A3B8; }
        .send-button { background-color: #2563EB; color: white; border: none; border-radius: 50%; width: 40px; height: 40px; cursor: pointer; transition: 0.3s; font-size: 18px; }
        .send-button:hover { background-color: #1D4ED8; }
        .new-chat-container { display: flex; justify-content: center; margin-top: 10px; }
        .new-chat-button { background-color: #DC2626; color: white; padding: 8px 16px; border: none; border-radius: 8px; cursor: pointer; font-size: 14px; transition: 0.3s; }
        .new-chat-button:hover { background-color: #B91C1C; }
    </style>
    """,
    unsafe_allow_html=True
)

# Inicializar historial de conversación en session_state
st.session_state.setdefault("chat_history", [])

def chat_with_gemini(prompt):
    model = genai.GenerativeModel("gemini-pro")
    return model.generate_content(prompt).text

st.markdown("<h1 style='text-align: center; color: #2563EB;'>Bienvenido al bot de gemini!</h1>", unsafe_allow_html=True)

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
    user_input = st.text_input("", placeholder="Escribe aquí...", key="user_input", label_visibility="collapsed")
    submit_button = st.form_submit_button("➤")

if submit_button and user_input.strip():
    st.session_state.chat_history.append({"role": "user", "message": user_input})
    st.session_state.chat_history.append({"role": "assistant", "message": chat_with_gemini(user_input)})
    st.rerun()

# Botón para nueva conversación
st.markdown('<div class="new-chat-container">', unsafe_allow_html=True)
if st.button("Nuevo Chat", key="new_chat", help="Iniciar una nueva conversación"):
    st.session_state.chat_history.clear()
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
