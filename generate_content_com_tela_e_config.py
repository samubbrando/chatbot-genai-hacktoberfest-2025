import streamlit as st
import google.genai as genai
from google.genai import types
from datetime import datetime
from time import time

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

def get_current_timestamp() -> float:
    """
    Função que calcular e retorna um timestamp correspondente ao momento atual.
    """
    return time()

def get_current_datetime() -> str:
    """
    Função que define e retorna a data de hoje em formato isoformat.
    """
    return datetime.now().isoformat()


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
        resposta = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=parse_history(st.session_state.mensagens),
            config=types.GenerateContentConfig(
                # Instrução do sistema, semelhante a um "prompt inicial"
                system_instruction="Você pode chamar as funções 'get_current_datetime' para obter o dia de hoje e 'get_current_timestamp', caso seja perguntada, se utilizar quaisquer dessas funções, notifique ao usuário que fez uso",
                
                # Habilitando o function_calling com data, como o exemplo dado durante o workshop
                tools=[ 
                    get_current_datetime,
                    get_current_timestamp
                ],

                temperature=1, # É um valor entre 0 e 2, quanto menor, menos "aleatório" a escolha das palavras, mais consistente
                top_k=0.9, # Faz a sample através dos k% tokens mais prováveis de cada iteração
                top_p=0.9  # Probabilidade cumulativa de cortar mais dados no sampling das próximas mensagens (menor valor, menos valores diferentes possíveis de ser escolhido a cada iteração)
                
            ),
        )

    st.session_state.mensagens.append({
        "role": "model",
        "content": resposta.text
    })

    client.close()
    st.rerun()
