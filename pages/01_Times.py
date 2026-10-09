import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Análise por Times",
    page_icon="⚽",
    layout="wide"
)

st.markdown("""
    <style>
        .stApp {
            background-color: #0e1117;
            color: #ffffff;
        }

        div[data-testid="stMetric"] {
            background-color: #151922;
            border: 1px solid #343a46;
            padding: 18px;
            border-radius: 10px;
        }

        div[data-testid="stMetricLabel"] {
            color: #b8c2d1;
        }
    </style>
""", unsafe_allow_html=True)

st.title("⚽ Análise por Time")
st.caption("Brasileirão Série A | 2008–2017")

# Carregar a base
@st.cache_data
def carregar_dados():
    return pd.read_csv("Tabela_Clubes.csv")

df = carregar_dados()

# Limpar nomes das colunas e dos clubes
df.columns = df.columns.str.strip()
df["Clubes"] = df["Clubes"].astype(str).str.strip()

# Filtro de clube
clubes = sorted(df["Clubes"].dropna().unique())

clube_selecionado = st.selectbox(
    "Selecione um clube",
    clubes
)

# Filtrar os dados
df_clube = (
    df[df["Clubes"] == clube_selecionado]
    .sort_values("Ano")
    .copy()
)

st.subheader(f"Histórico do {clube_selecionado}")

st.write(
    f"Em quantas temporadas o time apareceu: {df_clube['Ano'].nunique()}"
)

colunas = [
    "Ano", "Pos.", "Vitorias", "Derrotas",
    "Empates", "Saldo", "Qtd_Jogadores",
    "Estrangeiros", "Valor_total", "Media_Valor"
]

for coluna in colunas:
    df_clube[coluna] = pd.to_numeric(
        df_clube[coluna], errors="coerce"
    )

# Calcular os indicadores
melhor_posicao = (
    int(df_clube["Pos."].min())
    if df_clube["Pos."].notna().any()
    else None
)

total_vitorias = int(df_clube["Vitorias"].sum())

saldo_total = int(df_clube["Saldo"].sum())

valor_medio = df_clube["Media_Valor"].mean()

# Exibir os cartões
c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Melhor posição",
    f"{melhor_posicao}º" if melhor_posicao else "—"
)

c2.metric(
    "Total de vitórias",
    f"{total_vitorias:,}".replace(",", ".")
)

c3.metric(
    "Saldo de gols",
    f"{saldo_total:+}"
)

c4.metric(
    "Valor médio",
    (
        f"R$ {valor_medio:,.0f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )
    if pd.notna(valor_medio)
    else "—"
)

st.divider()

fig_posicao = px.line(
    df_clube,
    x="Ano",
    y="Pos.",
    markers=True,
    title=f"Evolução da posição — {clube_selecionado}",
    labels={
        "Ano": "Temporada",
        "Pos.": "Posição final"
    },
    template="plotly_dark"
)

fig_posicao.update_yaxes(
    autorange="reversed",
    dtick=1
)

fig_posicao.update_traces(
    line=dict(color="#79FFAC", width=3),
    marker=dict(size=8)
)

fig_posicao.update_layout(
    paper_bgcolor="#0e1117",
    plot_bgcolor="#0e1117",
    font_color="white",
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(
    fig_posicao,
    use_container_width=True
)

col_esq, col_dir = st.columns(2)

# Gráfico de vitórias, empates e derrotas
df_resultados = df_clube.melt(
    id_vars=["Ano"],
    value_vars=["Vitorias", "Empates", "Derrotas"],
    var_name="Resultado",
    value_name="Quantidade"
)

fig_resultados = px.bar(
    df_resultados,
    x="Ano",
    y="Quantidade",
    color="Resultado",
    barmode="group",
    title="Vitórias, empates e derrotas",
    template="plotly_dark",
    color_discrete_map={
        "Vitorias": "#DEE66D",
        "Empates": "#A355EB",
        "Derrotas": "#66E3F3"
    }
)

fig_resultados.update_layout(
    paper_bgcolor="#0e1117",
    plot_bgcolor="#0e1117",
    font_color="white"
)

col_esq.plotly_chart(
    fig_resultados,
    use_container_width=True
)

# Gráfico de valor total do elenco
fig_valor = px.line(
    df_clube,
    x="Ano",
    y="Valor_total",
    markers=True,
    title="Evolução do valor do elenco",
    template="plotly_dark"
)

fig_valor.update_traces(
    line=dict(color="#B665D6", width=3),
    marker=dict(size=7)
)

fig_valor.update_layout(
    paper_bgcolor="#0e1117",
    plot_bgcolor="#0e1117",
    font_color="white",
    yaxis_tickprefix="R$ ",
    yaxis_tickformat=",.0f"
)

col_dir.plotly_chart(
    fig_valor,
    use_container_width=True
)