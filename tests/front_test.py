"""
Dumont Network — Demo visual de Streamlit
==========================================
Isso é um exemplo de referência, com dado FICTÍCIO (não conecta na sua API/banco ainda).
Rode com: streamlit run dumont_streamlit_demo.py
Instale antes: pip install streamlit plotly pandas --break-system-packages

Objetivo: mostrar técnicas de Streamlit que deixam a interface mais profissional,
com comentários explicando o "porquê" de cada escolha — pra você adaptar no
frontend/streamlit_app.py real, conectado na sua API.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ─────────────────────────────────────────────────────────────
# 1. CONFIGURAÇÃO DA PÁGINA — sempre a primeira chamada do script
# ─────────────────────────────────────────────────────────────
# layout="wide" usa a largura inteira da tela, em vez da coluna estreita
# centralizada que é o padrão do Streamlit — essencial pra dashboard.
st.set_page_config(
    page_title="Dumont Network",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# 2. CSS CUSTOMIZADO — o que mais diferencia "Streamlit padrão" de "produto polido"
# ─────────────────────────────────────────────────────────────
# Streamlit permite injetar CSS via st.markdown com unsafe_allow_html=True.
# Isso não é "gambiarra" — é o jeito oficial documentado de customizar visual
# além do que os temas nativos (config.toml) permitem.
CUSTOM_CSS = """
<style>
    /* Importa uma fonte mais moderna que a padrão do sistema */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Remove o padding excessivo padrão do Streamlit no topo */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Cards de KPI customizados (usados via st.markdown, não st.metric puro) */
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

    /* Badge de status, tipo "MVP" ou "Compatível" */
    .badge {
        display: inline-block;
        padding: 0.2rem 0.7rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .badge-success { background-color: #D1FAE5; color: #065F46; }
    .badge-warning { background-color: #FEF3C7; color: #92400E; }

    /* Deixa os botões primários com cor de marca, não o vermelho padrão do Streamlit */
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

    /* Sidebar com fundo levemente diferente do conteúdo principal, pra separar visualmente */
    section[data-testid="stSidebar"] {
        background-color: #0F172A;
    }
    section[data-testid="stSidebar"] * {
        color: #E2E8F0 !important;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# 3. DADOS FICTÍCIOS — troque isso pelas suas chamadas de API depois
# ─────────────────────────────────────────────────────────────
AIRCRAFTS = pd.DataFrame([
    {"name": "Embraer Phenom 300", "type": "Jato executivo", "range_km": 3650, "max_passengers": 10, "cost_hour": 4200, "final_score": 88},
    {"name": "Embraer Legacy 500", "type": "Jato executivo", "range_km": 5900, "max_passengers": 12, "cost_hour": 6800, "final_score": 74},
    {"name": "Cessna Citation XLS+", "type": "Jato executivo", "range_km": 3455, "max_passengers": 9, "cost_hour": 3900, "final_score": 81},
    {"name": "ATR 72-600", "type": "Turboélice regional", "range_km": 1528, "max_passengers": 70, "cost_hour": 2600, "final_score": 55},
])

MISSOES_HISTORICO = pd.DataFrame({
    "mes": ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"],
    "missoes": [12, 18, 15, 22, 28, 25],
})


# ─────────────────────────────────────────────────────────────
# 4. SIDEBAR — navegação + branding
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ✈️ Dumont Network")
    st.markdown(
        '<span class="badge badge-success">MVP</span> '
        '<span class="badge badge-warning">IA + Telemetria</span>',
        unsafe_allow_html=True,
    )
    st.divider()

    # st.radio como menu de navegação — mais leve que instalar uma lib de menu externa
    pagina = st.radio(
        "Navegação",
        ["Nova Missão", "Dashboard", "Frota"],
        label_visibility="collapsed",
    )

    st.divider()
    st.caption("Desenvolvido por Lennon Vinicius de Moraes Soares")


# ─────────────────────────────────────────────────────────────
# 5. PÁGINA: NOVA MISSÃO
# ─────────────────────────────────────────────────────────────
if pagina == "Nova Missão":
    st.title("Nova missão aérea")
    st.caption("Descreva a missão e receba a aeronave recomendada pela IA.")

    # st.tabs separa "formulário estruturado" de "texto livre" (a extração por LLM
    # que discutimos) sem precisar de duas páginas diferentes.
    tab_form, tab_texto = st.tabs(["📋 Formulário", "💬 Descrever em texto livre"])

    with tab_form:
        # st.columns organiza os campos lado a lado, em vez de empilhados —
        # usa muito menos espaço vertical e parece mais "formulário de produto".
        col1, col2, col3 = st.columns(3)
        with col1:
            origem = st.selectbox("Origem", ["SBSJ · São José dos Campos", "SBBR · Brasília", "SBGL · Rio de Janeiro"])
        with col2:
            destino = st.selectbox("Destino", ["SBBR · Brasília", "SBSJ · São José dos Campos", "SBGL · Rio de Janeiro"])
        with col3:
            passageiros = st.number_input("Passageiros", min_value=1, max_value=80, value=8)

        col4, col5 = st.columns(2)
        with col4:
            tipo_missao = st.selectbox("Tipo de missão", ["Executivo", "Carga", "Misto", "Regional"])
        with col5:
            prioridade = st.select_slider(
                "Prioridade",
                options=["Custo", "Equilibrado", "Velocidade"],
                value="Equilibrado",
            )

        buscar = st.button("Buscar recomendação", type="primary", use_container_width=True)

    with tab_texto:
        texto_livre = st.text_area(
            "Descreva a missão com suas palavras",
            placeholder='Ex: "Preciso levar 8 executivos de São José dos Campos pra Brasília, o mais rápido possível"',
            height=100,
        )
        st.button("Extrair dados com IA", use_container_width=True)
        st.caption("A IA identifica origem, destino, passageiros e prioridade automaticamente — você confirma antes de prosseguir.")

    # ── Resultado (aparece após buscar; aqui sempre visível pra fins de demo) ──
    st.divider()
    st.subheader("Resultado da análise")

    # KPIs em cards customizados via HTML, em vez do st.metric padrão —
    # dá mais controle visual (cor de fundo, borda), ao custo de escrever HTML.
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpis = [
        ("Distância", "850 km", kpi1),
        ("Tempo de voo", "1.0 h", kpi2),
        ("Custo estimado", "R$ 4.200", kpi3),
        ("Score final", "88", kpi4),
    ]
    for label, value, col in kpis:
        with col:
            st.markdown(
                f'<div class="kpi-card"><div class="kpi-label">{label}</div>'
                f'<div class="kpi-value">{value}</div></div>',
                unsafe_allow_html=True,
            )

    st.write("")  # pequeno respiro vertical entre seções

    col_map, col_ai = st.columns([1, 1])

    with col_map:
        st.markdown("**Rota**")
        with st.container(border=True):
            st.info("📍 São José dos Campos (SBSJ) → Brasília (SBBR)\n\n**850 km** em linha reta")
            # Aqui, no projeto real, entraria o mapa com folium (ver seção 7 do
            # guia de banco/frontend) — por ora, um placeholder textual estilizado.

    with col_ai:
        st.markdown("**Recomendação da IA**")
        with st.container(border=True):
            st.success("✅ **Embraer Phenom 300** — melhor opção para esta missão")
            st.caption(
                "Maior score para prioridade equilibrada nesta rota, com autonomia de "
                "3.650 km e capacidade para 10 passageiros, dentro do necessário."
            )

    # Ranking com Plotly — bem mais bonito e interativo que um st.bar_chart puro
    st.markdown("**Ranking de aeronaves compatíveis**")
    df_rank = AIRCRAFTS.sort_values("final_score", ascending=True)
    fig = go.Figure(go.Bar(
        x=df_rank["final_score"],
        y=df_rank["name"],
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


# ─────────────────────────────────────────────────────────────
# 6. PÁGINA: DASHBOARD
# ─────────────────────────────────────────────────────────────
elif pagina == "Dashboard":
    st.title("Dashboard operacional")
    st.caption("Visão geral de uso do sistema — dado fictício de exemplo.")

    kpi1, kpi2, kpi3 = st.columns(3)
    for label, value, col in [
        ("Missões este mês", "25", kpi1),
        ("Aeronave mais usada", "Phenom 300", kpi2),
        ("Custo médio/missão", "R$ 4.850", kpi3),
    ]:
        with col:
            st.markdown(
                f'<div class="kpi-card"><div class="kpi-label">{label}</div>'
                f'<div class="kpi-value">{value}</div></div>',
                unsafe_allow_html=True,
            )

    st.write("")
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("**Missões por mês**")
        fig_line = px.line(MISSOES_HISTORICO, x="mes", y="missoes", markers=True)
        fig_line.update_traces(line_color="#0F4C81")
        fig_line.update_layout(
            height=280, margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(family="Inter, sans-serif"),
        )
        st.plotly_chart(fig_line, use_container_width=True)

    with col_b:
        st.markdown("**Distribuição por tipo de aeronave**")
        fig_pie = px.pie(AIRCRAFTS, names="type", hole=0.5,
                          color_discrete_sequence=["#0F4C81", "#4C9F70", "#CBD5E1"])
        fig_pie.update_layout(
            height=280, margin=dict(l=10, r=10, t=10, b=10),
            font=dict(family="Inter, sans-serif"),
        )
        st.plotly_chart(fig_pie, use_container_width=True)


# ─────────────────────────────────────────────────────────────
# 7. PÁGINA: FROTA
# ─────────────────────────────────────────────────────────────
else:
    st.title("Frota cadastrada")
    st.caption("Aeronaves disponíveis no banco de dados.")

    filtro_tipo = st.multiselect(
        "Filtrar por tipo",
        options=AIRCRAFTS["type"].unique(),
        default=list(AIRCRAFTS["type"].unique()),
    )
    df_filtrado = AIRCRAFTS[AIRCRAFTS["type"].isin(filtro_tipo)]

    # st.dataframe com column_config deixa a tabela nativa muito mais legível
    # que o padrão cru — formata número, barra de progresso, etc, sem HTML.
    st.dataframe(
        df_filtrado,
        use_container_width=True,
        hide_index=True,
        column_config={
            "name": st.column_config.TextColumn("Aeronave"),
            "type": st.column_config.TextColumn("Tipo"),
            "range_km": st.column_config.NumberColumn("Autonomia (km)", format="%d km"),
            "max_passengers": st.column_config.NumberColumn("Passageiros"),
            "cost_hour": st.column_config.NumberColumn("Custo/hora", format="R$ %d"),
            "final_score": st.column_config.ProgressColumn(
                "Score", min_value=0, max_value=100, format="%d"
            ),
        },
    )
