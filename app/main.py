import json
import streamlit as st
from dotenv import load_dotenv
from modules.database import initialize_db
from modules.agent import initialize_agent, ai_response
from modules.graph_tool import StreamlitGraphTool
from modules.utils import load_images
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a senha do arquivo .env
ACCESS_PASSWORD = os.getenv("ACCESS_PASSWORD")

if not ACCESS_PASSWORD:
    raise ValueError("A senha de acesso não foi encontrada no arquivo .env.")

# Configurações iniciais
st.set_page_config(page_title="SophIA", page_icon="app/icons/icon.png")
st.image("app/icons/logo_L.png", width=200)

# Carrega ícones
icon1, icon2 = load_images("app/icons/icon.png", "app/icons/icon_user.jpg")

# Inicializa o banco de dados
db = initialize_db("sqlite:///data/escola_banco.db")

# Inicializa o agente e a memória
agent_executor, prompt_template = initialize_agent(db)

# Histórico de mensagens
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Contador de perguntas
if "question_count" not in st.session_state:
    st.session_state["question_count"] = 0

# Limite de perguntas
if "question_limit" not in st.session_state:
    st.session_state["question_limit"] = 1

# Variável de autenticação
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False


# Função para processar respostas que contêm gráficos
def processar_resposta_com_grafico(resposta):
    if "dados_grafico" in resposta:
        try:
            dados_json_inicio = resposta.find("dados_grafico:{")
            dados_json_fim = resposta.rfind("}") + 1

            if dados_json_inicio != -1 and dados_json_fim != 0:
                dados_json = resposta[
                    dados_json_inicio + len("dados_grafico:") : dados_json_fim
                ]
                dados = json.loads(dados_json)
                tipo = dados.get("tipo")
                data = dados.get("dados", {})
                titulo = dados.get("titulo", "")
                fig = StreamlitGraphTool()._criar_grafico(tipo, data, titulo)
                return resposta, fig
        except json.JSONDecodeError:
            st.error(
                "Erro ao decodificar os dados do gráfico. Certifique-se de que o formato JSON está correto."
            )
    return resposta, None


# Função para exibir o histórico de mensagens
def exibir_historico():
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.chat_message("user", avatar=icon2).write(message["content"])
        elif message["role"] == "ai":
            st.chat_message("ai", avatar=icon1).write(message["content"])
            if "graph" in message:
                st.plotly_chart(message["graph"], use_container_width=True)


# Exibe o histórico de mensagens
exibir_historico()

# Verifica autenticação
if (
    not st.session_state["authenticated"]
    and st.session_state["question_count"] >= st.session_state["question_limit"]
):
    st.warning("Você atingiu o limite de perguntas. Digite a senha para continuar.")
    st.info(
        "O projeto está em desenvolvimento. Para mais testes, entre em contato com:\n\n"
        "**Rodolfo Batista**: rodolfo@batista.com | Tel: 65498798\n\n"
        "**Mario Alencar**: mario@mario.com | Tel: 6549988"
    )
    password = st.text_input("Senha:", type="password")
    if password:
        if password == ACCESS_PASSWORD:
            st.success("Senha correta! O limite foi aumentado.")
            st.session_state["question_limit"] = 10  # Aumenta o limite
            st.session_state["question_count"] = 0  # Reinicia o contador
            st.session_state["authenticated"] = (
                True  # Define autenticação como verdadeira
            )
        else:
            st.error("Senha incorreta. Tente novamente.")
            st.stop()

# Entrada do usuário
pergunta = st.chat_input(
    "Como posso ajudar hoje?",
    key="chat_input_unique_key",
    max_chars=200,
)

if pergunta:
    # Verifica se o usuário está autenticado ou dentro do limite
    if (
        not st.session_state["authenticated"]
        and st.session_state["question_count"] >= st.session_state["question_limit"]
    ):
        st.warning("Você atingiu o limite de perguntas. Digite a senha para continuar.")
        st.stop()

    # Adiciona a pergunta ao histórico
    st.chat_message("user", avatar=icon2).write(pergunta)
    st.session_state.messages.append({"role": "user", "content": pergunta})
    st.session_state["question_count"] += 1

    with st.spinner("Deixa eu procurar aqui..."):
        resposta = agent_executor.invoke(
            {
                "input": prompt_template.format(
                    q=pergunta, chat_history=st.session_state.messages
                )
            }
        )
        resposta_texto, grafico = processar_resposta_com_grafico(
            resposta.get("output", "")
        )

        if grafico:
            st.session_state.messages.append(
                {"role": "ai", "content": resposta_texto, "graph": grafico}
            )
            st.chat_message("ai", avatar=icon1).write(resposta_texto)
            st.plotly_chart(grafico, use_container_width=True)
        elif resposta_texto:
            st.session_state.messages.append({"role": "ai", "content": resposta_texto})
            st.chat_message("ai", avatar=icon1).write(resposta_texto)
        else:
            st.error("Ocorreu um erro ao processar sua pergunta.")
