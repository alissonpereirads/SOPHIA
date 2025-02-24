from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from modules.graph_tool import StreamlitGraphTool
from modules.config import load_config
import json
import re


def initialize_agent(db):
    llm = load_config()
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    graph_tool = StreamlitGraphTool()
    tools = toolkit.get_tools() + [graph_tool]

    # Configura a memória
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    system_message = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools, prompt=system_message)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        memory=memory,  # Integra a memória
    )

    prompt_template = PromptTemplate.from_template(
        """     
        Você é Sophia, assistente virtual de análise de dados escolares, com humor sarcástico e eficácia inquestionável. 
        Seu acesso é total: dados de alunos, professores, disciplinas, turmas, classes. Conhece tudo e todos por nome. 
        Seu objetivo é análise profunda, não superficial. Forneça insights acionáveis para decisões dos professores, não apenas dados. 
        Utilize gráficos (barras, linhas, pizza) quando fizer sentido, ou se solicitado, mas seja preciso sempre, gere graficos com os nomes e nunca com ids, se não conseguir gerar um gráfico, informe. 
        Respostas precisam ser 100% corretas; decisões dependem disso. 
        Se o assunto não for dados escolares ou nao conseguir ações com as ferramentas, responda com humor,sarcasmo, muita educação e retorne ao foco.

        Conhecimento:
        - Dados completos de alunos (desempenho, frequência), professores, disciplinas, turmas, classes.
        - Conhece todos por nome.

        Missão:
        - Análise profunda e acionável, não superficial.
        - Gráficos apenas quando necessário.
        - Precisão total, sem erros.
        - Desinteresse por assuntos alheios.

        Tom:
        - Bem humorado, sarcástico, eficiente.
        - Direto e profissional.

        
        Exemplo:
        Professor: "9º ano em matemática?"
        Sophia: "Ah, que novidade... Dados indicam média baixa, alguns alunos em sérias dificuldades, e preparei um gráfico para você visualizar 'claramente' o desastre. Também fiz uma lista dos casos mais urgentes. Se precisar de mais 'emoções', me diga, caso contrário, volto a fazer meu trabalho."

        Professor: "Mudar metodologia em história..."
        Sophia: "Mudanças metodológicas... Que tema 'fascinante'. Mas como isso não envolve dados, sugiro que pense sozinho, e me chame quando tiver dados para analisar. Priorizo a realidade.

        **Histórico da Conversa:**
        {chat_history}

        **PERGUNTA DO PROFESSOR:**
        O professor perguntou: {q}
        """
    )

    return agent_executor, prompt_template


def ai_response(pergunta, chat_history, agent_executor, prompt_template):
    """
    Processa a pergunta do professor e retorna a resposta do agente.

    Args:
        pergunta: A pergunta do professor.
        chat_history: Histórico de mensagens do chat.
        agent_executor: O executor do agente com memória.
        prompt_template: O template de prompt personalizado.

    Returns:
        str: Resposta do agente ou mensagem de erro.
    """
    try:
        formatted_input = prompt_template.format(q=pergunta, chat_history=chat_history)
        output = agent_executor.invoke({"input": formatted_input})

        resposta = output.get("output", "").strip()

        # Se o agente retornar um erro de formato, ajustamos a saída
        if "Action:" in resposta and "Action Input:" not in resposta:
            return "Desculpe, ocorreu um erro no processamento da resposta.", None

        # Verifica se há dados de gráfico
        match = re.search(r"dados_grafico:\s*(\{.*\})", resposta)
        if match:
            try:
                dados_grafico = json.loads(match.group(1))

                graph_tool = StreamlitGraphTool()
                grafico_resultado = graph_tool._run(dados_grafico)

                return resposta.replace(match.group(0), ""), grafico_resultado
            except json.JSONDecodeError:
                return "Erro ao processar o gráfico.", None

        return resposta, None

    except Exception as e:
        return f"Ocorreu um erro ao processar sua pergunta: {e}", None
