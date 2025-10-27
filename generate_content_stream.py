import google.genai as genai

# Coloque sua API_KEY
API_KEY = ""
client = genai.Client(api_key=API_KEY)

# for pedaco in client.models.generate_content_stream(contents=["Me explique sobre o que é você?"], model="gemini-2.5-flash"):
#     print(pedaco.text, sep="")

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

    resposta_modelo = ""
    for pedaco in client.models.generate_content_stream(contents=historico, model="gemini-2.5-flash"):
        resposta_modelo += pedaco.text
        print(pedaco.text, sep="")
    
    historico.append(
        genai.types.Content(
            role="model",
            parts=[genai.types.Part.from_text(text=resposta_modelo)]
        ))