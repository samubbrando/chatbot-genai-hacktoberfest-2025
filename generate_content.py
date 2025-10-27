import google.genai as genai

# Coloque sua API_KEY
API_KEY = ""
client = genai.Client(api_key=API_KEY)

# print(client.models.generate_content(contents=["Me explique sobre o que é você?"], model="gemini-2.5-flash"))

# Criando um chat com generate_content
historico = []

mensagem = "a"
while mensagem != "":
    mensagem = input("> ")
    historico.append(
        genai.types.Content(
            role="user",
            parts=[genai.types.Part.from_text(text=mensagem)]
        ))

    resposta_modelo = client.models.generate_content(
        contents=historico, model="gemini-2.5-flash")
    print(resposta_modelo.text)

    historico.append(
        genai.types.Content(
            role="model",
            parts=[genai.types.Part.from_text(text=resposta_modelo.text)]
        ))