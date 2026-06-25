import streamlit as st
import pandas as pd
from data_client import DataClient

# Importar componentes modulares
from components.styles import inject_custom_css
from components.sidebar import render_sidebar
from components.report import generate_pdf_report
from components.views import (
    render_kpis,
    render_opportunities_tab,
    render_factors_tab,
    render_common_preferences_tab,
    render_rare_preferences_tab,
    render_economic_analysis_tab,
    render_data_tab,
    render_history_tab
)

# Configuración de página
st.set_page_config(
    page_title="Tasador Inmobiliario Premium",
    page_icon=":material/domain:",
    layout="wide"
)

# Inyectar estilos CSS Premium personalizados
inject_custom_css()

# --- CLIENTE DE DATOS ---
if "data_client" not in st.session_state:
    st.session_state.data_client = DataClient("http://localhost:8000/api")
data_client = st.session_state.data_client

# --- SESIÓN DE USUARIO ---
if "user_id" not in st.session_state:
    st.session_state.user_id = None
    st.session_state.user_name = None

# --- CARGA DE DATOS ---
@st.cache_data(ttl=60)
def load_data():
    temp_client = DataClient("http://localhost:8000/api")
    try:
        props = temp_client.get_properties()
        stats = temp_client.get_stats_insight()
        opps = temp_client.get_opportunities()
        return pd.DataFrame(props), stats, pd.DataFrame(opps), True
    except Exception:
        return None, None, None, False

with st.spinner("Cargando métricas del mercado..."):
    df, stats, df_opps, api_online = load_data()

# --- RENDERIZAR PANEL LATERAL (SIDEBAR) ---
render_sidebar(data_client, api_online)

# --- CONTENIDO PRINCIPAL ---
st.markdown("<h1 class='premium-title'>Market Analytics & Real Estate</h1>", unsafe_allow_html=True)
st.markdown("<p class='premium-subtitle'>Plataforma avanzada de análisis inmobiliario potenciada por Machine Learning</p>", unsafe_allow_html=True)

# Validación de datos cargados
if df is None:
    st.error("⚠️ **Error Crítico de Datos:** No se pudo obtener la información del mercado. El servidor de la API está fuera de servicio.")
    st.stop()

# --- BOTÓN DE REPORTE PDF ---
col_title, col_btn = st.columns([0.8, 0.2])
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    try:
        pdf_bytes = generate_pdf_report(df, stats)
        st.download_button(
            label="📄 Descargar Reporte PDF",
            data=pdf_bytes,
            file_name="reporte_preferencias_inmobiliarias.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except Exception as e:
        st.error("❌ Error al generar reporte PDF")

# --- RENDERIZAR KPIs ---
render_kpis(df, stats, df_opps)

st.markdown("<br><br>", unsafe_allow_html=True)

# --- RENDERIZAR TABS / VISTAS ---
t_map, t_factors, t_prefs_common, t_prefs_rare, t_prefs_cost, t_data, t_history = st.tabs([
    ":material/map: Oportunidades", 
    ":material/psychology: Factores", 
    ":material/thumb_up: Más Comunes", 
    ":material/thumb_down: Menos Comunes",
    ":material/price_change: Impacto y Costos",
    ":material/table_chart: Datos",
    ":material/history: Historial"
])

with t_map:
    render_opportunities_tab(df, df_opps)

with t_factors:
    render_factors_tab(stats)

with t_prefs_common:
    render_common_preferences_tab(df)

with t_prefs_rare:
    render_rare_preferences_tab(df)

with t_prefs_cost:
    render_economic_analysis_tab(df, stats)

with t_data:
    render_data_tab(df_opps)

with t_history:
    render_history_tab(data_client, api_online)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748b; font-size: 0.9rem;'>© 2026 Inteligencia Artificial Real Estate • Todos los derechos reservados</p>", unsafe_allow_html=True)
