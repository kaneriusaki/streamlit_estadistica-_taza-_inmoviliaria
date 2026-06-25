import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def render_kpis(df: pd.DataFrame, stats: dict, df_opps: pd.DataFrame):
    """Renderiza las tarjetas de KPIs principales en el Dashboard."""
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Precio Medio del Mercado", f"${df['precio_lista'].mean():,.0f}", "Tendencia estable")
    with col2:
        st.metric("Área Promedio", f"{df['area_m2'].mean():.1f} m²", f"{len(df)} propiedades analizadas")
    with col3:
        st.metric("Oportunidades (Infravaloradas)", f"{len(df_opps)}", "Encontradas hoy", delta_color="normal")
    with col4:
        st.metric("Precisión IA (R²)", f"{stats.get('model_metrics', {}).get('r2_score', 0) * 100:.1f}%", "Alto nivel de confianza", delta_color="normal")


def render_opportunities_tab(df: pd.DataFrame, df_opps: pd.DataFrame):
    """Renderiza la pestaña de Oportunidades vs Mercado General."""
    st.markdown("### :material/location_on: Oportunidades vs Mercado General")
    st.caption("Las propiedades marcadas con diamantes verdes representan oportunidades matemáticas detectadas por nuestro algoritmo, encontrándose subvaloradas respecto al mercado general.")
    
    fig_map = go.Figure()
    
    # Mercado regular
    df_regular = df[~df['es_oportunidad']]
    fig_map.add_trace(go.Scatter(
        x=df_regular['longitud'], y=df_regular['latitud'], mode='markers',
        marker=dict(size=8, color='#475569', opacity=0.4),
        name="Mercado General"
    ))
    
    # Oportunidades
    if not df_opps.empty:
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


def render_factors_tab(stats: dict):
    """Renderiza la pestaña sobre factores de importancia en el precio."""
    st.markdown("### :material/bar_chart: ¿Qué es lo que verdaderamente influye en el precio?")
    st.caption("Pesos calculados por nuestro modelo de Inteligencia Artificial que explican qué características aumentan o disminuyen el valor de una propiedad.")
    
    coefs = stats.get('feature_importance', {})
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


def render_common_preferences_tab(df: pd.DataFrame):
    """Renderiza la pestaña de Preferencias de Mercado Más Comunes."""
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


def render_rare_preferences_tab(df: pd.DataFrame):
    """Renderiza la pestaña de Preferencias de Mercado Menos Comunes."""
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


def render_economic_analysis_tab(df: pd.DataFrame, stats: dict):
    """Renderiza la pestaña de Análisis Económico de Preferencias."""
    st.markdown("### :material/price_change: Análisis Económico de Preferencias")
    st.caption("Descubre cuáles preferencias encarecen o abaratan más una propiedad según nuestro análisis.")
    
    coefs = stats.get('feature_importance', {})
    mas_caras = sorted(coefs.items(), key=lambda x: x[1], reverse=True)[:2]
    mas_baratas = sorted(coefs.items(), key=lambda x: x[1])[:2]
    
    format_names = {
        "area_m2": "Área (m²)",
        "habitaciones": "Nro. Habitaciones",
        "banos": "Nro. Baños",
        "distancia_centro_km": "Cercanía al Centro",
        "antiguedad_anos": "Antigüedad",
        "tiene_piscina": "Tiene Piscina"
    }
    
    n_cara = format_names.get(mas_caras[0][0], mas_caras[0][0]) if mas_caras else "Desconocido"
    v_cara = mas_caras[0][1] if mas_caras else 0
    n_barata = format_names.get(mas_baratas[0][0], mas_baratas[0][0]) if mas_baratas else "Desconocido"
    v_barata = mas_baratas[0][1] if mas_baratas else 0
    
    st.info(f"**💡 Insight Económico:** La preferencia que MÁS eleva el precio es **{n_cara}** (+${v_cara:,.0f} por unidad). La característica que MÁS abarata una propiedad es **{n_barata}** (${v_barata:,.0f} por unidad).")

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


def render_data_tab(df_opps: pd.DataFrame):
    """Renderiza la pestaña con los datos de las principales oportunidades."""
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


def render_history_tab(data_client, api_online: bool):
    """Renderiza la pestaña del historial de tasaciones guardadas."""
    st.markdown("### :material/history: Historial de Tasaciones")
    st.caption("Registro de todas las predicciones realizadas por los usuarios del sistema.")
    
    if not api_online:
        st.info("No hay conexión con el servidor de la API para recuperar el historial de tasaciones.")
        return

    try:
        preds = data_client.get_predictions()
        if preds:
            df_preds = pd.DataFrame(preds)
            df_preds['created_at'] = pd.to_datetime(df_preds['created_at'])
            df_preds['Valor Estimado'] = df_preds['predicted_price'].apply(lambda x: f"${x:,.0f}")
            df_preds['Margen Error'] = df_preds['margin_of_error'].apply(lambda x: f"±${x:,.0f}")
            df_preds['Usuario'] = df_preds['user_name'].fillna("Anónimo")
            
            col_filtro, _ = st.columns([1, 3])
            with col_filtro:
                filter_user = st.selectbox("Filtrar por usuario", ["Todos"] + list(df_preds['Usuario'].unique()))
            
            if filter_user != "Todos":
                df_preds = df_preds[df_preds['Usuario'] == filter_user]
            
            st.dataframe(
                df_preds[['created_at', 'Usuario', 'area_m2', 'habitaciones', 'banos', 'Valor Estimado', 'Margen Error']].rename(columns={
                    'created_at': 'Fecha',
                    'Usuario': 'Usuario',
                    'area_m2': 'Área (m²)',
                    'habitaciones': 'Hab.',
                    'banos': 'Baños',
                    'Valor Estimado': 'Valor Estimado',
                    'Margen Error': 'Margen Error'
                }),
                use_container_width=True,
                hide_index=True,
                height=400
            )
            
            st.markdown(f"**Total de predicciones registradas:** {len(df_preds)}")
        else:
            st.info("No hay predicciones registradas aún. Realiza una tasación desde el panel lateral.")
    except Exception:
        st.error("No se pudo cargar el historial de predicciones.")
