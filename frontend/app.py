import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración de página
st.set_page_config(page_title="Tasador Inmobiliario Premium", page_icon=":material/domain:", layout="wide")

# Estilos CSS personalizados Premium
st.markdown("""
    <style>
    /* Fondo principal y tipografía */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgb(15, 23, 42) 0%, rgb(20, 28, 48) 90%);
        color: #f8fafc;
        font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #f1f5f9;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    /* Titulo principal */
    .premium-title {
        text-align: center;
        background: linear-gradient(120deg, #818cf8 0%, #38bdf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    
    .premium-subtitle {
        text-align: center; 
        color: #94a3b8; 
        font-size: 1.25rem; 
        margin-bottom: 3rem;
        font-weight: 300;
    }
    
    /* Métricas con glassmorphism */
    div[data-testid="metric-container"] {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(12px);
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px !important;
        padding: 1.5rem !important;
        transition: transform 0.3s ease, box-shadow 0.3s ease, border 0.3s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px -3px rgba(56, 189, 248, 0.15);
        border: 1px solid rgba(56, 189, 248, 0.3);
    }
    
    div[data-testid="metric-container"] label {
        color: #cbd5e1 !important;
        font-size: 1.1rem !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.7) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
    }
    
    /* Botones primarios */
    .stButton>button {
        background: linear-gradient(90deg, #6366f1 0%, #38bdf8 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.2rem;
        transition: opacity 0.2s ease, transform 0.1s ease;
        box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.39);
    }
    .stButton>button:hover {
        opacity: 0.9;
        transform: scale(1.02);
    }
    .stButton>button:active {
        transform: scale(0.98);
    }
    
    /* Pestañas (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        gap: 1rem;
        padding-top: 10px;
        padding-bottom: 10px;
        color: #94a3b8;
    }
    .stTabs [aria-selected="true"] {
        color: #38bdf8 !important;
        border-bottom: 2px solid #38bdf8 !important;
    }
    </style>
""", unsafe_allow_html=True)

API_URL = "http://localhost:8000/api"

# --- SIDEBAR: TASADOR AUTOMÁTICO ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>Tasador Inmobiliario</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>Introduce los datos de la propiedad para estimar su valor en el mercado.</p>", unsafe_allow_html=True)
    
    st.divider()

    area_m2 = st.slider(":material/square_foot: Área de la propiedad (m²)", 40, 500, 100)
    
    col_hab, col_ban = st.columns(2)
    with col_hab:
        habitaciones = st.number_input(":material/bed: Habitaciones", 1, 8, 3)
    with col_ban:
        banos = st.number_input(":material/bathtub: Baños", 1, 5, 2)
        
    distancia = st.slider(":material/location_on: Distancia al centro (km)", 0.1, 30.0, 5.0)
    antiguedad = st.slider(":material/domain_add: Antigüedad (años)", 0, 50, 10)
    piscina = st.radio(":material/pool: ¿Cuenta con Piscina?", ["No", "Sí"], horizontal=True)
    piscina_val = 1 if piscina == "Sí" else 0

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button(":material/calculate: Calcular Tasación", use_container_width=True):
        with st.spinner("Analizando mercado..."):
            try:
                payload = {
                    "area_m2": area_m2,
                    "habitaciones": habitaciones,
                    "banos": banos,
                    "distancia_centro_km": distancia,
                    "antiguedad_anos": antiguedad,
                    "tiene_piscina": piscina_val
                }
                res = requests.post(f"{API_URL}/predict", json=payload)
                if res.status_code == 200:
                    data = res.json()
                    st.success(f"### Valor Estimado: ${data['predicted_price']:,.0f}\n\nMargen de Error: ±${data['margin_of_error']:,.0f}")
                else:
                    st.error("❌ Error al calcular con la API.")
            except requests.exceptions.ConnectionError:
                st.error("❌ No se pudo conectar con el motor estadístico (API).")

# --- MAIN CONTENT ---
st.markdown("<h1 class='premium-title'>Market Analytics & Real Estate</h1>", unsafe_allow_html=True)
st.markdown("<p class='premium-subtitle'>Plataforma avanzada de análisis inmobiliario potenciada por Machine Learning</p>", unsafe_allow_html=True)

# Cargar datos
@st.cache_data(ttl=60)
def load_data():
    try:
        props = requests.get(f"{API_URL}/properties").json()
        stats = requests.get(f"{API_URL}/stats_insight").json()
        opps = requests.get(f"{API_URL}/opportunities").json()
        return pd.DataFrame(props), stats, pd.DataFrame(opps)
    except Exception as e:
        return None, None, None

with st.spinner("Cargando métricas del mercado..."):
    df, stats, df_opps = load_data()

if df is None:
    st.error("⚠️ **Error de conexión:** El motor de datos analítico (Backend) no está en línea. Ejecuta `uvicorn main:app` en la carpeta backend para iniciarlo.")
    st.stop()

# --- KPIs ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Precio Medio del Mercado", f"${df['precio_lista'].mean():,.0f}", "Tendencia estable")
with col2:
    st.metric("Área Promedio", f"{df['area_m2'].mean():.1f} m²", f"{len(df)} propiedades analizadas")
with col3:
    st.metric("Oportunidades (Infravaloradas)", f"{len(df_opps)}", "Encontradas hoy", delta_color="normal")
with col4:
    st.metric("Precisión IA (R²)", f"{stats['model_metrics']['r2_score'] * 100:.1f}%", "Alto nivel de confianza", delta_color="normal")

st.markdown("<br><br>", unsafe_allow_html=True)

# --- CHARTS ---
t_map, t_factors, t_data = st.tabs([":material/map: Mapa de Oportunidades", ":material/psychology: Factores de Impacto", ":material/table_chart: Tabla de Datos"])

with t_map:
    st.markdown("### :material/location_on: Oportunidades vs Mercado General")
    st.caption("Las propiedades marcadas con diamantes verdes representan oportunidades matemáticas detectadas por nuestro algoritmo, encontrándose subvaloradas respecto al mercado general.")
    # Mapa de Mercado: Oportunidades vs Resto
    fig_map = go.Figure()
    # Mercado regular
    df_regular = df[~df['es_oportunidad']]
    fig_map.add_trace(go.Scatter(
        x=df_regular['longitud'], y=df_regular['latitud'], mode='markers',
        marker=dict(size=8, color='#475569', opacity=0.4),
        name="Mercado General"
    ))
    # Oportunidades
    fig_map.add_trace(go.Scatter(
        x=df_opps['longitud'], y=df_opps['latitud'], mode='markers',
        marker=dict(size=14, color='#10b981', symbol='diamond', line=dict(width=1, color='white')),
        name="Oportunidades",
        hovertext=df_opps['precio_lista'].apply(lambda x: f"Listado: ${x:,.0f}")
    ))
    fig_map.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=600,
        margin=dict(l=0, r=0, t=30, b=0),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor="rgba(15, 23, 42, 0.8)"),
        font=dict(color="#f8fafc")
    )
    st.plotly_chart(fig_map, use_container_width=True)

with t_factors:
    st.markdown("### :material/bar_chart: ¿Qué es lo que verdaderamente influye en el precio?")
    st.caption("Pesos calculados por nuestro modelo de Inteligencia Artificial que explican qué características aumentan o disminuyen el valor de una propiedad.")
    coefs = stats['feature_importance']
    df_coefs = pd.DataFrame(list(coefs.items()), columns=['Característica', 'Impacto en el Precio (USD)'])
    df_coefs = df_coefs.sort_values(by='Impacto en el Precio (USD)', ascending=True)
    
    # Formatear nombres de características
    format_names = {
        "area_m2": "Área (m²)",
        "habitaciones": "Nro. Habitaciones",
        "banos": "Nro. Baños",
        "distancia_centro_km": "Cercanía al Centro",
        "antiguedad_anos": "Antigüedad",
        "tiene_piscina": "Tiene Piscina"
    }
    df_coefs['Característica'] = df_coefs['Característica'].map(format_names).fillna(df_coefs['Característica'])
    
    fig_coefs = px.bar(df_coefs, x='Impacto en el Precio (USD)', y='Característica', orientation='h',
                       color='Impacto en el Precio (USD)', color_continuous_scale="icefire")
    fig_coefs.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=500,
        font=dict(color="#f8fafc")
    )
    st.plotly_chart(fig_coefs, use_container_width=True)

with t_data:
    st.markdown("### :material/list_alt: Top Oportunidades Detectadas")
    if not df_opps.empty:
        st.dataframe(
            df_opps[['id', 'precio_lista', 'precio_predicho', 'diferencia', 'area_m2', 'habitaciones']].rename(columns={
                'id': 'ID Propiedad',
                'precio_lista': 'Precio Solicitado',
                'precio_predicho': 'Tasación Real (IA)',
                'diferencia': 'Ganancia Potencial',
                'area_m2': 'Metros Cuadrados',
                'habitaciones': 'Habitaciones'
            }).style.format({
                'Precio Solicitado': '${:,.0f}',
                'Tasación Real (IA)': '${:,.0f}',
                'Ganancia Potencial': '${:,.0f}'
            }),
            use_container_width=True,
            hide_index=True,
            height=400
        )
    else:
        st.info("No se encontraron propiedades significativamente infravaloradas en el rastreo actual.")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748b; font-size: 0.9rem;'>© 2026 Inteligencia Artificial Real Estate • Todos los derechos reservados</p>", unsafe_allow_html=True)
