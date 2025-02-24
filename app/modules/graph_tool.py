import json
import plotly.graph_objects as go
from langchain.tools import BaseTool
import streamlit as st


class StreamlitGraphTool(BaseTool):
    name: str = "create_graph"  # Adicionada a anotação de tipo para o atributo 'name'
    description: str = (
        "Cria um gráfico usando dados fornecidos. Input deve ser um JSON com formato: "
        "{'tipo': 'bar/line/pie', 'dados': {'labels': [], 'valores': []}, 'titulo': 'string'}"
    )

    def _run(self, input_str: str) -> str:
        try:
            dados = json.loads(input_str)
            fig = self._criar_grafico(dados)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
                return "Gráfico criado com sucesso"
            return "Não foi possível criar o gráfico"
        except Exception as e:
            return f"Erro ao criar gráfico: {str(e)}"

    def _criar_grafico(self, dados):
        # Paleta de cores personalizada
        colors = ["#DA8C92", "#9871A3", "#6A4A7D", "#B2A3B5"]

        tipo = dados.get("tipo")
        data = dados.get("dados", {})
        titulo = dados.get("titulo", "")

        if not data.get("labels") or not data.get("valores"):
            return None

        if tipo == "bar":
            fig = go.Figure(
                data=[go.Bar(x=data["labels"], y=data["valores"], marker_color=colors)]
            )
        elif tipo == "line":
            fig = go.Figure(
                data=[
                    go.Scatter(
                        x=data["labels"],
                        y=data["valores"],
                        mode="lines",  # Alterado para "lines" (sem marcadores)
                        line=dict(color=colors, width=2),  # Cor e espessura da linha
                    )
                ]
            )
        elif tipo == "pie":
            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=data["labels"],
                        values=data["valores"],
                        marker=dict(colors=colors),
                    )
                ]
            )
        else:
            return None

        fig.update_layout(title=titulo, template="plotly_white")
        return fig
