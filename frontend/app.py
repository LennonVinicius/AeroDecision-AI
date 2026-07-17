import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import requests
from streamlit_searchbox import st_searchbox
from streamlit_folium import st_folium
import pandas as pd
from map import router_map
 
 
dark = st.get_option("theme.base") == "dark"
font_color = "white" if dark else "black"
background = "#0E1117" if dark else "white"
grid = "#374151" if dark else "#E5E7EB"
 
 
@st.cache_data()
def fleet_load():
    aircraft_response = requests.get("http://127.0.0.1:8000/fleet/get_fleet")
    return pd.DataFrame(aircraft_response.json())
 
 
AIRCRAFTS = fleet_load()
 
 
@st.cache_data(ttl=60)
def load_historic_missions():
    response = requests.get("http://127.0.0.1:8000/recommendation/historic_missions")
    return pd.DataFrame(response.json())
 
 
MISSOES_HISTORICO = load_historic_missions()
 
 
def search_airports(searchterm: str):
    response = requests.get(
        "http://127.0.0.1:8000/airports/search",
        params={"q": searchterm}
    )
    airports = response.json()
    return [
        f"{a['icao']} - {a['name']} ({a['city']})"
        for a in airports
    ]
 
 
def extrair_icao(texto: str) -> str:
    return texto.split(" - ")[0].strip()
 


def render_formulario():
    col1, col2, col3 = st.columns(3)
    with col1:
        origem = st_searchbox(search_airports, label="Origem", key="origem_search")
    with col2:
        destino = st_searchbox(search_airports, label="Destino", key="destino_search")
    with col3:
        passageiros = st.number_input("Passageiros", min_value=1, max_value=99, value=1)
 
    col4, col5 = st.columns(2)
    with col4:
        tipo = st.selectbox("Tipo de missão", ["Executiva", "Carga", "Regional"])
    with col5:
        peso = st.number_input("Volume da Carga(Kg)", min_value=1, max_value=100000000)
 
    buscar = st.button("Gerar recomendação")
    if buscar:
        if not origem or not destino:
            st.error("Selecione origem e destino antes de gerar a recomendação.")
            st.stop()
 
        data = {
            "origin_airport": extrair_icao(origem),
            "destination_airport": extrair_icao(destino),
            "mission_type": tipo,
            "priority": tipo,
            "passengers": passageiros,
            "cargo_weight": peso,
        }
 
        with st.spinner("Analisando missão e consultando a  IA..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/recommendation/post_mission",
                    json=data,
                    timeout=120
                )
            except requests.exceptions.Timeout:
                st.error("Timeout: a IA demorou demais para responder")
                st.stop()
            except requests.exceptions.RequestException as e:
                st.error(f"Erro de conexão: {e}")
                st.stop()
 
            if response.status_code == 200:
                st.session_state["aircraft_info"] = response.json()

                st.rerun()
            else:
                st.error(f"Erro {response.status_code} : {response.text}")
 

@st.fragment
def render_resultados():
    st.subheader("Resultados da análise")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    if "aircraft_info" in st.session_state:
        aircraft_info = st.session_state["aircraft_info"]
        kpis = [
            ("Distância (Km)", f'{aircraft_info["distance"]:.2f}', kpi1),
            ("Tempo de voo(Horas)", f'{aircraft_info["mission_time"]:.2f}', kpi2),
            ("Custo estimado (US$)", f'{aircraft_info["total_cost"]:.2f}', kpi3),
            ("Score da Aeronave escolhida", f'{aircraft_info["final_score"]:.1f}', kpi4)
        ]
        for label, value, col in kpis:
            with col:
                st.markdown(
                    f"""
                    <div class="kpi-card">
                        <div class="kpi-label">{label}</div>
                        <div class="kpi-value">{value}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
 
    col_map, col_ai = st.columns(2)
    with col_map:
        st.markdown("**Rota**")
        with st.container(border=True):
            if "aircraft_info" in st.session_state:
                aircraft_info = st.session_state["aircraft_info"]
                if ("map_cache" not in st.session_state
                        or st.session_state.get("map_mission_id") != aircraft_info.get("mission_id")):
                    st.session_state["map_cache"] = router_map(
                        aircraft_info["origem_lat"],
                        aircraft_info["origem_lon"],
                        aircraft_info["destino_lat"],
                        aircraft_info["destino_lon"],
                        aircraft_info["origin_name"],
                        aircraft_info["destination_name"]
                    )
                    st.session_state["map_mission_id"] = aircraft_info.get("mission_id")
 
                try:
                    st_folium(
                        st.session_state["map_cache"],
                        width="stretch",
                        height=300,
                        key="route_map",
                        returned_objects=[]
                    )
                except TypeError:
                    st_folium(
                        st.session_state["map_cache"],
                        width="stretch",
                        height=300,
                        key="route_map",
                        returned_objects=[]
                    )
                    
            else:
                st.info("Gere uma recomendação para visualizar  a rota")

                
    with col_ai:
        st.markdown("**Resultado da IA**")
        with st.container(border=True):
            if "aircraft_info" in st.session_state:
                aircraft_info = st.session_state["aircraft_info"]
                st.success(aircraft_info["best"])
                st.info(aircraft_info["resposta"])
  
    st.markdown("**Condições da Missão**")
    with st.container(border=True):
        if "aircraft_info" in st.session_state:
            aircraft = st.session_state["aircraft_info"]
            col_we, col_ve, col_vi, col_pr, col_te = st.columns(5)
            with col_we:
                st.metric(
                    "Weather Score",
                    f"{aircraft['weather_score']:.1f}"
                )
            with col_ve:
                st.metric(
                    "Vento",
                    f"{aircraft['avg_wind']:.1f} km/h"
                )
            with col_vi:
                st.metric(
                    "Visibilidade",
                    f"{aircraft['avg_visibility']/1000:.1f} km"
                )
            with col_pr:
                st.metric(
                    "Precipitação",
                    f"{aircraft['avg_precipitation']:.1f} mm"
                )
            with col_te:
                st.metric(
                    "Temperatura",
                    f"{aircraft['avg_temperature']:.1f}°C"
                )
            st.divider()
            st.markdown(f"Score climático: {aircraft["weather_score"]}/100")
            st.progress(aircraft["weather_score"]/100)
    
    if "aircraft_info" in st.session_state:
        aircraft_info = st.session_state["aircraft_info"]
        ranking_list = aircraft_info.get("ranking", [])
        if ranking_list:
            df_rank = pd.DataFrame(ranking_list)
            st.markdown("**Ranking de aeronaves compatíveis**")
            df_rank = df_rank.sort_values("final_score", ascending=True)
            fig = go.Figure(go.Bar(
                x=df_rank["final_score"],
                y=df_rank["name"],
                orientation="h",
                marker_color=["#0F4C81" if s == df_rank["final_score"].max() else "#CBD5E1" for s in df_rank["final_score"]],
                text=df_rank["final_score"].round(1),
                textposition="outside",
            ))
            fig.update_layout(
                font=dict(color=font_color),
                height=260,
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis=dict(range=[0, 100], showgrid=True, gridcolor=grid, tickfont=dict(color=font_color)),
                yaxis=dict(tickfont=dict(color=font_color)),
                plot_bgcolor=background,
                paper_bgcolor=background,
            )
            st.plotly_chart(fig, width="stretch")
        else:
            st.info("Nenhum ranking disponível para esta missão")
    else:
        st.info("Nenhum ranking disponível para esta missão")
 
 
st.set_page_config(
    page_title="AeroDecisionAI",
    page_icon="📍",
    layout="wide",
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
    .badge-success { background-color: #FF623C; color: #065F46; }
    .badge-warning { background-color: #25328E; color: #92400E; }
 
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
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
 
with st.sidebar:
    st.title("AeroDecisionAI")
    st.markdown(
        '<span class="badge badge-success">MVP</span> '
        '<span class="badge badge-warning">AI</span>',
        unsafe_allow_html=True,
    )
 
    st.divider()
    page = st.radio("Navigation", ["Nova página", "Dashboard", "Frota"])
    st.divider()
    st.caption("Desenvolvido por Lennon Vinicius de Moraes")
 
 
if page == "Nova página":
    st.title("Nova missão")
    st.markdown("Preencha os campos a abaixo e receba a aeronave recomendada pela IA")
 
    tab_form, tab_text = st.tabs(["Formulário", "Descreva em texto livre"])

    with tab_form:
        render_formulario()
        st.divider()
        render_resultados()
 
elif page == "Dashboard":
    st.title("Dashboard Operacional")
    st.caption("Visão geral do uso do Sistema")
 
    missions_month_response = requests.get(
        "http://127.0.0.1:8000/dashboard/get_missions_month",
        timeout=120
    )
    missions_month_response_json = missions_month_response.json()
    aircraft_most_used = requests.get(
        "http://127.0.0.1:8000/dashboard/get_most_used_aircraft",
        timeout=120
    )
    aircraft_most_used_json = aircraft_most_used.json()
    cost_per_mission = requests.get(
        "http://127.0.0.1:8000/dashboard/cost",
        timeout=120
    )
    cost_per_mission_json = cost_per_mission.json()
    kpi1, kpi2, kpi3 = st.columns(3)
    for label, value, col in [
        ("Missões este mês", missions_month_response_json, kpi1),
        ("Aeronave mais usada", aircraft_most_used_json["aircraft"], kpi2),
        ("Custo médio/missão", f'{cost_per_mission_json:.2f}', kpi3),
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
        df_missoes = MISSOES_HISTORICO.copy()
        df_missoes["created_at"] = pd.to_datetime(df_missoes["created_at"])
        df_missoes["mes"] = df_missoes["created_at"].dt.to_period("M").astype(str)
        missoes_por_mes = df_missoes.groupby("mes").size().reset_index(name="total_missoes")
 
        st.markdown("**Missões por mês**")
        fig_line = px.line(missoes_por_mes, x="mes", y="total_missoes", markers=True)
        fig_line.update_traces(line_color="#0F4C81")
        fig_line.update_layout(
            height=280, margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor="white", paper_bgcolor="white",
            font=dict(family="Inter, sans-serif"),
        )
        st.plotly_chart(fig_line, width="stretch")
 
    with col_b:
        st.markdown("**Distribuição por tipo de aeronave**")
        response_type = requests.get(
            "http://127.0.0.1:8000/dashboard/aircraft_by_type",
            timeout=120
        )
        per_type = pd.DataFrame(response_type.json())
 
        fig_pie = px.pie(per_type, names="aircraft_type", hole=0.5,
                          color_discrete_sequence=["#0F4C81", "#4C9F70", "#CBD5E1"])
        fig_pie.update_layout(
            height=280, margin=dict(l=10, r=10, t=10, b=10),
            font=dict(family="Inter, sans-serif"),
        )
        st.plotly_chart(fig_pie, width="stretch")
 
else:
    st.title("Frota cadastrada")
    st.caption("Aeronaves disponíveis no banco de dados.")
    filtro_tipo = st.multiselect(
        "Filtrar por tipo",
        options=AIRCRAFTS["aircraft_type"].unique(),
        default=list(AIRCRAFTS["aircraft_type"].unique()),
    )
    df_filtrado = AIRCRAFTS[AIRCRAFTS["aircraft_type"].isin(filtro_tipo)]
    st.dataframe(
        df_filtrado,
        width="stretch",
        hide_index=True,
        column_config={
            "name": st.column_config.TextColumn("Aeronave"),
            "aircraft_type": st.column_config.TextColumn("Tipo"),
            "manufacturer": st.column_config.TextColumn("Manufatura"),
            "range_km": st.column_config.NumberColumn("Autonomia (km)", format="%d km"),
            "max_passengers": st.column_config.NumberColumn("Passageiros"),
            "cost_hour": st.column_config.NumberColumn("Custo/hora", format="R$ %d")
        },
    )