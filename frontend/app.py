import streamlit as st
import plotly.graph_objects as go
import plotly.express as px


st.set_page_config(
    page_title="AeroDecisionAI",
    page_icon=" ",
    layout= "wide",
    initial_sidebar_state="expanded"
    )
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .kpi-card {
        background-color: #F8F9FA;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        text-align: left;
    }
    .kpi-label {
        font-size: 0.8rem;
        color: #6B7280;
        margin-bottom: 0.3rem;
        font-weight: 500;
    }
    .kpi-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #111827;
    }

    .badge {
        display: inline-block;
        padding: 0.2rem 0.7rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .badge-success { background-color: #D1FAE5; color: #065F46; }
    .badge-warning { background-color: #FEF3C7; color: #92400E; }

    div.stButton > button:first-child {
        background-color: #0F4C81;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
    }
    div.stButton > button:first-child:hover {
        background-color: #0B3A63;
        color: white;
    }

    section[data-testid="stSidebar"] {
        background-color: #0F172A;
    }
    section[data-testid="stSidebar"] * {
        color: #E2E8F0 !important;
    }
</style>
"""
st.markdown(CUSTOM_CSS,unsafe_allow_html=True)

with st.sidebar():
    st.title("AeroDecisionAI")
    st.markdown('<span class= "badge badge-sucess">MVP</span>',
                '<span class= "badge badge-warning>AI</span>',
                '<span class= "badge badge-warning>Telerimetria</span>'
                )
    st.divider()
    page = st.radio("Navigation",
            ["Nova página", "Dashboard", "Frota"]
            )
    st.divider()
    st.caption("Desenvolvido por Lennon Vinicius de Moraes")
    st.link_button(url="https://github.com/LennonVinicius")
    st.link_button(url="https://www.linkedin.com/in/lennon-vinicius-de-moraes-soares-0544a0276/")

if page == "Nova página":
    st.title("Nova missãp")
    st.markdown("Preencha os campos a abaixo e receba a aeronave recomendada pela IA")

    tab_form, tab_text = st.tabs(["Formulário", "Descreva em texto livre"])

    with tab_form:
        col1, col2, col3 = st.columns(3)
        with col1:
            origem = st.selectbox("Origem", ["COLOCAR A LISTA DE AEROPORTOS"])
        with col2:
            destino = st.selectbox("Destino", ["COLOCAR A LISTA DE AEROPORTOS"])
        with col3:
            passageiros = st.number_input("Passageiros", min_value=1, max_value=99, value=1)

        col4, col5 = st.tabs(2)

        with col4:
            tipo = st.selectbox("Tipo de missão", ["Executiva", "Carga", "Regional"])
        with col5:
            peso = st.number_input("Volume da Carga", min_value=0, max_value=100000000)

        buscar = st.button("Gerar recomendação")

        st.divider()

        st.subheader("Resultados da análise")

        kpi1, kpi2, kpi3, kpi4 = st.columns(4)

        kpis = [
            ("Distância", "AQUI É O CALCULO DA DISTANCIA", kpi1),
            ("Tempo de voo", "CALCULAR TEMPO DE VOO", kpi2),
            ("Custo estimado", "CALCULAR O CUSTO ESTIMADO", kpi3),
            ("Score da Aeronave escolhida", "COLOCAR O SCORE FINAL", kpi4)
        ]
        col_map, col_ai = st.columns(2)

        with col_map:
            st.markdown("**Rota**")
            with st.container(border=True):
                st.info("AQUI TEM QUE TER O MAPA")
        with col_ai:
            st.markdown("**Resultado da IA**")
            with st.container(border=True):
                st.success("✅AQUI TEM QUE TER O NOME DA AERONAVE")
                st.info("AQUI TEM QUE TER A MENSAGEM GERADA PELA IA")

        st.markdown("**Ranking de aeronaves compatíveis**")
        df_rank = """RECEBE O RANKING"""

        fig = go.Figure(go.Bar(
            x=df_rank["AQUI VAI O FINAL SCORE"],
            y=df_rank["NOMES DAS AERONAVES"],
            orientation="h",
            marker_color=["#0F4C81" if s == df_rank["final_score"].max() else "#CBD5E1" for s in df_rank["final_score"]],
            text=df_rank["final_score"],
            textposition="outside",
        ))
        fig.update_layout(
            height=260,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(range=[0, 100], showgrid=True, gridcolor="#F1F5F9"),
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(family="Inter, sans-serif", size=13),
        )
        st.plotly_chart(fig, use_container_width=True)
