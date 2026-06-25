import streamlit as st


def inject_custom_css():
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
