import streamlit as st
import plotly.express as px
import pandas as pd
st.set_page_config(layout='wide')

st.markdown("""
    <style>
        .stApp {
            background-color: #0e1117;
            color: #f5f5f5;
        }

        div[data-testid="stMetric"] {
            background-color: #151922;
            border: 1px solid #343a46;
            border-radius: 10px;
        }

        section[data-testid="stSidebar"] {
            background-color: #11151d;
        }
    </style>
""", unsafe_allow_html=True)

df = pd.read_csv('Tabela_Clubes.csv')
df['Gols_Feitos'] = df['GolsF/S'].apply(lambda x: int(x.split(':')[0]))
df['Gols_Sofridos']= df['GolsF/S'].apply(lambda x: int(x.split(':')[1]))
#=============================== SIDEBAR
lista_anos = df['Ano'].unique().tolist()
filtro_anos = st.sidebar.multiselect('Ano', lista_anos, default=lista_anos)

#=============================== BODY
df = df[df['Ano'].apply(lambda x: x in filtro_anos)]

with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.metric('Quantidade de Estrangeiros', df['Estrangeiros'].sum())
            
    with col2:
        with st.container(border=True):
            idade_media = df['Idade_Media'].apply(lambda x: float(x.replace(',', '.'))).mean()
            st.metric('Idade média dos jogadores', f'{idade_media:.0f}')
            
    with col3:
        with st.container(border=True):
            valor_medio= df['Valor_total'].mean()
            st.metric('Valor médio dos times', f'R$ {df['Valor_total'].mean():,.0f}')

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        with st.container(width='stretch'):
            podio = df[df['Pos.'] <= 5][
                ['Ano', 'Pos.', 'Clubes']
            ].sort_values(['Ano', 'Pos.'])

            st.table(podio)

    with col2:
        with st.container(width='stretch'):
            g1 = px.bar(
                df,
                x='Clubes',
                y='Gols_Feitos',
                title='Total de gols feitos',
                template='plotly_dark',
                color_discrete_sequence=["#79D9F7"]
            )

            g1.update_layout(
                paper_bgcolor='#0e1117',
                plot_bgcolor='#0e1117',
                font_color='#f5f5f5'
            )

            st.plotly_chart(g1, use_container_width=True)

            g2 = px.line(
                df,
                x='Ano',
                y='Valor_total',
                color='Clubes',
                markers=True,
                title='Valor total dos times através dos anos',
                template='plotly_dark',
                color_discrete_sequence=px.colors.qualitative.Bold
            )

            g2.update_layout(
                paper_bgcolor='#0e1117',
                plot_bgcolor='#0e1117',
                font_color='#f5f5f5'
            )

            st.plotly_chart(g2, use_container_width=True)

