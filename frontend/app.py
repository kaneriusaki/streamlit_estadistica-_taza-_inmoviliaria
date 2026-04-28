import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from fpdf import FPDF

# Configuración de página
st.set_page_config(page_title="Tasador Inmobiliario Premium", page_icon=":material/domain:", layout="wide")

# Estilos CSS personalizados Premium
st.markdown("""
    <style>
    /* Fondo principal y tipografía */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        color: #f8fafc;
        font-family: 'Inter', 'Outfit', 'Segoe UI', sans-serif;
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
        background: linear-gradient(120deg, #a78bfa 0%, #f472b6 50%, #38bdf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.8rem;
        font-weight: 900;
        margin-bottom: 0.2rem;
        text-shadow: 0px 10px 30px rgba(167, 139, 250, 0.2);
    }
    
    .premium-subtitle {
        text-align: center; 
        color: #cbd5e1; 
        font-size: 1.3rem; 
        margin-bottom: 3rem;
        font-weight: 300;
        letter-spacing: 0.5px;
    }
    
    /* Métricas con glassmorphism */
    div[data-testid="metric-container"] {
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px !important;
        padding: 1.5rem !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 15px 35px -5px rgba(167, 139, 250, 0.25);
        border: 1px solid rgba(167, 139, 250, 0.4);
    }
    
    div[data-testid="metric-container"] label {
        color: #e2e8f0 !important;
        font-size: 1.15rem !important;
        font-weight: 500;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.6) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
    }
    
    /* Botones primarios */
    .stButton>button {
        background: linear-gradient(90deg, #8b5cf6 0%, #d946ef 100%);
        color: white;
        font-weight: 700;
        font-size: 1.1rem;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1.2rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px 0 rgba(139, 92, 246, 0.4);
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #7c3aed 0%, #c026d3 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px 0 rgba(139, 92, 246, 0.5);
    }
    .stButton>button:active {
        transform: scale(0.96);
    }
    
    /* Pestañas (Tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 3.5rem;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 8px 8px 0px 0px;
        gap: 1rem;
        padding-top: 10px;
        padding-bottom: 10px;
        color: #cbd5e1;
        font-weight: 600;
        transition: color 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        color: #f472b6 !important;
        border-bottom: 3px solid #f472b6 !important;
        background: linear-gradient(180deg, rgba(244,114,182,0) 0%, rgba(244,114,182,0.1) 100%);
    }
    </style>
""", unsafe_allow_html=True)

API_URL = "http://localhost:8000/api"

# --- SIDEBAR: TASADOR AUTOMÁTICO ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>Tasador Inmobiliario</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>Introduce los datos de la propiedad para estimar su valor en el mercado.</p>", unsafe_allow_html=True)
    
    st.divider()

    area_m2 = st.number_input(":material/square_foot: Área de la propiedad (m²)", 40, 500, 100, step=1)
    
    col_hab, col_ban = st.columns(2)
    with col_hab:
        habitaciones = st.number_input(":material/bed: Habitaciones", 1, 8, 3, step=1)
    with col_ban:
        banos = st.number_input(":material/bathtub: Baños", 1, 5, 2, step=1)
        
    distancia = st.number_input(":material/location_on: Distancia al centro (km)", 0.1, 30.0, 5.0, step=0.1)
    antiguedad = st.number_input(":material/domain_add: Antigüedad (años)", 0, 50, 10, step=1)
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

def generate_pdf_report(df, stats):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font('helvetica', 'B', 24)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 15, 'Reporte de Preferencias de Mercado', new_x="LMARGIN", new_y="NEXT", align='C')
    
    pdf.set_font('helvetica', 'I', 12)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 10, 'Generado por IA Real Estate Analytics', new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(10)
    
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(56, 189, 248)
    pdf.cell(0, 10, '1. Preferencias de Mercado Mas Comunes', new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font('helvetica', '', 12)
    pdf.set_text_color(0, 0, 0)
    hab_comun = df['habitaciones'].mode()[0]
    area_promedio = df['area_m2'].mean()
    pdf.multi_cell(0, 8, f"- Habitaciones mas solicitadas: {int(hab_comun)} habitaciones.\n- Area promedio del mercado: {area_promedio:.1f} metros cuadrados.")
    pdf.ln(5)
    
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(56, 189, 248)
    pdf.cell(0, 10, '2. Preferencias Menos Comunes (Atipicas)', new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font('helvetica', '', 12)
    pdf.set_text_color(0, 0, 0)
    banos_menos_comun = df['banos'].value_counts().idxmin()
    pdf.multi_cell(0, 8, f"- La cantidad de banos menos frecuente es: {int(banos_menos_comun)} banos.\n- Propiedades muy grandes (>6 habs): {len(df[df['habitaciones'] > 6])}\n- Propiedades antiguas (>40 anios): {len(df[df['antiguedad_anos'] > 40])}\n- Propiedades pequenas con piscina: {len(df[(df['area_m2'] < 80) & (df['tiene_piscina'] == 1)])}")
    pdf.ln(5)
    
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(56, 189, 248)
    pdf.cell(0, 10, '3. Analisis Economico: Impacto en Precio', new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font('helvetica', '', 12)
    pdf.set_text_color(0, 0, 0)
    coefs = stats['feature_importance']
    mas_caras = sorted(coefs.items(), key=lambda x: x[1], reverse=True)[:2]
    mas_baratas = sorted(coefs.items(), key=lambda x: x[1])[:2]
    
    format_names = {
        "area_m2": "Area (m2)",
        "habitaciones": "Habitaciones",
        "banos": "Banos",
        "distancia_centro_km": "Distancia al Centro (km)",
        "antiguedad_anos": "Antiguedad (anios)",
        "tiene_piscina": "Tiene Piscina"
    }
    
    n_cara = format_names.get(mas_caras[0][0], mas_caras[0][0])
    v_cara = mas_caras[0][1]
    n_barata = format_names.get(mas_baratas[0][0], mas_baratas[0][0])
    v_barata = mas_baratas[0][1]
    
    pdf.multi_cell(0, 8, f"Caracteristica mas cara: {n_cara} (+${v_cara:,.0f})\nCaracteristica que mas devalua: {n_barata} (${v_barata:,.0f})")
    pdf.ln(5)
    
    pdf.multi_cell(0, 8, f"Desglose de costos principales:\n- Cada m2 extra suma: ${coefs.get('area_m2', 0):,.0f}\n- Cada km lejos del centro resta: ${abs(coefs.get('distancia_centro_km', 0)):,.0f}\n- Cada anio de antiguedad resta: ${abs(coefs.get('antiguedad_anos', 0)):,.0f}")
    
    pdf.ln(15)
    pdf.set_font('helvetica', 'I', 10)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 10, 'Documento generado de forma automatizada por IA.', new_x="LMARGIN", new_y="NEXT", align='C')
    
    return bytes(pdf.output())

col_title, col_btn = st.columns([0.8, 0.2])
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    pdf_bytes = generate_pdf_report(df, stats)
    st.download_button(
        label="📄 Descargar Reporte PDF",
        data=pdf_bytes,
        file_name="reporte_preferencias_inmobiliarias.pdf",
        mime="application/pdf",
        use_container_width=True
    )

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
t_map, t_factors, t_prefs_common, t_prefs_rare, t_prefs_cost, t_data = st.tabs([
    ":material/map: Oportunidades", 
    ":material/psychology: Factores", 
    ":material/thumb_up: Más Comunes", 
    ":material/thumb_down: Menos Comunes",
    ":material/price_change: Impacto y Costos",
    ":material/table_chart: Datos"
])

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

with t_prefs_common:
    st.markdown("### :material/thumb_up: Preferencias de Mercado Más Comunes")
    st.caption("Características y configuraciones más frecuentes y buscadas en el mercado inmobiliario actual.")
    c1, c2 = st.columns(2)
    with c1:
        # Gráfico Habitaciones más comunes
        hab_counts = df['habitaciones'].value_counts().reset_index()
        hab_counts.columns = ['Habitaciones', 'Cantidad']
        fig_hab = px.pie(hab_counts, values='Cantidad', names='Habitaciones', title='Distribución de Habitaciones', hole=0.4, color_discrete_sequence=px.colors.sequential.Teal)
        fig_hab.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color="#f8fafc"))
        st.plotly_chart(fig_hab, use_container_width=True)
    with c2:
        # Rango de área más común
        area_bins = pd.cut(df['area_m2'], bins=5).value_counts().reset_index()
        area_bins.columns = ['Rango Área (m²)', 'Frecuencia']
        area_bins['Rango Área (m²)'] = area_bins['Rango Área (m²)'].astype(str)
        fig_area = px.bar(area_bins, x='Rango Área (m²)', y='Frecuencia', title='Áreas más habituales (m²)', color='Frecuencia', color_continuous_scale='Purpor')
        fig_area.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#f8fafc"))
        st.plotly_chart(fig_area, use_container_width=True)

with t_prefs_rare:
    st.markdown("### :material/thumb_down: Preferencias de Mercado Menos Comunes")
    st.caption("Características raras, nichos de mercado o propiedades atípicas que se ven con menor frecuencia.")
    
    col_rare1, col_rare2 = st.columns(2)
    with col_rare1:
        # Menos comunes en baños
        banos_counts = df['banos'].value_counts().sort_values(ascending=True).reset_index()
        banos_counts.columns = ['Baños', 'Cantidad']
        fig_banos = px.bar(banos_counts, x='Baños', y='Cantidad', title='Baños menos frecuentes (de menor a mayor)', color='Cantidad', color_continuous_scale='OrRd')
        fig_banos.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#f8fafc"))
        fig_banos.update_xaxes(type='category')
        st.plotly_chart(fig_banos, use_container_width=True)
    with col_rare2:
        # Piscinas vs no piscinas en propiedades extremas
        st.markdown("#### Propiedades Atípicas")
        st.write(f"- 🏠 **Propiedades con más de 6 habitaciones:** {len(df[df['habitaciones'] > 6])} encontradas.")
        st.write(f"- 🏛️ **Propiedades más antiguas (>40 años):** {len(df[df['antiguedad_anos'] > 40])} encontradas.")
        st.write(f"- 🏊 **Propiedades muy pequeñas con piscina:** {len(df[(df['area_m2'] < 80) & (df['tiene_piscina'] == 1)])} encontradas.")

with t_prefs_cost:
    st.markdown("### :material/price_change: Análisis Económico de Preferencias")
    st.caption("Descubre cuáles preferencias encarecen o abaratan más una propiedad según nuestro análisis.")
    
    coefs = stats['feature_importance']
    mas_caras = sorted(coefs.items(), key=lambda x: x[1], reverse=True)[:2]
    mas_baratas = sorted(coefs.items(), key=lambda x: x[1])[:2]
    
    st.info(f"**💡 Insight Económico:** La preferencia que MÁS eleva el precio es **{format_names.get(mas_caras[0][0], mas_caras[0][0])}** (+${mas_caras[0][1]:,.0f} por unidad). La característica que MÁS abarata una propiedad es **{format_names.get(mas_baratas[0][0], mas_baratas[0][0])}** (${mas_baratas[0][1]:,.0f} por unidad).")

    st.markdown("#### Análisis Detallado por Característica")
    an_tipo = st.radio("Selecciona la característica a analizar:", ["Área", "Distancia", "Antigüedad"], horizontal=True)
    
    if an_tipo == "Área":
        fig = px.scatter(df, x="area_m2", y="precio_lista", color="habitaciones", trendline="ols",
                         title="Relación Precio vs Área (m²)", labels={"area_m2": "Área (m²)", "precio_lista": "Precio Solicitado ($)"})
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#f8fafc"))
        st.plotly_chart(fig, use_container_width=True)
    elif an_tipo == "Distancia":
        fig = px.scatter(df, x="distancia_centro_km", y="precio_lista", color="tiene_piscina", trendline="ols",
                         title="Efecto de la Distancia al Centro sobre el Precio", labels={"distancia_centro_km": "Distancia al Centro (km)", "precio_lista": "Precio Solicitado ($)"})
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#f8fafc"))
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig = px.scatter(df, x="antiguedad_anos", y="precio_lista", color="banos", trendline="ols",
                         title="Depreciación por Antigüedad", labels={"antiguedad_anos": "Antigüedad (años)", "precio_lista": "Precio Solicitado ($)"})
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#f8fafc"))
        st.plotly_chart(fig, use_container_width=True)

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
