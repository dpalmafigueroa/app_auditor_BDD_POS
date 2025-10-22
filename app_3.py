# --- validador_app.py ---
# Versión Atlantia 1.9 para Streamlit (Corrige SyntaxError V11)

import streamlit as st
import pandas as pd
import locale
import io # Para leer los archivos subidos
import numpy as np # Para manejar tipos numéricos

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title="Validador Atlantia")

# --- CSS PERSONALIZADO ---
# (Mismo CSS de la versión anterior)
atlantia_css = """
<style>
    /* ... (pega aquí TODO el CSS de la versión anterior 1.8) ... */
     /* Importar fuentes Atlantia */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Hind:wght@400;500;600&display=swap');

    /* Variables de colores Atlantia (Fijos) */
    :root {
        --atlantia-violet: #6546C3;
        --atlantia-purple: #AA49CA;
        --atlantia-lemon: #77C014;
        --atlantia-turquoise: #04D1CD;
        --atlantia-white: #FFFFFF;
        --atlantia-green: #23B776;
        --atlantia-yellow: #FFB73B;
        --atlantia-orange: #FF9231;
        --atlantia-red: #E61252;
        /* Colores pastel para validación */
        --validation-correct-bg: #E8F5E9;
        --validation-correct-border: #4CAF50;
        --validation-correct-text: #1B5E20;
        --validation-incorrect-bg: #FFEBEE;
        --validation-incorrect-border: #F44336;
        --validation-incorrect-text: #B71C1C;
        --validation-info-bg: #E3F2FD;
        --validation-info-border: #2196F3;
        --validation-info-text: #0D47A1;
        --validation-error-bg: #FFF3E0;
        --validation-error-border: #FF9800;
        --validation-error-text: #E65100;

        /* --- Variables ADAPTATIVAS Claro/Oscuro --- */
        /* Tema Claro (Por defecto) */
        --text-color: #0E1117; /* Streamlit's default dark text */
        --text-color-subtle: #555;
        --bg-color: #FFFFFF;
        --secondary-bg-color: #F0F2F6; /* Streamlit's light secondary bg */
        --widget-bg: #FFFFFF;
        --input-border-color: #CCCCCC;
        --table-header-bg: #F0F2F6;
        --table-row-even-bg: #FFFFFF;
        --table-border-color: #E0E0E0;
    }

    /* Tema Oscuro (Sobrescribe variables) */
    html[data-theme="dark"] {
        --text-color: #FAFAFA; /* Streamlit's default light text */
        --text-color-subtle: #a0a0a0;
        --bg-color: #0E1117; /* Streamlit's dark bg */
        --secondary-bg-color: #1c202a; /* Darker secondary bg */
        --widget-bg: #262730; /* Streamlit's dark widget bg */
        --input-border-color: #555;
        --table-header-bg: #222733;
        --table-row-even-bg: #2a303e;
        --table-border-color: #444;

        /* Ajustar fondos pastel para mejor contraste en oscuro */
        --validation-correct-bg: #1c3d1e;
        --validation-incorrect-bg: #4d1f23;
        --validation-info-bg: #1a3a57;
        --validation-error-bg: #4d3a1e;
        /* Ajustar texto pastel si es necesario */
        --validation-correct-text: #b8f5b9;
        --validation-incorrect-text: #f7c5c7;
        --validation-info-text: #bce3ff;
        --validation-error-text: #ffe0b3;
    }

    /* Ocultar menú y footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Tipografía base (Usa variable adaptativa) */
    body, * {
        font-family: 'Hind', sans-serif;
        color: var(--text-color);
    }
    .stApp { background-color: var(--bg-color); }

    /* Títulos Atlantia (Color fijo) */
    h1, .main-title, h2, .section-title, h3, .subsection-title {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 700 !important;
        color: var(--atlantia-violet) !important;
    }
    h1, .main-title { font-size: 24pt !important; }
    h2, .section-title { font-size: 20pt !important; }
    h3, .subsection-title { font-size: 16pt !important; }

    /* Labels Atlantia (Color fijo) */
    .stSelectbox label, .stTextInput label, .stTextArea label, .stFileUploader label,
    .indicator-subtitle, .metric-label, .stMetric label, .stExpander summary {
        font-family: 'Hind', sans-serif !important;
        font-weight: 600 !important;
        font-size: 14pt !important;
        color: var(--atlantia-violet) !important;
    }

    /* Cuerpo de texto (Usa variable adaptativa) */
    p, .body-text, .stMarkdown, .stText, label, div[data-baseweb="select"] > div, .stAlert * {
        font-family: 'Hind', sans-serif !important;
        font-weight: 400 !important;
        font-size: 12pt !important;
        color: var(--text-color) !important;
    }
    .stExpander div[data-baseweb="block"] > div { color: var(--text-color) !important; }

    /* Botones */
    .stButton button { font-family: 'Hind', sans-serif !important; font-weight: 600 !important; font-size: 12pt !important; border-radius: 8px !important; }

    /* Inputs y Select (Adaptativo) */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    div[data-baseweb="select"] > div {
        border: 1px solid var(--input-border-color) !important;
        background-color: var(--widget-bg) !important;
        color: var(--text-color) !important;
        border-radius: 8px !important;
    }
     .stTextInput > div > div > input:focus,
     .stTextArea > div > div > textarea:focus {
          border-color: var(--atlantia-violet) !important;
          box-shadow: 0 0 0 2px rgba(101, 70, 195, 0.3) !important;
     }

    /* File Uploader (Adaptativo) */
    .stFileUploader > div > div {
         border: 2px dashed var(--atlantia-violet) !important;
         background-color: var(--secondary-bg-color) !important;
         border-radius: 10px !important;
     }
     .stFileUploader label span {
         color: var(--text-color) !important;
     }

    /* Expander (Adaptativo) */
    .streamlit-expanderHeader {
         background-color: var(--secondary-bg-color) !important;
         border: 1px solid var(--input-border-color) !important;
         border-radius: 8px !important;
    }
    .streamlit-expanderHeader p {
         color: var(--atlantia-violet) !important;
    }

    /* Métricas (Adaptativo) */
    .stMetric {
         background-color: var(--widget-bg);
         border: 1px solid var(--input-border-color);
         border-radius: 8px;
         padding: 10px 15px;
     }
     .stMetric > label { color: var(--atlantia-violet) !important; }
     .stMetric > div[data-testid="stMetricValue"] { color: var(--text-color) !important; }
     .stMetric > div[data-testid="stMetricDelta"] { color: var(--text-color-subtle) !important; }

    /* --- ESTILOS DE VALIDACIÓN (Adaptativos) --- */
    .validation-box {
        border: 1px solid var(--input-border-color);
        border-left-width: 5px !important;
        border-radius: 8px; padding: 16px; margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05); line-height: 1.6;
    }
    .validation-box h3 { border-bottom: 1px solid var(--input-border-color); color: var(--atlantia-violet); } /* Título principal violeta */
    .validation-box h3.sub-heading { color: var(--text-color-subtle); border-bottom-style: dotted; }

    /* Estados */
    .status-correcto { background-color: var(--validation-correct-bg); border-left-color: var(--validation-correct-border); }
    .status-correcto h3, .status-correcto span, .status-correcto p, .status-correcto li { color: var(--validation-correct-text) !important; }
    .status-correcto-inline { color: var(--validation-correct-text) !important; font-weight: bold; }

    .status-incorrecto { background-color: var(--validation-incorrect-bg); border-left-color: var(--validation-incorrect-border); }
    .status-incorrecto h3, .status-incorrecto span, .status-incorrecto p, .status-incorrecto li, .status-incorrecto .df-style th, .status-incorrecto .df-style td { color: var(--validation-incorrect-text) !important; }
    .status-incorrecto-inline { color: var(--validation-incorrect-text) !important; font-weight: bold; }

    .status-info { background-color: var(--validation-info-bg); border-left-color: var(--validation-info-border); }
    .status-info h3, .status-info span, .status-info p, .status-info li, .status-info .df-style th, .status-info .df-style td { color: var(--validation-info-text) !important; }

    .status-error { background-color: var(--validation-error-bg); border-left-color: var(--validation-error-border); }
    .status-error h3, .status-error span, .status-error p, .status-error li, .status-error .df-style th, .status-error .df-style td { color: var(--validation-error-text) !important; }
    .status-error-inline { color: var(--validation-error-text) !important; font-weight: bold; }

     /* Tablas dentro de validación */
    .df-style { border-collapse: collapse; width: 95%; margin: 10px auto; font-size: 0.9em; }
    .df-style th, .df-style td { border: 1px solid var(--table-border-color); padding: 6px; color: var(--text-color) !important; }
    .df-style th { background-color: var(--table-header-bg); text-align: left; font-weight: bold; }
    .df-style tr:nth-child(even) { background-color: var(--table-row-even-bg); }
    /* Override para tablas dentro de cajas de estado */
    .status-incorrecto .df-style th, .status-incorrecto .df-style td { color: var(--validation-incorrect-text) !important; border-color: rgba(183, 28, 28, 0.3); }
    .status-incorrecto .df-style th { background-color: rgba(183, 28, 28, 0.1); }
    .status-error .df-style th, .status-error .df-style td { color: var(--validation-error-text) !important; border-color: rgba(230, 81, 0, 0.3); }
    .status-error .df-style th { background-color: rgba(230, 81, 0, 0.1); }
    .status-info .df-style th, .status-info .df-style td { color: var(--validation-info-text) !important; border-color: rgba(13, 71, 161, 0.3); }
    .status-info .df-style th { background-color: rgba(13, 71, 161, 0.1); }

    /* Resumen Lista */
    .summary-list ul { list-style-type: none; padding-left: 0; }
    .summary-list li { padding: 5px 0; border-bottom: 1px dotted var(--input-border-color); }
    .summary-list li strong { color: var(--atlantia-violet); }

    /* Header principal */
    .main-header-container { margin-bottom: 2rem; }
    .main-header { text-align: center; padding: 1rem 0; background: linear-gradient(135deg, var(--atlantia-violet) 0%, var(--atlantia-purple) 100%); border-radius: 15px; color: white; }
    .main-header h1 { color: white !important; font-family: 'Poppins', sans-serif !important; font-weight: 700 !important; font-size: 24pt !important; margin-bottom: 0.2rem; }
    .main-header .subtitle { color: rgba(255, 255, 255, 0.9) !important; font-family: 'Poppins', sans-serif !important; font-weight: 500 !important; font-size: 14pt !important; margin-top: 0; }
    .atlantia-logo { width: 40px; height: auto; vertical-align: middle; margin-right: 0.5rem; }

</style>
"""
st.markdown(atlantia_css, unsafe_allow_html=True)

# --- HEADER PERSONALIZADO ---
# ... (mismo HTML header) ...
st.markdown('<div class="main-header-container">', unsafe_allow_html=True)
st.markdown("""<div class="main-header"><svg class="atlantia-logo" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="atlantiaGradient" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#04D1CD"/><stop offset="50%" style="stop-color:#6546C3"/><stop offset="100%" style="stop-color:#AA49CA"/></linearGradient></defs><path d="M20,80 L50,20 L80,80 L65,80 L50,50 L35,80 Z" fill="url(#atlantiaGradient)" stroke="white" stroke-width="2"/></svg><h1 style="display: inline-block; vertical-align: middle;">Validador de Bases</h1><div class="subtitle">Powered by Atlantia</div></div>""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- INSTRUCCIONES ---
# ... (mismas instrucciones V1.8) ...
st.markdown("## Instrucciones")
st.markdown("""1.  **Selecciona el país** para el cual se aplicarán las reglas geográficas y de volumetría.\n2.  **Carga los archivos Excel** correspondientes a la base numérica y textual.""")
st.markdown("### Evaluaciones Realizadas:")
st.markdown("""* **Tamaño:** Compara filas y columnas.\n* **Orden de IDs:** Verifica `Unico` vs `[auth]`.\n* **Finalización (lastpage):** Revisa unicidad.\n* **Periodo de Campo:** Muestra fechas de `startdate`.\n* **Agrupaciones:** Edad vs `[age]`, `NSE` vs `NSE2`, Geografía (Región/Ciudad).\n* **Origen/Proveedor:** Conteo por proveedor.\n* **Nulos (Numérica):** Busca vacíos en `NSE`, `gender`, `AGErange`, `Region`.\n* **Abiertas ('Menciona'):** Lista respuestas.\n* **Ponderador (Numérica):** Compara suma `Ponderador` vs total filas.\n* **Suma Ponderador x Demo:** Suma `Ponderador` por `NSE`, `gender`, `AGErange`, `Region`.\n* **Volumetría (Numérica):** Valida columnas contra umbrales definidos por país.""")
st.divider()


# --- CONFIGURACIÓN DE REGLAS ---
# ... (mismos diccionarios CLASIFICACIONES_POR_PAIS y THRESHOLDS_POR_PAIS que V1.8) ...
CLASIFICACIONES_POR_PAIS = {
    'Panamá': {'Centro': ['Aguadulce', 'Antón', 'La Pintada', 'Natá', 'Olá', 'Penonomé','Chagres', 'Ciudad de Colón', 'Colón', 'Donoso', 'Portobelo','Resto del Distrito', 'Santa Isabel', 'La Chorrera', 'Arraiján','Capira', 'Chame', 'San Carlos'],'Metro': ['Panamá', 'San Miguelito', 'Balboa', 'Chepo', 'Chimán', 'Taboga', 'Chepigana', 'Pinogana'],'Oeste': ['Alanje', 'Barú', 'Boquerón', 'Boquete', 'Bugaba', 'David', 'Dolega', 'Guacala', 'Remedios', 'Renacimiento', 'San Félix', 'San Lorenzo', 'Tolé', 'Bocas del Toro', 'Changuinola', 'Chiriquí Grande', 'Chitré', 'Las Minas', 'Los Pozos', 'Ocú', 'Parita', 'Pesé', 'Santa María', 'Guararé', 'Las Tablas', 'Los Santos', 'Macaracas', 'Pedasí', 'Pocrí', 'Tonosí', 'Atalaya', 'Calobre', 'Cañazas', 'La Mesa', 'Las Palmas', 'Mariato', 'Montijo', 'Río de Jesús', 'San Francisco', 'Santa Fé', 'Santiago', 'Soná']},
    'México': {'Central/Bajio': ['CDMX + AM', 'Estado de México', 'Guanajuato', 'Hidalgo','Morelos', 'Puebla', 'Querétaro', 'Tlaxcala'],'Norte': ['Baja California Norte', 'Baja California Sur', 'Chihuahua', 'Coahuila','Durango', 'Nuevo León', 'Sinaloa', 'Sonora', 'Tamaulipas'],'Occidente/Pacifico': ['Aguascalientes', 'Colima', 'Guerrero', 'Jalisco', 'Michoacan','Nayarit', 'San Luis Potosí', 'Zacatecas'],'Sureste': ['Campeche', 'Chiapas', 'Oaxaca', 'Quintana Roo', 'Tabasco','Veracruz', 'Yucatán']},
    'Colombia': {}, 'Ecuador': {}, 'Perú': {}, 'R. Dominicana': {}, 'Honduras': {},
    'El Salvador': {}, 'Costa Rica': {}, 'Puerto Rico': {}, 'Guatemala': {}, 'Colombia Minors': {}
}
THRESHOLDS_POR_PAIS = {
    'México': [{'col': 'Total_consumo', 'cond': 'mayor_a', 'lim': 11000}, {'col': 'Total_consumo', 'cond': 'igual_a', 'lim': 0},{'col': 'Beer', 'cond': 'mayor_a', 'lim': 7000},{'col': 'Wine', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Spirits', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Other alc', 'cond': 'mayor_a', 'lim': 1400},{'col': 'CSDs', 'cond': 'mayor_a', 'lim': 5000},{'col': 'Energy drinks', 'cond': 'mayor_a', 'lim': 1400}],
    'Colombia': [{'col': 'Total_consumo', 'cond': 'mayor_a', 'lim': 11000}, {'col': 'Total_consumo', 'cond': 'igual_a', 'lim': 0},{'col': 'Beer', 'cond': 'mayor_a', 'lim': 7000},{'col': 'Wine', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Spirits', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Other alc', 'cond': 'mayor_a', 'lim': 1400},{'col': 'CSDs', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Energy drinks', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Malts', 'cond': 'mayor_a', 'lim': 2000}],
    'Ecuador': [{'col': 'Total_consumo', 'cond': 'mayor_a', 'lim': 11000}, {'col': 'Total_consumo', 'cond': 'igual_a', 'lim': 0},{'col': 'Beer', 'cond': 'mayor_a', 'lim': 7000},{'col': 'Wine', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Spirits', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Other alc', 'cond': 'mayor_a', 'lim': 1400},{'col': 'CSDs', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Energy drinks', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Malts', 'cond': 'mayor_a', 'lim': 2000}],
    'Perú': [{'col': 'Total_consumo', 'cond': 'mayor_a', 'lim': 11000}, {'col': 'Total_consumo', 'cond': 'igual_a', 'lim': 0},{'col': 'Beer', 'cond': 'mayor_a', 'lim': 7000},{'col': 'Wine', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Spirits', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Other alc', 'cond': 'mayor_a', 'lim': 1400},{'col': 'CSDs', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Energy drinks', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Malts', 'cond': 'mayor_a', 'lim': 2000}],
    'R. Dominicana': [{'col': 'Total_consumo', 'cond': 'mayor_a', 'lim': 11000},{'col': 'Total_consumo', 'cond': 'igual_a', 'lim': 0},{'col': 'Beer', 'cond': 'mayor_a', 'lim': 7000},{'col': 'Wine', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Ron', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Whisky', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Spirits', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Other alc', 'cond': 'mayor_a', 'lim': 1400},{'col': 'CSDs', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Energy drinks', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Malts', 'cond': 'mayor_a', 'lim': 2000}],
    'Honduras': [{'col': 'Total_consumo', 'cond': 'mayor_a', 'lim': 11000},{'col': 'Total_consumo', 'cond': 'igual_a', 'lim': 0},{'col': 'Beer', 'cond': 'mayor_a', 'lim': 7000},{'col': 'Wine', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Spirits', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Other alc', 'cond': 'mayor_a', 'lim': 1400},{'col': 'CSDs', 'cond': 'mayor_a', 'lim': 5000},{'col': 'Energy drinks', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Malts', 'cond': 'mayor_a', 'lim': 2000}],
    'El Salvador': [{'col': 'Total_consumo', 'cond': 'mayor_a', 'lim': 11000},{'col': 'Total_consumo', 'cond': 'igual_a', 'lim': 0},{'col': 'Beer', 'cond': 'mayor_a', 'lim': 7000},{'col': 'Wine', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Spirits', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Other alc', 'cond': 'mayor_a', 'lim': 1400},{'col': 'CSDs', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Energy drinks', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Malts', 'cond': 'mayor_a', 'lim': 2000}],
    'Costa Rica': [{'col': 'Total_consumo', 'cond': 'mayor_a', 'lim': 11000},{'col': 'Total_consumo', 'cond': 'igual_a', 'lim': 0},{'col': 'Beer', 'cond': 'mayor_a', 'lim': 7000},{'col': 'Wine', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Spirits', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Other alc', 'cond': 'mayor_a', 'lim': 1400},{'col': 'CSDs', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Energy drinks', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Malts', 'cond': 'mayor_a', 'lim': 2000}],
    'Puerto Rico': [{'col': 'Total_consumo', 'cond': 'mayor_a', 'lim': 11000},{'col': 'Total_consumo', 'cond': 'igual_a', 'lim': 0},{'col': 'Beer', 'cond': 'mayor_a', 'lim': 7000},{'col': 'Wine', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Spirits', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Other alc', 'cond': 'mayor_a', 'lim': 1400},{'col': 'CSDs', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Energy drinks', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Malts', 'cond': 'mayor_a', 'lim': 2000}],
    'Panamá': [{'col': 'Total_consumo', 'cond': 'mayor_a', 'lim': 11000},{'col': 'Total_consumo', 'cond': 'igual_a', 'lim': 0},{'col': 'Beer', 'cond': 'mayor_a', 'lim': 7000},{'col': 'Wine', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Spirits', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Other alc', 'cond': 'mayor_a', 'lim': 1400},{'col': 'CSDs', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Energy drinks', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Malts', 'cond': 'mayor_a', 'lim': 2000}],
    'Guatemala': [{'col': 'Total_consumo', 'cond': 'mayor_a', 'lim': 11000},{'col': 'Total_consumo', 'cond': 'igual_a', 'lim': 0},{'col': 'Beer', 'cond': 'mayor_a', 'lim': 7000},{'col': 'Wine', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Spirits', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Other alc', 'cond': 'mayor_a', 'lim': 1400},{'col': 'CSDs', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Energy drinks', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Malts', 'cond': 'mayor_a', 'lim': 2000}],
    'Colombia Minors': [{'col': 'Total_consumo', 'cond': 'mayor_a', 'lim': 11000},{'col': 'Total_consumo', 'cond': 'igual_a', 'lim': 0},{'col': 'Beer', 'cond': 'mayor_a', 'lim': 7000},{'col': 'Wine', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Spirits', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Other alc', 'cond': 'mayor_a', 'lim': 1400},{'col': 'CSDs', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Energy drinks', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Malts', 'cond': 'mayor_a', 'lim': 2000}],
}
paises_disponibles = list(CLASIFICACIONES_POR_PAIS.keys())

# --- SELECCIÓN DE PAÍS Y CARGA DE ARCHIVOS ---
# ... (igual que antes) ...
col_pais, col_vacia = st.columns([1, 2])
with col_pais: pais_seleccionado_display = st.selectbox("Selecciona el País:", paises_disponibles, key="select_pais")
st.markdown("### Carga de Archivos Excel")
col1_up, col2_up = st.columns(2)
with col1_up: uploaded_file_num = st.file_uploader("Carga el archivo Numérico", type=["xlsx"], key="num")
with col2_up: uploaded_file_txt = st.file_uploader("Carga el archivo Textual", type=["xlsx"], key="txt")

# --- LÓGICA DE VALIDACIÓN ---
if uploaded_file_num is not None and uploaded_file_txt is not None:
    # ... (carga, optimización, V1-V10 igual que antes) ...
    st.info(f"Archivos cargados. Iniciando validación para **{pais_seleccionado_display}**...")
    st.divider()
    pais_clave_interna = pais_seleccionado_display
    validation_results = []
    try:
        df_numerico_full = pd.read_excel(io.BytesIO(uploaded_file_num.getvalue()))
        df_textual_full = pd.read_excel(io.BytesIO(uploaded_file_txt.getvalue()))
    except Exception as e: st.error(f"Error al leer archivos: {e}"); st.stop()
    num_cols_base = ['Unico', 'lastpage', 'lastpage_Parte2']; txt_cols = ['[auth]', 'startdate', "Por favor, selecciona el rango de edad en el que te encuentras:", '[age]', 'NSE', 'NSE2', 'Region 1 (Centro/Metro/Oeste)', 'CIUDAD', 'Origen', 'Proveedor']
    num_cols_extra = ['Ponderador', 'NSE', 'gender', 'AGErange', 'Region'] # Columnas para V7, V9, V10, V11
    num_cols_extra.extend([rule['col'] for rule in THRESHOLDS_POR_PAIS.get(pais_clave_interna, [])]) # Añadir cols de umbrales
    num_cols = num_cols_base + [c for c in num_cols_extra if c in df_numerico_full.columns and c not in num_cols_base] # Únicas y existentes
    num_ex = [c for c in num_cols_base if c in df_numerico_full.columns]; txt_ex = [c for c in txt_cols if c in df_textual_full.columns]
    try:
        df_numerico = df_numerico_full[num_ex] # Optimizado solo para V2, V3
        df_textual = df_textual_full[txt_ex]   # Optimizado para V4, V5, V6, V8
    except KeyError as e: st.error(f"Columna base esencial {e} no encontrada."); st.stop()


    # --- VALIDACIONES (V1-V11) ---

    # V1: Tamaño (Usa _full)
    key_v1 = "Tamaño de las Bases"; content_v1 = ""; status_v1 = "Correcto"
    fn, cn = df_numerico_full.shape; ft, ct = df_textual_full.shape
    content_v1 += f"- Num: {fn} filas x {cn} columnas<br>- Txt: {ft} filas x {ct} columnas<br><br><b>Comparación:</b><br>"
    if fn == ft and cn == ct: content_v1 += "<span class='status-correcto-inline'>[Correcto]</span> Coinciden."
    else: status_v1 = "Incorrecto"; content_v1 += "<span class='status-incorrecto-inline'>[Incorrecto]</span> Diferentes.<br>";
    if fn != ft: content_v1 += "- Filas.<br>"
    if cn != ct: content_v1 += "- Columnas.<br>"
    validation_results.append({'key': key_v1, 'status': status_v1, 'content': content_v1})

    # V2: Orden IDs (Usa optimizados)
    key_v2 = "Orden de Códigos Únicos"; content_v2 = ""; status_v2 = "Correcto"; col_num = 'Unico'; col_txt = '[auth]'
    try:
        if col_num not in df_numerico.columns: raise KeyError(f"{col_num} (Numérica)")
        if col_txt not in df_textual.columns: raise KeyError(f"{col_txt} (Textual)")
        cod_num = df_numerico[col_num]; cod_txt = df_textual[col_txt]
        if len(cod_num) != len(cod_txt): status_v2 = "Incorrecto"; content_v2 += f"<span class='status-incorrecto-inline'>[Incorrecto]</span> Filas no coinciden.<br>Num:{len(cod_num)}, Txt:{len(cod_txt)}<br>(Error V1)"
        elif cod_num.equals(cod_txt): content_v2 += f"<span class='status-correcto-inline'>[Correcto]</span> Orden idéntico."
        else:
            status_v2 = "Incorrecto"; content_v2 += f"<span class='status-incorrecto-inline'>[Incorrecto]</span> Códigos/orden no coinciden.<br>"; diff = cod_num != cod_txt
            diff_data = cod_txt.loc[diff]; rep = pd.DataFrame({'Fila': diff_data.index + 2, f'{col_txt}': diff_data.values})
            content_v2 += f"Primeras 5 (Fila y {col_txt}):<br>" + rep.head().to_html(classes='df-style', index=False)
    except KeyError as e: status_v2 = "Error"; content_v2 += f"<span class='status-error-inline'>[ERROR]</span> Col {e} no encontrada."
    validation_results.append({'key': key_v2, 'status': status_v2, 'content': content_v2})

    # V3: lastpage (Usa optimizado)
    key_v3 = "lastpage y lastpage_Parte2"; content_v3 = ""; status_v3 = "Correcto"; cols_v3 = ['lastpage', 'lastpage_Parte2']
    for col in cols_v3:
        content_v3 += f"<br><b>'{col}':</b><br>";
        if col not in df_numerico.columns: status_v3 = "Error"; content_v3 += f"<span class='status-error-inline'>[ERROR]</span> No encontrada.<br>"; continue
        vals = df_numerico[col].dropna().unique()
        if len(vals) <= 1: content_v3 += f"<span class='status-correcto-inline'>[Correcto]</span> Único valor.<br>"
        else: status_v3 = "Incorrecto"; vals_str = ", ".join(map(str, vals)); content_v3 += f"<span class='status-incorrecto-inline'>[Incorrecto]</span> Múltiples: {vals_str}<br>"
    validation_results.append({'key': key_v3, 'status': status_v3, 'content': content_v3})

    # V4: Periodo Campo (Usa optimizado)
    key_v4 = "Periodo Campo ('startdate')"; content_v4 = ""; status_v4 = "Info"; col_fecha = 'startdate'
    locale_usado = ''; formato_fecha = '%d/%b/%Y %H:%M'
    try:
        try: locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8'); locale_usado = 'es_ES'; formato_fecha = '%d de %B de %Y, %I:%M %p'
        except:
            try: locale.setlocale(locale.LC_TIME, 'es'); locale_usado = 'es'; formato_fecha = '%d de %B de %Y, %I:%M %p'
            except: locale.setlocale(locale.LC_TIME, ''); locale_usado = 'Sistema'
        if col_fecha not in df_textual.columns: raise KeyError(f"'{col_fecha}' ausente.")
        fechas = pd.to_datetime(df_textual[col_fecha], dayfirst=True, errors='coerce').dropna()
        if not fechas.empty: f_min, f_max = fechas.min(), fechas.max(); content_v4 += f"<b>Periodo ({locale_usado}):</b><br> - Inicio: {f_min.strftime(formato_fecha)}<br> - Fin: {f_max.strftime(formato_fecha)}<br>"
        else: status_v4 = "Error"; content_v4 += "<span class='status-error-inline'>[ERROR]</span> No hay fechas.<br>"
    except KeyError as e: status_v4 = "Error"; content_v4 += f"<span class='status-error-inline'>[ERROR]</span> Col {e}.<br>"
    except Exception as e_loc: status_v4 = "Error"; content_v4 += f"<span class='status-error-inline'>[ERROR Locale]</span> {e_loc}.<br>"
    validation_results.append({'key': key_v4, 'status': status_v4, 'content': content_v4})

    # V5: Agrupaciones (Usa optimizado Textual)
    key_v5 = "Agrupaciones"; content_v5 = ""; status_v5 = "Correcto"
    # 5.1 Edad
    content_v5 += "<h3>5.1: Edad vs [age]</h3>"; col_g_edad = "Por favor, selecciona el rango de edad en el que te encuentras:"; col_d_edad = '[age]'
    try:
        if not all(c in df_textual.columns for c in [col_g_edad, col_d_edad]): raise KeyError("Edad/[age]")
        rep_edad = df_textual.groupby(col_g_edad)[col_d_edad].agg(['count', 'min', 'max']); rep_edad.columns = ['Total', 'Min', 'Max']
        content_v5 += rep_edad.to_html(classes='df-style')
    except KeyError as e: status_v5 = "Error"; content_v5 += f"<span class='status-error-inline'>[ERROR]</span> {e}<br>"
    content_v5 += "<hr style='border-top: 1px dotted #ccc;'>"
    # 5.2 NSE
    content_v5 += "<h3>5.2: NSE vs NSE2</h3>"; col_g_nse = 'NSE'; col_d_nse = 'NSE2'
    try:
        if not all(c in df_textual.columns for c in [col_g_nse, col_d_nse]): raise KeyError("NSE/NSE2")
        rep_nse = pd.crosstab(df_textual[col_g_nse], df_textual[col_d_nse])
        content_v5 += "Verifica consistencia:<br>" + rep_nse.to_html(classes='df-style')
    except KeyError as e:
        if status_v5 != "Error": status_v5 = "Error"; content_v5 += f"<span class='status-error-inline'>[ERROR]</span> {e}<br>"
    content_v5 += "<hr style='border-top: 1px dotted #ccc;'>"
    # 5.3 Geografía (AJUSTADO PARA PAÍSES SIN REGLAS)
    content_v5 += f"<h3>5.3: Geografía ({pais_seleccionado_display})</h3>"; status_v5_3 = "Correcto"
    try:
        clasif = CLASIFICACIONES_POR_PAIS.get(pais_clave_interna);
        if not clasif: # Si es None o {}
            status_v5_3 = "Info"; content_v5 += f"<span class='status-info'>[INFO]</span> No hay reglas geográficas definidas para {pais_seleccionado_display}."
        else:
            col_reg = 'Region 1 (Centro/Metro/Oeste)'; col_ciu = 'CIUDAD'
            if not all(c in df_textual.columns for c in [col_reg, col_ciu]): raise KeyError(f"Columnas Región/Ciudad no encontradas.")
            err_reg = [];
            for idx, row in df_textual.iterrows(): # Usar df_textual optimizado aquí está bien
                reg, ciu = row[col_reg], row[col_ciu]
                if pd.isna(reg) or pd.isna(ciu): continue
                if reg in clasif:
                    if ciu not in clasif[reg]: err_reg.append({'Fila': idx + 2, 'Region': reg, 'Ciudad': ciu, 'Error': f"'{ciu}' no en '{reg}'"})
                else: err_reg.append({'Fila': idx + 2, 'Region': reg, 'Ciudad': ciu, 'Error': f"Región '{reg}' no válida"})
            if not err_reg: content_v5 += f"<span class='status-correcto-inline'>[Correcto]</span> Consistente."
            else: status_v5_3 = "Incorrecto"; content_v5 += f"<span class='status-incorrecto-inline'>[Incorrecto]</span> {len(err_reg)} inconsistencias.<br>"; df_err = pd.DataFrame(err_reg); content_v5 += "Primeras 5:<br>" + df_err.head().to_html(classes='df-style', index=False)
    except (KeyError, ValueError) as e: status_v5_3 = "Error"; content_v5 += f"<span class='status-error-inline'>[ERROR]</span> {e}<br>"
    # Ajuste estado general
    if status_v5 == "Correcto" and status_v5_3 not in ["Correcto", "Info"]: status_v5 = status_v5_3
    elif status_v5_3 == "Error": status_v5 = "Error"
    validation_results.append({'key': key_v5, 'status': status_v5, 'content': content_v5})

    # V6: Origen/Proveedor (Usa optimizado Textual)
    key_v6 = "Origen/Proveedor"; content_v6 = ""; status_v6 = "Info"; prov_cols = ['Origen', 'Proveedor']
    prov_col = next((col for col in prov_cols if col in df_textual.columns), None)
    if prov_col:
        content_v6 += f"<b>'{prov_col}':</b><br>";
        try: cnt = df_textual[prov_col].value_counts(dropna=False).reset_index(); cnt.columns = [prov_col, 'Conteo']; content_v6 += cnt.to_html(classes='df-style', index=False)
        except Exception as e: status_v6 = "Error"; content_v6 += f"<span class='status-error-inline'>[ERROR]</span> {e}<br>"
    else: content_v6 += f"[INFO] No encontrada."
    validation_results.append({'key': key_v6, 'status': status_v6, 'content': content_v6})

    # V7: Nulos Base Numérica (Usa _full)
    key_v7 = "Nulos Base Numérica"; content_v7 = ""; status_v7 = "Correcto"; id_unico = 'Unico'; cols_v7 = ['NSE', 'gender', 'AGErange', 'Region']
    nulos_det = []; no_enc = []; id_ok = id_unico in df_numerico_full.columns
    if not id_ok: content_v7 += f"<span class='status-error-inline'>[WARN]</span> Col '{id_unico}' no encontrada.<br>"
    for col in cols_v7:
        if col not in df_numerico_full.columns: no_enc.append(col); continue
        nulas = df_numerico_full[df_numerico_full[col].isnull()]; cant = len(nulas)
        if cant > 0: ids = nulas[id_unico].tolist() if id_ok else []; nulos_det.append({'col': col, 'cant': cant, 'ids': ids})
    if no_enc: status_v7 = "Error"; content_v7 += f"<span class='status-error-inline'>[ERROR]</span> No encontradas: {', '.join(no_enc)}<br>"
    if nulos_det:
        if status_v7 == "Correcto": status_v7 = "Incorrecto"
        content_v7 += f"<span class='status-incorrecto-inline'>[Incorrecto]</span> Nulos:<br><ul>"
        for item in nulos_det:
            content_v7 += f"<li><b>{item['col']}</b>: {item['cant']}";
            if item['ids']: ids_str = ", ".join(map(str, item['ids'])); content_v7 += f"<br>- IDs: <b>{ids_str}</b>"
            content_v7 += "</li>"
        content_v7 += "</ul>"
    if status_v7 == "Correcto": content_v7 = f"<span class='status-correcto-inline'>[Correcto]</span> Columnas OK."
    validation_results.append({'key': key_v7, 'status': status_v7, 'content': content_v7})

    # V8: Abiertas ('Menciona') (Usa _full)
    key_v8 = "Abiertas ('Menciona')"; content_v8 = ""; status_v8 = "Info"
    try:
        id_auth = '[auth]';
        if id_auth not in df_textual_full.columns: raise KeyError(f"'{id_auth}' ausente.")
        cols_m = [c for c in df_textual_full.columns if "menciona" in str(c).lower() and "mencionaste" not in str(c).lower()]; total_p = len(cols_m)
        if not cols_m: content_v8 = "No hay columnas 'menciona'."
        else:
            melted = df_textual_full[[id_auth] + cols_m].melt(id_vars=[id_auth], var_name='Pregunta', value_name='Respuesta')
            final_abiertas = melted.dropna(subset=['Respuesta'])
            if final_abiertas.empty: content_v8 = f"{total_p} columnas, sin respuestas."
            else:
                total_r = len(final_abiertas); content_v8 += f"<b>{total_p}</b> cols, <b>{total_r}</b> respuestas.<br><br>";
                df_disp = final_abiertas[[id_auth, 'Respuesta']]
                if total_r > 500: content_v8 += f"(Primeras 500)<br>"; df_disp = df_disp.head(500)
                df_disp.columns = [id_auth, 'Respuesta']
                content_v8 += df_disp.to_html(classes='df-style', index=False)
    except Exception as e: status_v8 = "Error"; content_v8 += f"<span class='status-error-inline'>[ERROR]</span> {e}<br>"
    validation_results.append({'key': key_v8, 'status': status_v8, 'content': content_v8})

    # V9: Ponderador vs Total Filas (Usa _full)
    key_v9 = "Ponderador vs Total Filas"; content_v9 = ""; status_v9 = "Correcto"; col_pond = 'Ponderador'
    try:
        if col_pond not in df_numerico_full.columns: raise KeyError(f"Col '{col_pond}' no encontrada.")
        suma_ponderador = pd.to_numeric(df_numerico_full[col_pond], errors='coerce').sum()
        total_filas = df_numerico_full.shape[0]
        suma_str = f"{suma_ponderador:,.2f}" if suma_ponderador != int(suma_ponderador) else f"{int(suma_ponderador):,}"
        total_str = f"{total_filas:,}"
        content_v9 += f"- Suma '{col_pond}': {suma_str}<br>- Total Filas: {total_str}<br><br>"
        if np.isclose(suma_ponderador, total_filas, atol=1e-5): content_v9 += "<span class='status-correcto-inline'>[Correcto]</span> Coinciden."
        else: status_v9 = "Incorrecto"; content_v9 += "<span class='status-incorrecto-inline'>[Incorrecto]</span> NO coinciden."
    except KeyError as e: status_v9 = "Error"; content_v9 += f"<span class='status-error-inline'>[ERROR]</span> {e}"
    except Exception as e: status_v9 = "Error"; content_v9 += f"<span class='status-error-inline'>[ERROR]</span> al sumar '{col_pond}': {e}"
    validation_results.append({'key': key_v9, 'status': status_v9, 'content': content_v9})

    # V10: Suma Ponderador por Demo (Usa _full)
    key_v10 = "Suma Ponderador por Demográfico"; content_v10 = ""; status_v10 = "Info"; col_pond = 'Ponderador'
    cols_demo = ['NSE', 'gender', 'AGErange', 'Region']
    ponderador_numerico = None; missing_cols = []
    all_results = []
    if col_pond not in df_numerico_full.columns: missing_cols.append(col_pond)
    for d_col in cols_demo:
        if d_col not in df_numerico_full.columns: missing_cols.append(d_col)
    if missing_cols: status_v10 = "Error"; content_v10 = f"<span class='status-error-inline'>[ERROR]</span> Faltan: {', '.join(missing_cols)}"
    else:
        try:
            ponderador_numerico = pd.to_numeric(df_numerico_full[col_pond], errors='coerce')
            if ponderador_numerico.isnull().any(): content_v10 += f"<span class='status-error-inline'>[WARN]</span> '{col_pond}' con no numéricos.<br>"
            temp_df = df_numerico_full.copy(); temp_df['Ponderador_Num'] = ponderador_numerico
            for dem_col in cols_demo:
                suma_grupo = temp_df.groupby(dem_col, dropna=False)['Ponderador_Num'].sum().reset_index()
                suma_grupo.rename(columns={dem_col: 'Categoría', 'Ponderador_Num': 'Suma Ponderador'}, inplace=True)
                suma_grupo['Variable'] = dem_col; all_results.append(suma_grupo[['Variable', 'Categoría', 'Suma Ponderador']])
            if all_results:
                final_table = pd.concat(all_results, ignore_index=True)
                final_table['Suma Ponderador'] = final_table['Suma Ponderador'].apply(lambda x: f"{x:,.2f}" if pd.notna(x) else "Error")
                final_table['Categoría'] = final_table['Categoría'].fillna('VACÍO/NULO')
                content_v10 += final_table.to_html(classes='df-style', index=False)
            else: content_v10 += "[INFO] No se generaron resultados."; status_v10 = "Error"
        except Exception as e: status_v10 = "Error"; content_v10 += f"<span class='status-error-inline'>[ERROR]</span> {e}"
    validation_results.append({'key': key_v10, 'status': status_v10, 'content': content_v10})

    # --- [NUEVA] Validación 11: Volumetría (Umbrales Numéricos) (Usa _full) ---
    key_v11 = "Volumetría (Umbrales Numéricos)"; content_v11 = ""; status_v11 = "Correcto"; id_unico = 'Unico'
    errores_umbrales = []
    reglas_pais = THRESHOLDS_POR_PAIS.get(pais_clave_interna, [])
    if not reglas_pais:
        status_v11 = "Info"; content_v11 = f"[INFO] No hay reglas de volumetría para {pais_seleccionado_display}."
    else:
        id_col_ok_v11 = id_unico in df_numerico_full.columns
        if not id_col_ok_v11: content_v11 += f"<span class='status-error-inline'>[WARN]</span> Col '{id_unico}' no encontrada.<br>"
        for regla in reglas_pais:
            col = regla['col']; cond = regla['cond']; lim = regla['lim']
            if col not in df_numerico_full.columns:
                errores_umbrales.append({'Columna': col, 'Error': 'No encontrada', 'ID': '-', 'Valor': '-'})
                if status_v11 != "Error": status_v11 = "Error"; continue
            try: col_numerica = pd.to_numeric(df_numerico_full[col], errors='coerce')
            except Exception as e:
                errores_umbrales.append({'Columna': col, 'Error': f'No numérico ({e})', 'ID': '-', 'Valor': '-'})
                if status_v11 != "Error": status_v11 = "Error"
                continue # Saltar al siguiente regla
            violaciones = pd.Series(False, index=df_numerico_full.index); cond_desc = ""
            if cond == 'mayor_a': violaciones = col_numerica.gt(lim) & col_numerica.notna(); cond_desc = f"ser > {lim}"
            elif cond == 'igual_a': violaciones = col_numerica.eq(lim) & col_numerica.notna(); cond_desc = f"ser == {lim}"
            else:
                errores_umbrales.append({'Columna': col, 'Error': f'Cond "{cond}" no reconocida', 'ID': '-', 'Valor': '-'})
                if status_v11 != "Error": status_v11 = "Error"
                continue
            df_violaciones = df_numerico_full.loc[violaciones]
            if not df_violaciones.empty:
                if status_v11 == "Correcto": status_v11 = "Incorrecto"
                for idx, row in df_violaciones.iterrows():
                    uid = row[id_unico] if id_col_ok_v11 else f"Fila {idx+2}"
                    valor_violador_num = col_numerica.loc[idx]
                    try: valor_violador_str = f"{valor_violador_num:,.2f}" if isinstance(valor_violador_num, (float, np.floating)) else f"{int(valor_violador_num):,}"
                    except: valor_violador_str = str(row[col]) # Fallback
                    errores_umbrales.append({'Columna': col, 'Error': f'Valor {valor_violador_str} viola no {cond_desc}', 'ID': uid, 'Valor': valor_violador_str})
        if status_v11 == "Correcto": content_v11 = f"<span class='status-correcto-inline'>[Correcto]</span> Cumplen umbrales."
        elif status_v11 in ["Incorrecto", "Error"]:
             prefix = ""
             if status_v11 == "Incorrecto": prefix = f"<span class='status-incorrecto-inline'>[Incorrecto]</span> Valores fuera de umbral:<br>"
             if status_v11 == "Error": prefix = f"<span class='status-error-inline'>[ERROR]</span> Errores en validación:<br>"
             if errores_umbrales: df_errores = pd.DataFrame(errores_umbrales)[['Columna', 'Error', 'ID', 'Valor']]; content_v11 = prefix + df_errores.to_html(classes='df-style', index=False)
             else: content_v11 = prefix + "(Sin detalles específicos)"
    validation_results.append({'key': key_v11, 'status': status_v11, 'content': content_v11})
    # --- [FIN V11] ---


    # --- FIN VALIDACIONES ---

    st.success("Proceso de validación terminado.")
    st.divider()

    # --- ÁREA DE REPORTE ESTILIZADO ---
    # (El código de ordenamiento, resumen y reporte detallado es el mismo que antes)
    sort_order = {'Correcto': 1, 'Incorrecto': 2, 'Error': 3, 'Info': 4}
    sorted_results_temp = sorted(validation_results, key=lambda v: sort_order.get(v['status'], 5))
    final_numbered_results = []
    for i, v in enumerate(sorted_results_temp):
        new_title = f"Validación {i + 1}: {v['key']}"; final_numbered_results.append({'title': new_title, 'status': v['status'], 'content': v['content']})

    correct_count = sum(1 for v in validation_results if v['status'] == 'Correcto'); incorrect_count = sum(1 for v in validation_results if v['status'] == 'Incorrecto')
    info_count = sum(1 for v in validation_results if v['status'] == 'Info'); error_count = sum(1 for v in validation_results if v['status'] == 'Error')
    total_validations = correct_count + incorrect_count + error_count; correct_pct = (correct_count / total_validations * 100) if total_validations > 0 else 0; incorrect_pct = (incorrect_count / total_validations * 100) if total_validations > 0 else 0

    st.subheader("--- RESUMEN DE VALIDACIÓN ---", divider='violet')
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("✅ Correctos", f"{correct_count}", f"{correct_pct:.1f}%"); col2.metric("❌ Incorrectos", f"{incorrect_count}", f"{incorrect_pct:.1f}%")
    col3.metric("⚠️ Errores", f"{error_count}"); col4.metric("ℹ️ Reportes", f"{info_count}")

    with st.expander("Ver lista detallada de verificaciones", expanded=False):
        summary_list_html = "<div class='summary-list'><ul>";
        for v in final_numbered_results:
            icon = "✅" if v['status'] == 'Correcto' else "❌" if v['status'] == 'Incorrecto' else "⚠️" if v['status'] == 'Error' else "ℹ️"
            summary_list_html += f"<li>{icon} <strong>{v['title']}:</strong> <span class='status-{v['status'].lower()}-inline'>{v['status']}</span></li>"
        summary_list_html += "</ul></div>"; st.markdown(summary_list_html, unsafe_allow_html=True)

    st.divider()

    st.subheader("--- REPORTE DETALLADO ---", divider='violet')
    for v in final_numbered_results:
        status_class = f"status-{v['status'].lower()}"
        content_detalle = v['content'].replace("<h3>5.1:", "<h3 class='sub-heading'>5.1:").replace("<h3>5.2:", "<h3 class='sub-heading'>5.2:").replace("<h3>5.3:", "<h3 class='sub-heading'>5.3:")
        safe_content = content_detalle.replace('<br>', '<br/>')
        safe_content = safe_content.replace('\n', '')
        html_content = f"""<div class='validation-box {status_class}'><h3>{v['title']}</h3>{safe_content}</div>"""
        st.markdown(html_content, unsafe_allow_html=True)

    st.success("¡Validación completada!")

else:
    st.info("Por favor, carga ambos archivos Excel para iniciar la validación.")