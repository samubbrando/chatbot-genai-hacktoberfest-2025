import streamlit as st
import google.genai as genai
from google.genai import types

# Coloque sua API_KEY
API_KEY = ""

# Criando "mensagens" no session_state

if "mensagens" not in st.session_state:
    st.session_state.mensagens = [
        # types.Content(
        #     role="user",
        #     parts=types.Part(text="Você é um chatbot que faz função específica x.")
        # )

        {"role": "user", "content": "Você é um chatbot que faz função específica x."}
    ]


def parse_history(history_content: list[dict]) -> list[types.Content]:
    result = []

    for cada_mensagem in history_content:
        result.append(
            types.Content(
                role=cada_mensagem["role"],
                parts=[types.Part(text=cada_mensagem["content"])]
            )
        )

    return result

# Resgatando histórico do session_state e colocando mensagens na conversa


for mensagem in st.session_state.mensagens:
    role = mensagem["role"]
    if role == "model":
        role = "assistant"

    with st.chat_message(role):
        st.markdown(mensagem["content"])


# Preparando para envio de mensagens

prompt = st.chat_input("Sua mensagem?")
if prompt:

    client = genai.Client(api_key=API_KEY)

    st.session_state.mensagens.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Carregando mensagem"):
        resposta = ""
        with st.chat_message("assistant"):
            for parte in client.models.generate_content_stream(model="gemini-2.5-flash", contents=parse_history(st.session_state.mensagens)):
                resposta += parte.text
                st.markdown(parte.text)
    

    st.session_state.mensagens.append({
        "role": "model",
        "content": resposta
    })

    client.close()
    st.rerun()
