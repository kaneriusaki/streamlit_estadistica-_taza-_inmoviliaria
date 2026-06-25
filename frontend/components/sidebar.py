import streamlit as st
from exceptions import UserAlreadyExistsError


def render_sidebar(data_client, api_online: bool):
    """Renderiza el panel lateral para estimación y gestión de usuario."""
    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>Tasador Inmobiliario</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #94a3b8;'>Introduce los datos de la propiedad para estimar su valor en el mercado.</p>", unsafe_allow_html=True)
        
        st.divider()

        # Indicador de estado de la conexión
        if not api_online:
            st.sidebar.warning("⚠️ Modo Offline (API Caída)")
        else:
            st.sidebar.success("🟢 Conector IA (REST API Activa)")

        st.divider()
        
        # --- Registro/Selección de usuario ---
        with st.expander(":material/person: Gestión de Usuario", expanded=st.session_state.user_id is None):
            try:
                users = data_client.get_users() if api_online else []
            except Exception:
                users = []
            
            user_options = {f"{u['nombre']} ({u['email']})": u['id'] for u in users}
            
            selected = "--- Nuevo usuario ---"
            if user_options:
                selected = st.selectbox("Seleccionar usuario", ["--- Nuevo usuario ---"] + list(user_options.keys()))
                if selected != "--- Nuevo usuario ---":
                    st.session_state.user_id = user_options[selected]
                    st.session_state.user_name = selected.split(" (")[0]
            
            if st.session_state.user_id is None or selected == "--- Nuevo usuario ---":
                col_nom, col_mail = st.columns(2)
                with col_nom:
                    new_nombre = st.text_input("Nombre", placeholder="Ej: Juan Pérez")
                with col_mail:
                    new_email = st.text_input("Email", placeholder="ej@correo.com")
                if st.button(":material/person_add: Registrarse", use_container_width=True):
                    if new_nombre and new_email:
                        if not api_online:
                            st.error("❌ No es posible registrar usuarios en modo offline.")
                        else:
                            try:
                                user_data = data_client.create_user(new_nombre, new_email)
                                st.session_state.user_id = user_data["id"]
                                st.session_state.user_name = user_data["nombre"]
                                st.rerun()
                            except UserAlreadyExistsError as e:
                                st.error(f"❌ {str(e)}")
                            except Exception as e:
                                st.error(f"❌ Error al registrar: {str(e)}")
                    else:
                        st.warning("Completa todos los campos")
        
        if st.session_state.user_id:
            st.info(f"👤 Usuario: **{st.session_state.user_name}**")
        
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
            if not api_online:
                st.error("❌ El servicio de cálculo no está disponible en modo offline.")
            else:
                with st.spinner("Analizando mercado..."):
                    try:
                        params = {
                            "area_m2": area_m2,
                            "habitaciones": habitaciones,
                            "banos": banos,
                            "distancia_centro_km": distancia,
                            "antiguedad_anos": antiguedad,
                            "tiene_piscina": piscina_val,
                        }
                        data = data_client.predict_and_save(params, st.session_state.user_id)
                        st.success(f"### Valor Estimado: ${data['predicted_price']:,.0f}\n\nMargen de Error: ±${data['margin_of_error']:,.0f}")
                    except Exception as e:
                        st.error(f"❌ Error al calcular tasación: {str(e)}")
