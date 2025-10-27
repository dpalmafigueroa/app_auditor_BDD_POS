# --- validador_app.py ---
# Versión Atlantia 2.18 para Streamlit (Corrección Definitiva Geo Guatemala - 5 Regiones)

import streamlit as st
import pandas as pd
import locale
import io # Para leer los archivos subidos
import numpy as np # Para manejar tipos numéricos
from io import BytesIO # Para crear Excel en memoria

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title="Auditor de calidad de bases de datos")

# --- Función para convertir DataFrame a Excel en memoria ---
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Reglas')
    processed_data = output.getvalue()
    return processed_data

# --- CSS PERSONALIZADO ---
# (Mismo CSS)
atlantia_css = """
<style>
    /* ... (pega aquí TODO el CSS de la versión anterior 2.1) ... */
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
    .status-info-inline { color: var(--validation-info-text) !important; font-weight: bold; } /* Añadido para V13 */


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
st.markdown('<div class="main-header-container">', unsafe_allow_html=True)
st.markdown("""
<div class="main-header">
    <svg class="atlantia-logo" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="atlantiaGradient" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#04D1CD"/><stop offset="50%" style="stop-color:#6546C3"/><stop offset="100%" style="stop-color:#AA49CA"/></linearGradient></defs><path d="M20,80 L50,20 L80,80 L65,80 L50,50 L35,80 Z" fill="url(#atlantiaGradient)" stroke="white" stroke-width="2"/></svg>
    <h1 style="display: inline-block; vertical-align: middle;">Auditor de calidad de bases de datos</h1>
    <div class="subtitle">Powered by Atlantia</div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- INSTRUCCIONES ---
st.markdown("## Instrucciones")
st.markdown("""1.  **Selecciona el país** para el cual se aplicarán las reglas geográficas y de volumetría.\n2.  **Carga los archivos Excel** correspondientes a la base numérica y textual.""")
st.markdown("### Evaluaciones Realizadas:")
st.markdown("""
* **Tamaño:** Compara filas y columnas.
* **Orden de IDs:** Verifica `Unico` vs `[auth]`.
* **Unico valor en (lastpage y lastpage2):** Revisa unicidad.
* **Periodo de Campo:** Muestra fechas de `startdate`.
* **Agrupaciones:** Rango de edad vs `[age]`, `NSE` vs `NSE2`, Geografía (Región/Ciudad). (Perú incluye validación `region2`).
* **Origen/Proveedor:** Conteo por proveedor.
* **Nulos (Numérica):** Busca vacíos en `NSE`, `gender`, `AGErange`, `Region`.
* **Abiertas ('Menciona'):** Lista respuestas.
* **Ponderador (Numérica):** Compara suma `Ponderador` vs total filas.
* **Suma Ponderador por demográfico:** Suma `Ponderador` por `NSE`, `gender`, `AGErange`, `Region` y muestra porcentajes.
* **Volumetría (Numérica):** Valida columnas contra umbrales definidos por país.
* **Duplicados en IDs:** Verifica que `Unico` (Num) y `[auth]` (Txt) no tengan valores repetidos.
* **Duplicados [panelistid]:** Reporta (Info) `[panelistid]` (Txt) duplicados y su conteo.
""")
st.divider()

# --- CONFIGURACIÓN DE REGLAS ---
CLASIFICACIONES_POR_PAIS = {
    'Panamá': {'Centro': ['Aguadulce', 'Antón', 'La Pintada', 'Natá', 'Olá', 'Penonomé','Chagres', 'Ciudad de Colón', 'Colón', 'Donoso', 'Portobelo','Resto del Distrito', 'Santa Isabel', 'La Chorrera', 'Arraiján','Capira', 'Chame', 'San Carlos'],'Metro': ['Panamá', 'San Miguelito', 'Balboa', 'Chepo', 'Chimán', 'Taboga', 'Chepigana', 'Pinogana'],'Oeste': ['Alanje', 'Barú', 'Boquerón', 'Boquete', 'Bugaba', 'David', 'Dolega', 'Guacala', 'Remedios', 'Renacimiento', 'San Félix', 'San Lorenzo', 'Tolé', 'Bocas del Toro', 'Changuinola', 'Chiriquí Grande', 'Chitré', 'Las Minas', 'Los Pozos', 'Ocú', 'Parita', 'Pesé', 'Santa María', 'Guararé', 'Las Tablas', 'Los Santos', 'Macaracas', 'Pedasí', 'Pocrí', 'Tonosí', 'Atalaya', 'Calobre', 'Cañazas', 'La Mesa', 'Las Palmas', 'Mariato', 'Montijo', 'Río de Jesús', 'San Francisco', 'Santa Fé', 'Santiago', 'Soná']},
    'México': {'Central/Bajío': ['CDMX + AM', 'Estado de México', 'Guanajuato', 'Hidalgo','Morelos', 'Puebla', 'Querétaro', 'Tlaxcala'],'Norte': ['Baja California Norte', 'Baja California Sur', 'Chihuahua', 'Coahuila','Durango', 'Nuevo León', 'Sinaloa', 'Sonora', 'Tamaulipas'],'Occidente/Pacifico': ['Aguascalientes', 'Colima', 'Guerrero', 'Jalisco', 'Michoacan','Nayarit', 'San Luis Potosi', 'Zacatecas'],'Sureste': ['Campeche', 'Chiapas', 'Oaxaca', 'Quintana Roo', 'Tabasco','Veracruz', 'Yucatán']},
    'Colombia': {'Andes': ['Antioquia', 'Caldas', 'Quindio', 'Risaralda', 'Santander'],'Centro': ['Bogotá', 'Boyacá', 'Casanare', 'Cundinamarca'],'Norte': ['Atlántico', 'Bolívar', 'Cesar', 'Córdoba', 'La Guajira', 'Magdalena', 'Norte de Santader', 'Sucre'], 'Sur': ['Cauca', 'Huila', 'Meta', 'Nariño', 'Tolima', 'Valle de Cauca']},
    'Ecuador': {'Costa': ['El Oro', 'Esmeraldas', 'Los Ríos', 'Manabí', 'Santa Elena', 'Santo Domingo de los Tsáchilas'],'Guayaquil': ['Guayas'],'Quito': ['Pichincha'],'Sierra': ['Azuay', 'Bolívar', 'Cañar', 'Carchi', 'Chimborazo', 'Cotopaxi', 'Imbabura', 'Loja', 'Tungurahua']},
    'Perú': {'REGIÓN CENTRO': ['Ayacucho', 'Huancavelica', 'Junín'],'REGIÓN LIMA': ['Ica', 'Lima', 'Callao'],'REGIÓN NORTE': ['Áncash', 'Cajamarca', 'La Libertad', 'Lambayeque', 'Piura', 'Tumbes'],'REGIÓN ORIENTE': ['Amazonas', 'Huánuco', 'Loreto', 'Pasco', 'San Martin', 'Ucayali'],'REGIÓN SUR': ['Apurimac', 'Arequipa', 'Cuzco', 'Madre de Dios', 'Moquegua', 'Puno', 'Tacna']},
    'R. Dominicana': {'Capital': ['Distrito Nacional', 'Santo Domingo'],'Region Este': ['El Seibo', 'Hato Mayor', 'La Altagracia', 'La Romana', 'Monte Plata', 'San Pedro de Macorís'],'Region norte/ Cibao': ['Dajabón', 'Duarte (San Francisco)', 'Espaillat', 'Hermanas Mirabal', 'La Vega', 'María Trinidad Sánchez', 'Monseñor Nouel', 'Montecristi', 'Puerto Plata', 'Samaná', 'Sánchez Ramírez', 'Santiago', 'Santiago Rodríguez', 'Valverde'],'Region Sur': ['Azua', 'Bahoruco', 'Barahona', 'Elías Piña', 'Independencia', 'Pedernales', 'Peravia', 'San Cristóbal', 'San José de Ocoa', 'San Juan']},
    'Honduras': {'Norte Ciudad': ['Cortés'],'Norte interior': ['Atlántida', 'Colón', 'Copán', 'Ocotepeque', 'Santa Bárbara', 'Yoro'],'Sur Ciudad': ['Francisco Morazán'],'Sur interior': ['Choluteca', 'Comayagua', 'El Paraíso', 'Intibucá', 'La Paz', 'Olancho', 'Valle']},
    # --- INICIO CORRECCIÓN GUATEMALA v2.18 (Definitiva - 5 Regiones) ---
    'Guatemala': {
        'Metro': ['Guatemala'],
        'Nor Oriente': ['Petén', 'Alta Verapaz', 'Zacapa', 'El Progreso', 'Izabal', 'Baja Verapaz'],
        'Nor Occidente': ['San Marcos', 'Quetzaltengango', 'Chimaltenango', 'Quiché', 'Totonicapán', 'Huehuetenango', 'Sololá', 'Sacatepequez'],
        'Sur Occidente': ['Suchitepéquez', 'Retalhuleu'],
        'Sur Oriente': ['Chiquimula', 'Jutiapa', 'Jalapa', 'Santa Rosa', 'Escuintla']
    },
    # --- FIN CORRECCIÓN GUATEMALA v2.18 ---
    'El Salvador': {'AMSS': ['San Salvador'],'Centro': ['Cabañas', 'Chalatenango', 'Cuscatlán', 'La Libertad', 'La Paz', 'San Vicente'],'Occidente': ['Ahuachapán', 'Santa Ana', 'Sonsonate'],'Oriente': ['La Union', 'Morazán', 'San Miguel', 'Usulután']},
    'Costa Rica': {}, 'Puerto Rico': {}, 'Colombia Minors': {}
}

# (NUEVO) REGLAS ADICIONALES PARA PERÚ (REGION2)
CLASIFICACIONES_PERU_REGION2 = {
    'REGIÓN LIMA': ['Lima', 'Callao'],
    'REGIÓN NORTE': ['La Libertad', 'Lambayeque', 'Piura'],
    'REGIÓN CENTRO': ['Junín'],
    'REGIÓN SUR': ['Arequipa', 'Cuzco'],
    'REGIÓN ORIENTE': ['Loreto']
}
# ---

THRESHOLDS_POR_PAIS = {
    # (Igual que V1.8)
    'México': [{'col': 'Total_consumo', 'cond': 'mayor_a', 'lim': 11000}, {'col': 'Total_consumo', 'cond': 'igual_a', 'lim': 0},{'col': 'Beer', 'cond': 'mayor_a', 'lim': 7000},{'col': 'Wine', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Spirits', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Other_alc', 'cond': 'mayor_a', 'lim': 1400},{'col': 'CSDs', 'cond': 'mayor_a', 'lim': 5000},{'col': 'Energy_drinks', 'cond': 'mayor_a', 'lim': 1400}],
    'Colombia': [{'col': 'Total_consumo', 'cond': 'mayor_a', 'lim': 11000}, {'col': 'Total_consumo', 'cond': 'igual_a', 'lim': 0},{'col': 'Beer', 'cond': 'mayor_a', 'lim': 7000},{'col': 'Wine', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Spirits', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Other_alc', 'cond': 'mayor_a', 'lim': 1400},{'col': 'CSDs', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Energy_drinks', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Malts', 'cond': 'mayor_a', 'lim': 2000}],
    'Ecuador': [{'col': 'Total_consumo', 'cond': 'mayor_a', 'lim': 11000}, {'col': 'Total_consumo', 'cond': 'igual_a', 'lim': 0},{'col': 'Beer', 'cond': 'mayor_a', 'lim': 7000},{'col': 'Wine', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Spirits', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Other_alc', 'cond': 'mayor_a', 'lim': 1400},{'col': 'CSDs', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Energy_drinks', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Malts', 'cond': 'mayor_a', 'lim': 2000}],
    'Perú': [{'col': 'Total_consumo', 'cond': 'mayor_a', 'lim': 11000}, {'col': 'Total_consumo', 'cond': 'igual_a', 'lim': 0},{'col': 'Beer', 'cond': 'mayor_a', 'lim': 7000},{'col': 'Wine', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Spirits', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Other_alc', 'cond': 'mayor_a', 'lim': 1400},{'col': 'CSDs', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Energy_drinks', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Malts', 'cond': 'mayor_a', 'lim': 2000}],
    'R. Dominicana': [{'col': 'Total_consumo', 'cond': 'mayor_a', 'lim': 11000},{'col': 'Total_consumo', 'cond': 'igual_a', 'lim': 0},{'col': 'Beer', 'cond': 'mayor_a', 'lim': 7000},{'col': 'Wine', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Ron', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Whisky', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Spirits', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Other_alc', 'cond': 'mayor_a', 'lim': 1400},{'col': 'CSDs', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Energy_drinks', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Malts', 'cond': 'mayor_a', 'lim': 2000}],
    'Honduras': [{'col': 'Total_consumo', 'cond': 'mayor_a', 'lim': 11000},{'col': 'Total_consumo', 'cond': 'igual_a', 'lim': 0},{'col': 'Beer', 'cond': 'mayor_a', 'lim': 7000},{'col': 'Wine', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Spirits', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Other_alc', 'cond': 'mayor_a', 'lim': 1400},{'col': 'CSDs', 'cond': 'mayor_a', 'lim': 5000},{'col': 'Energy_drinks', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Malts', 'cond': 'mayor_a', 'lim': 2000}],
    'El Salvador': [{'col': 'Total_consumo', 'cond': 'mayor_a', 'lim': 11000},{'col': 'Total_consumo', 'cond': 'igual_a', 'lim': 0},{'col': 'Beer', 'cond': 'mayor_a', 'lim': 7000},{'col': 'Wine', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Spirits', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Other_alc', 'cond': 'mayor_a', 'lim': 1400},{'col': 'CSDs', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Energy_drinks', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Malts', 'cond': 'mayor_a', 'lim': 2000}],
    'Costa Rica': [{'col': 'Total_consumo', 'cond': 'mayor_a', 'lim': 11000},{'col': 'Total_consumo', 'cond': 'igual_a', 'lim': 0},{'col': 'Beer', 'cond': 'mayor_a', 'lim': 7000},{'col': 'Wine', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Spirits', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Other_alc', 'cond': 'mayor_a', 'lim': 1400},{'col': 'CSDs', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Energy_drinks', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Malts', 'cond': 'mayor_a', 'lim': 2000}],
    'Puerto Rico': [{'col': 'Total_consumo', 'cond': 'mayor_a', 'lim': 11000},{'col': 'Total_consumo', 'cond': 'igual_a', 'lim': 0},{'col': 'Beer', 'cond': 'mayor_a', 'lim': 7000},{'col': 'Wine', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Spirits', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Other_alc', 'cond': 'mayor_a', 'lim': 1400},{'col': 'CSDs', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Energy_drinks', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Malts', 'cond': 'mayor_a', 'lim': 2000}],
    'Panamá': [{'col': 'Total_consumo', 'cond': 'mayor_a', 'lim': 11000},{'col': 'Total_consumo', 'cond': 'igual_a', 'lim': 0},{'col': 'Beer', 'cond': 'mayor_a', 'lim': 7000},{'col': 'Wine', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Spirits', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Other_alc', 'cond': 'mayor_a', 'lim': 1400},{'col': 'CSDs', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Energy_drinks', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Malts', 'cond': 'mayor_a', 'lim': 2000}],
    'Guatemala': [{'col': 'Total_consumo', 'cond': 'mayor_a', 'lim': 11000},{'col': 'Total_consumo', 'cond': 'igual_a', 'lim': 0},{'col': 'Beer', 'cond': 'mayor_a', 'lim': 7000},{'col': 'Wine', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Spirits', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Other_alc', 'cond': 'mayor_a', 'lim': 1400},{'col': 'CSDs', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Energy_drinks', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Malts', 'cond': 'mayor_a', 'lim': 2000}],
    'Colombia Minors': [{'col': 'Total_consumo', 'cond': 'mayor_a', 'lim': 11000},{'col': 'Total_consumo', 'cond': 'igual_a', 'lim': 0},{'col': 'Beer', 'cond': 'mayor_a', 'lim': 7000},{'col': 'Wine', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Spirits', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Other_alc', 'cond': 'mayor_a', 'lim': 1400},{'col': 'CSDs', 'cond': 'mayor_a', 'lim': 3000},{'col': 'Energy_drinks', 'cond': 'mayor_a', 'lim': 1400},{'col': 'Malts', 'cond': 'mayor_a', 'lim': 2000}],
}
paises_disponibles = sorted(list(CLASIFICACIONES_POR_PAIS.keys()))

# --- (ACTUALIZADO) MAPEO DINÁMICO DE COLUMNAS ---
COLUMN_MAPPING = {
    'Base Numérica': {
        'Unico': {'Panamá': 'Unico', 'México': 'Unico', 'Colombia': 'Unico', 'Ecuador': 'Unico', 'Perú': 'Unico', 'R. Dominicana': 'Unico', 'Honduras': 'Unico', 'El Salvador': 'Unico', 'Guatemala': 'Unico', 'Colombia Minors': 'id'},
        'lastpage': {'Panamá': 'lastpage', 'México': 'lastpage', 'Colombia': 'lastpage', 'Ecuador': 'lastpage', 'Perú': 'lastpage', 'R. Dominicana': 'lastpage', 'Honduras': 'lastpage', 'El Salvador': 'lastpage', 'Guatemala': 'lastpage', 'Colombia Minors': 'lastpage'},
        'lastpage_Parte2': {'Panamá': 'lastpage_Parte2', 'México': 'lastpage_Parte2', 'Colombia': 'lastpage_Parte2', 'Ecuador': 'lastpage_Parte2', 'Perú': 'lastpage_Parte2', 'R. Dominicana': 'lastpage_Parte2', 'Honduras': 'lastpage_Parte2', 'El Salvador': 'lastpage_Parte2', 'Guatemala': 'lastpage_Parte2', 'Colombia Minors': ''},
        'Ponderador': {'Panamá': 'Ponderador', 'México': 'Ponderador', 'Colombia': 'Ponderador', 'Ecuador': 'Ponderador', 'Perú': 'Ponderador', 'R. Dominicana': 'Ponderador', 'Honduras': 'Ponderador', 'El Salvador': 'Ponderador', 'Guatemala': 'Ponderador', 'Colombia Minors': ''},
        'NSE': {'Panamá': 'NSE', 'México': 'NSE', 'Colombia': 'NSE', 'Ecuador': 'NSE', 'Perú': 'NSE', 'R. Dominicana': 'NSE', 'Honduras': 'NSE', 'El Salvador': 'NSE', 'Guatemala': 'NSE', 'Colombia Minors': 'NSE'},
        'gender': {'Panamá': 'gender', 'México': 'gender', 'Colombia': 'gender', 'Ecuador': 'gender', 'Perú': 'gender', 'R. Dominicana': 'gender', 'Honduras': 'gender', 'El Salvador': 'gender', 'Guatemala': 'gender', 'Colombia Minors': 'gender'},
        'AGErange': {'Panamá': 'AGErange', 'México': 'AGErange', 'Colombia': 'AGErange', 'Ecuador': 'AGErange', 'Perú': 'AGErange', 'R. Dominicana': 'AGErange', 'Honduras': 'AGErange', 'El Salvador': 'AGErange', 'Guatemala': 'AGErange', 'Colombia Minors': 'AGErange'},
        'Region': {'Panamá': 'Region', 'México': 'region', 'Colombia': 'region', 'Ecuador': 'region', 'Perú': 'region', 'R. Dominicana': 'region', 'Honduras': 'region', 'El Salvador': 'region', 'Guatemala': 'region', 'Colombia Minors': 'region'},
        'Total_consumo': {'Panamá': 'Total_consumo', 'México': 'Total_consumo', 'Colombia': 'Total_consumo', 'Ecuador': 'Total_consumo', 'Perú': 'Total_consumo', 'R. Dominicana': 'Total_consumo', 'Honduras': 'Total_consumo', 'El Salvador': 'Total_consumo', 'Guatemala': 'Total_consumo', 'Colombia Minors': 'Total_consumo'},
        'Beer': {'Panamá': 'Beer', 'México': 'Beer', 'Colombia': 'Beer', 'Ecuador': 'Beer', 'Perú': 'Beer', 'R. Dominicana': 'Beer', 'Honduras': 'Beer', 'El Salvador': 'Beer', 'Guatemala': 'Beer', 'Colombia Minors': ''},
        'Wine': {'Panamá': 'Wine', 'México': 'Wine', 'Colombia': 'Wine', 'Ecuador': 'Wine', 'Perú': 'Wine', 'R. Dominicana': 'Wine', 'Honduras': 'Wine', 'El Salvador': 'Wine', 'Guatemala': 'Wine', 'Colombia Minors': ''},
        'Ron': {'R. Dominicana': 'Rum'}, 
        'Whisky': {'R. Dominicana': 'Wiskey'}, 
        'Spirits': {'Panamá': 'Spirits', 'México': 'Spirits', 'Colombia': 'Spirits', 'Ecuador': 'Spirits', 'Perú': 'Spirits', 'R. Dominicana': 'Spirits', 'Honduras': 'Spirits', 'El Salvador': 'Spirits', 'Guatemala': 'Spirits', 'Colombia Minors': ''},
        'Other_alc': {'Panamá': 'Other_alc', 'México': 'Other_alc', 'Colombia': 'Other_alc', 'Ecuador': 'Other_alc', 'Perú': 'Other_alc', 'R. Dominicana': 'Other_alc', 'Honduras': 'Other_alc', 'El Salvador': 'Other_alc', 'Guatemala': 'Other_alc', 'Colombia Minors': ''},
        'CSDs': {'Panamá': 'CSDs', 'México': 'CSDs', 'Colombia': 'CSDs', 'Ecuador': 'CSDs', 'Perú': 'CSDs', 'R. Dominicana': 'CSDs', 'Honduras': 'CSDs', 'El Salvador': 'CSDs', 'Guatemala': 'CSDs', 'Colombia Minors': 'CSDs'},
        'Energy_drinks': {'Panamá': 'Energy_drinks', 'México': 'Energy_drinks', 'Colombia': 'Energy_drinks', 'Ecuador': 'Energy_drinks', 'Perú': 'Energy_drinks', 'R. Dominicana': 'Energy_drinks', 'Honduras': 'Energy_drinks', 'El Salvador': 'Energy_drinks', 'Guatemala': 'Energy_drinks', 'Colombia Minors': 'Energy_drinks'},
        'Malts': {'Panamá': 'Malts', 'México': '', 'Colombia': 'Malts', 'Ecuador': 'Malts', 'Perú': 'Malts', 'R. Dominicana': 'Malts', 'Honduras': 'Malts', 'El Salvador': 'Malts', 'Guatemala': 'Malts', 'Colombia Minors': 'Malts'},
        'RTD_Cider': {'Panamá': 'RTD_Cider', 'México': 'RTD_Cider', 'Colombia': 'RTD_Cider', 'Ecuador': 'RTD_Cider', 'Perú': 'RTD_Cider', 'R. Dominicana': 'RTD_Cider', 'Honduras': 'RTD_Cider', 'El Salvador': 'RTD_Cider', 'Guatemala': 'RTD_Cider', 'Colombia Minors': ''},
        'Hard_Seltzer': {'Panamá': 'Hard_Seltzer', 'México': 'Hard_Seltzer', 'Colombia': 'Hard_Seltzer', 'Ecuador': 'Hard_Seltzer', 'Perú': 'Hard_Seltzer', 'R. Dominicana': 'Hard_Seltzer', 'Honduras': 'Hard_Seltzer', 'El Salvador': 'Hard_Seltzer', 'Guatemala': 'Hard_Seltzer', 'Colombia Minors': ''},
        'Bottled_water': {'Panamá': 'Bottled_water', 'México': 'Bottled_water', 'Colombia': 'Bottled_water', 'Ecuador': 'Bottled_water', 'Perú': 'Bottled_water', 'R. Dominicana': 'Bottled_water', 'Honduras': 'Bottled_water', 'El Salvador': 'Bottled_water', 'Guatemala': 'Bottled_water', 'Colombia Minors': 'Bottled_water'},
        'NABs': {'Panamá': 'NABs', 'México': 'NABs', 'Colombia': 'NABs', 'Ecuador': 'NABs', 'Perú': 'NABs', 'R. Dominicana': 'NABs', 'Honduras': 'NABs', 'El Salvador': 'NABs', 'Guatemala': 'NABs', 'Colombia Minors': 'NABs'},
        'Alcohol': {'Panamá': 'Alcohol', 'México': '', 'Colombia': 'Alcohol', 'Ecuador': 'Alcohol', 'Perú': 'Alcohol', 'R. Dominicana': 'Alcohol', 'Honduras': 'Alcohol', 'El Salvador': '', 'Guatemala': 'Alcohol', 'Colombia Minors': ''},
    },
    'Base Textual': {
        '[auth]': {'Panamá': '[auth]', 'México': '[auth]', 'Colombia': '[auth]', 'Ecuador': '[auth]', 'Perú': '[auth]', 'R. Dominicana': '[auth]', 'Honduras': '[auth]', 'El Salvador': '[auth]', 'Guatemala': '[auth]', 'Colombia Minors': 'id'},
        'startdate': {'Panamá': 'startdate', 'México': 'startdate', 'Colombia': 'startdate', 'Ecuador': 'startdate', 'Perú': 'startdate', 'R. Dominicana': 'startdate', 'Honduras': 'startdate', 'El Salvador': 'startdate', 'Guatemala': 'startdate', 'Colombia Minors': 'startdate'},
        'Por favor, selecciona el rango de edad en el que te encuentras:': {'Panamá': 'Por favor, selecciona el rango de edad en el que te encuentras:', 'México': 'Por favor, selecciona el rango de edad en el que te encuentras:', 'Colombia': 'Por favor, selecciona el rango de edad en el que te encuentras:', 'Ecuador': 'Por favor, selecciona el rango de edad en el que te encuentras:', 'Perú': 'Por favor, selecciona el rango de edad en el que te encuentras:', 'R. Dominicana': 'Por favor, selecciona el rango de edad en el que te encuentras:', 'Honduras': 'Por favor, selecciona el rango de edad en el que te encuentras:', 'El Salvador': 'Por favor, selecciona el rango de edad en el que te encuentras:', 'Guatemala': 'Por favor, selecciona el rango de edad en el que te encuentras:', 'Colombia Minors': 'AGErange'},
        '[age]': {'Panamá': '[age]', 'México': 'Edad:', 'Colombia': 'Edad en el que te encuentras:', 'Ecuador': 'EDAD', 'Perú': 'Edad:', 'R. Dominicana': 'AGE', 'Honduras': 'EDAD', 'El Salvador': 'AGE', 'Guatemala': 'AGE', 'Colombia Minors': 'A partir de esta sección te pediremos que respondas pensando sobre el consumo de bebidas de tus hijos entre 8 y 17 años.Si tienes más de 1 hijo en esta edad te pediremos que te enfoques en uno de tus hijos para responder sobre su consumo. ¿Qué edad t'},
        'NSE': {'Panamá': 'NSE', 'México': 'SEL AGRUPADO', 'Colombia': 'NSE', 'Ecuador': 'agrupado ows', 'Perú': 'SEL AGRUPADO', 'R. Dominicana': 'NSE', 'Honduras': 'NSE', 'El Salvador': 'NSE', 'Guatemala': 'NSE Agrupado', 'Colombia Minors': 'SEL AGRUPADO'},
        'NSE2': {'Panamá': 'NSE2', 'México': 'SEL SEPARADO', 'Colombia': 'NSE2', 'Ecuador': 'Clasificación NSE (HIDDEN VARIABLE)PUNTOS: 0', 'Perú': 'SEL SEPARADO', 'R. Dominicana': 'NSE2', 'Honduras': 'NSE2', 'El Salvador': '¿Cuál es el ingreso mensual promedio de su hogar?', 'Guatemala': 'Clasificación NSE (HIDDEN VARIABLE)PUNTOS: 0', 'Colombia Minors': 'SEL SEPARADO'},
        'Region 1 (Centro/Metro/Oeste)': {'Panamá': 'Region 1 (Centro/Metro/Oeste)', 'México': 'region', 'Colombia': 'region_Parte2', 'Ecuador': 'Region', 'Perú': 'region', 'R. Dominicana': 'region', 'Honduras': 'Region', 'El Salvador': 'REGION', 'Guatemala': 'region', 'Colombia Minors': 'region'},
        'Region2': {'Perú': 'region2'}, 
        'CIUDAD': {'Panamá': 'CIUDAD', 'México': 'Estado donde vive:', 'Colombia': 'Por favor escribe el nombre de la ciudad en la que vives:', 'Ecuador': 'Estado', 'Perú': 'state', 'R. Dominicana': 'state', 'Honduras': 'Region', 'El Salvador': 'ESTADO', 'Guatemala': 'state', 'Colombia Minors': 'Departamento:'},
        'Origen': {'Panamá': 'Origen', 'México': 'Origen', 'Colombia': '', 'Ecuador': 'Origen del registro', 'Perú': '', 'R. Dominicana': '', 'Honduras': '', 'El Salvador': '', 'Guatemala': '', 'Colombia Minors': ''},
        # Columnas como 'Proveedor' y '[panelistid]' no están en el CSV de mapeo,
        # por lo que el script buscará el nombre estándar ('Proveedor', '[panelistid]')
        # en el archivo cargado.
    }
}
# ---

# --- SELECCIÓN DE PAÍS Y CARGA DE ARCHIVOS ---
col_pais, col_vacia = st.columns([1, 2])
with col_pais:
    pais_seleccionado_display = st.selectbox("Selecciona el País:", paises_disponibles, key="select_pais")

# --- Botones de Descarga ---
st.markdown("### Descargar Reglas de Validación")
col_dl1, col_dl2, col_dl_spacer = st.columns([2, 2, 3])
with col_dl1:
    reglas_vol = THRESHOLDS_POR_PAIS.get(pais_seleccionado_display, [])
    if reglas_vol:
        df_vol = pd.DataFrame(reglas_vol); df_vol.columns = ['Columna', 'Condición', 'Límite']
        excel_vol = to_excel(df_vol)
        st.download_button(label="Descargar Reglas Volumetría (.xlsx)", data=excel_vol, file_name=f'reglas_volumetria_{pais_seleccionado_display}.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', key='dl_vol')
    else: st.info(f"No hay regras de volumetría para {pais_seleccionado_display}.")
with col_dl2:
    reglas_geo = CLASIFICACIONES_POR_PAIS.get(pais_seleccionado_display, {})
    if reglas_geo:
        lista_g = [{'Región': r, 'Ciudad/Dpto': c} for r, ciudades in reglas_geo.items() for c in ciudades]
        if lista_g:
            df_geo = pd.DataFrame(lista_g)
            excel_geo = to_excel(df_geo)
            st.download_button(label="Descargar Reglas Geografía (.xlsx)", data=excel_geo, file_name=f'reglas_geografia_{pais_seleccionado_display}.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', key='dl_geo')
        else: st.info(f"No hay reglas geográficas detalladas para {pais_seleccionado_display}.")
    else: st.info(f"No hay reglas geográficas definidas para {pais_seleccionado_display}.")

st.divider()

# --- Carga de Archivos ---
st.markdown("### Carga de Archivos Excel")
col1_up, col2_up = st.columns(2)
with col1_up: uploaded_file_num = st.file_uploader("Carga el archivo Numérico", type=["xlsx"], key="num")
with col2_up: uploaded_file_txt = st.file_uploader("Carga el archivo Textual", type=["xlsx"], key="txt")

# --- LÓGICA DE VALIDACIÓN ---
if uploaded_file_num is not None and uploaded_file_txt is not None:
    
    st.info(f"Archivos cargados. Iniciando validación para **{pais_seleccionado_display}**...")
    st.divider()
    pais_clave_interna = pais_seleccionado_display 
    validation_results = []
    
    try:
        df_numerico_full = pd.read_excel(io.BytesIO(uploaded_file_num.getvalue()))
        df_textual_full = pd.read_excel(io.BytesIO(uploaded_file_txt.getvalue()))
    except Exception as e: st.error(f"Error al leer archivos: {e}"); st.stop()
    
    # --- LÓGICA DE RENOMBRADO DINÁMICO ---
    rename_map_num = {}
    rename_map_txt = {}
    for standard_name, country_mappings in COLUMN_MAPPING['Base Numérica'].items():
        if pais_clave_interna in country_mappings:
            country_specific_name = country_mappings[pais_clave_interna]
            if country_specific_name and country_specific_name in df_numerico_full.columns:
                rename_map_num[country_specific_name] = standard_name
    for standard_name, country_mappings in COLUMN_MAPPING['Base Textual'].items():
        if pais_clave_interna in country_mappings:
            country_specific_name = country_mappings[pais_clave_interna]
            if country_specific_name and country_specific_name in df_textual_full.columns:
                rename_map_txt[country_specific_name] = standard_name
    try:
        df_numerico_full.rename(columns=rename_map_num, inplace=True)
        df_textual_full.rename(columns=rename_map_txt, inplace=True)
    except Exception as e:
        st.error(f"Error al renombrar columnas: {e}")
        st.stop()
    # --- FIN DE LÓGICA DE RENOMBRADO ---

    # --- Optimización de Carga ---
    num_cols_base = ['Unico', 'lastpage', 'lastpage_Parte2']
    txt_cols = ['[auth]', 'startdate', "Por favor, selecciona el rango de edad en el que te encuentras:", '[age]', 'NSE', 'NSE2', 'Region 1 (Centro/Metro/Oeste)', 'CIUDAD', 'Origen', 'Proveedor', 'Region2', '[panelistid]'] 
    num_cols_extra = ['Ponderador', 'NSE', 'gender', 'AGErange', 'Region']
    num_cols_extra.extend([rule['col'] for rule in THRESHOLDS_POR_PAIS.get(pais_clave_interna, [])])
    num_cols = num_cols_base + list(set([c for c in num_cols_extra if c in df_numerico_full.columns and c not in num_cols_base]))
    num_ex = [c for c in num_cols if c in df_numerico_full.columns]; 
    txt_ex = [c for c in txt_cols if c in df_textual_full.columns]
    
    try:
        # Aseguramos que las columnas clave para V5.1 existan antes de crear df_textual
        col_g_edad_std = "Por favor, selecciona el rango de edad en el que te encuentras:"
        col_d_edad_std = '[age]'
        
        # Encontramos los nombres reales en df_textual_full después del renombrado
        actual_col_g_edad = next((col for col in df_textual_full.columns if col == col_g_edad_std), None)
        actual_col_d_edad = next((col for col in df_textual_full.columns if col == col_d_edad_std), None)

        # Si alguna falta, añadimos un placeholder o notificamos
        if actual_col_g_edad is None and col_g_edad_std not in txt_ex:
            st.warning(f"Columna '{col_g_edad_std}' (o mapeada) no encontrada para V5.1.")
        elif actual_col_g_edad and actual_col_g_edad not in txt_ex:
             txt_ex.append(actual_col_g_edad) # Asegurar que esté en la lista si se encontró

        if actual_col_d_edad is None and col_d_edad_std not in txt_ex:
             st.warning(f"Columna '{col_d_edad_std}' (o mapeada) no encontrada para V5.1.")
        elif actual_col_d_edad and actual_col_d_edad not in txt_ex:
             txt_ex.append(actual_col_d_edad) # Asegurar que esté en la lista si se encontró
        
        # Creamos df_textual asegurando que solo incluya columnas existentes
        txt_ex_final = [col for col in txt_ex if col in df_textual_full.columns]
        df_textual = df_textual_full[txt_ex_final]
        df_numerico = df_numerico_full[num_ex] # Asumiendo que num_ex ya está validado

    except KeyError as e: st.error(f"Columna base esencial {e} no encontrada (después del renombrado)."); st.stop()
    
    # --- VALIDACIONES (V1-V13) ---
    
    # V1: Tamaño
    key_v1 = "Tamaño de las Bases"; content_v1 = ""; status_v1 = "Correcto"
    fn, cn = df_numerico_full.shape; ft, ct = df_textual_full.shape
    content_v1 += f"- Num: {fn} filas x {cn} columnas<br>- Txt: {ft} filas x {ct} columnas<br><br><b>Comparación:</b><br>"
    if fn == ft and cn == ct: content_v1 += "<span class='status-correcto-inline'>[Correcto]</span> Coinciden."
    else: status_v1 = "Incorrecto"; content_v1 += "<span class='status-incorrecto-inline'>[Incorrecto]</span> Diferentes.<br>";
    if fn != ft: content_v1 += "- Filas.<br>"
    if cn != ct: content_v1 += "- Columnas.<br>"
    validation_results.append({'key': key_v1, 'status': status_v1, 'content': content_v1})

    # V2: Orden IDs
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

    # V3: lastpage
    key_v3 = "lastpage y lastpage_Parte2"; content_v3 = ""; status_v3 = "Correcto"; cols_v3 = ['lastpage', 'lastpage_Parte2']
    for col in cols_v3:
        content_v3 += f"<br><b>'{col}':</b><br>";
        if col not in df_numerico.columns: status_v3 = "Error"; content_v3 += f"<span class='status-error-inline'>[ERROR]</span> No encontrada.<br>"; continue
        vals = df_numerico[col].dropna().unique()
        if len(vals) <= 1: content_v3 += f"<span class='status-correcto-inline'>[Correcto]</span> Único valor.<br>"
        else: status_v3 = "Incorrecto"; vals_str = ", ".join(map(str, vals)); content_v3 += f"<span class='status-incorrecto-inline'>[Incorrecto]</span> Múltiples: {vals_str}<br>"
    validation_results.append({'key': key_v3, 'status': status_v3, 'content': content_v3})

    # V4: Periodo Campo
    key_v4 = "Periodo Campo ('startdate')"; content_v4 = ""; status_v4 = "Info"; col_fecha = 'startdate'
    locale_usado = ''; formato_fecha = '%d/%b/%Y %H:%M'
    try:
        try: locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8'); locale_usado = 'es_ES.UTF-8'; formato_fecha = '%d de %B de %Y, %I:%M %p'
        except:
            try: locale.setlocale(locale.LC_TIME, 'es'); locale_usado = 'es'; formato_fecha = '%d de %B de %Y, %I:%M %p'
            except: locale.setlocale(locale.LC_TIME, ''); locale_usado = 'Sistema'
        
        if col_fecha not in df_textual.columns: raise KeyError(f"'{col_fecha}' ausente.")
        fechas = pd.to_datetime(df_textual[col_fecha], dayfirst=True, errors='coerce').dropna()
        if not fechas.empty: f_min, f_max = fechas.min(), fechas.max(); content_v4 += f"<b>Periodo (locale: {locale_usado}):</b><br> - Inicio: {f_min.strftime(formato_fecha)}<br> - Fin: {f_max.strftime(formato_fecha)}<br>"
        else: status_v4 = "Error"; content_v4 += "<span class='status-error-inline'>[ERROR]</span> No hay fechas válidas.<br>"
    except KeyError as e: status_v4 = "Error"; content_v4 += f"<span class='status-error-inline'>[ERROR]</span> Col {e}.<br>"
    except Exception as e_loc: status_v4 = "Error"; content_v4 += f"<span class='status-error-inline'>[ERROR Locale]</span> {e_loc}.<br>"
    validation_results.append({'key': key_v4, 'status': status_v4, 'content': content_v4})

    # V5: Agrupaciones (ACTUALIZADO - SELECCIÓN EXPLÍCITA PRIMERA COLUMNA)
    key_v5 = "Agrupaciones"; content_v5 = ""; status_v5 = "Correcto"
    # 5.1 Edad
    content_v5 += "<h3>5.1: Edad vs [age]</h3>"; 
    col_g_edad_std = "Por favor, selecciona el rango de edad en el que te encuentras:" # Nombre estándar
    col_d_edad_std = '[age]' # Nombre estándar
    
    try:
        # --- INICIO CORRECCIÓN v2.11 (Fix V5.1 - Duplicados) ---
        
        # 1. Encontrar la POSICIÓN de la primera columna que coincida
        pos_g_edad = -1
        pos_d_edad = -1
        
        # Iterar para encontrar el primer índice (posición)
        # Usamos df_textual (el subconjunto) que ya fue definido
        for i, col_name in enumerate(df_textual.columns):
            if pos_g_edad == -1 and col_name == col_g_edad_std:
                pos_g_edad = i
            if pos_d_edad == -1 and col_name == col_d_edad_std:
                pos_d_edad = i
            # Optimización: si encontramos ambas, salimos
            if pos_g_edad != -1 and pos_d_edad != -1:
                break
        
        # 2. Verificar que AMBAS columnas se encontraron
        if pos_g_edad == -1:
             raise KeyError(f"No se encontró la columna de rango de edad ('{col_g_edad_std}' o mapeada)")
        if pos_d_edad == -1:
             raise KeyError(f"No se encontró la columna de edad exacta ('{col_d_edad_std}' o mapeada)")

        # 3. Crear el DataFrame temporal USANDO POSICIONES (iloc)
        # Esto garantiza que solo tomamos 2 columnas, incluso si los nombres están duplicados.
        df_temp_edad = df_textual.iloc[:, [pos_g_edad, pos_d_edad]].copy()
        
        # 4. Renombrar las columnas (que ahora son únicas posicionalmente) a los NOMBRES ESTÁNDAR
        # Esto hace que el resto del código funcione sin importar cómo se llamaban.
        df_temp_edad.columns = [col_g_edad_std, col_d_edad_std]
        
        # --- FIN CORRECCIÓN v2.11 ---

        # Ahora el resto del código usa los nombres estándar
        df_temp_edad[col_d_edad_std] = pd.to_numeric(df_temp_edad[col_d_edad_std], errors='coerce')
        
        # Agrupar usando el nombre ESTÁNDAR de la columna de rango
        grouped_edad = df_temp_edad.groupby(col_g_edad_std, dropna=False)
        
        # Accedemos directamente a la columna de agregación
        rep_edad = grouped_edad[col_d_edad_std].agg(['count', 'min', 'max']) 
        rep_edad.columns = ['Total', 'Min', 'Max']
        content_v5 += rep_edad.to_html(classes='df-style')

    except KeyError as e: 
        status_v5 = "Error"
        content_v5 += f"<span class='status-error-inline'>[ERROR]</span> {e}<br>"
    except Exception as e_agg: 
        status_v5 = "Error"
        content_v5 += f"<span class='status-error-inline'>[ERROR Agregación Edad]</span> {e_agg}<br>"
        
    content_v5 += "<hr style='border-top: 1px dotted #ccc;'>"
    
    # 5.2 NSE
    content_v5 += "<h3>5.2: NSE vs NSE2</h3>"; col_g_nse = 'NSE'; col_d_nse = 'NSE2'
    try:
        # --- INICIO CORRECCIÓN v2.14 (Fix V5.2 - Duplicados NSE/NSE2) ---
        
        # 1. Encontrar la POSICIÓN de la primera columna 'NSE' y 'NSE2'
        pos_g_nse = -1
        pos_d_nse = -1
        for i, col_name in enumerate(df_textual.columns):
            if pos_g_nse == -1 and col_name == col_g_nse:
                pos_g_nse = i
            if pos_d_nse == -1 and col_name == col_d_nse:
                pos_d_nse = i
            if pos_g_nse != -1 and pos_d_nse != -1:
                break
                
        # 2. Verificar que AMBAS columnas se encontraron
        if pos_g_nse == -1:
             raise KeyError(f"No se encontró la columna '{col_g_nse}' (o mapeada)")
        if pos_d_nse == -1:
             raise KeyError(f"No se encontró la columna '{col_d_nse}' (o mapeada)")
             
        # 3. Usar iloc para pasar las Series (columnas por posición) a crosstab
        rep_nse = pd.crosstab(df_textual.iloc[:, pos_g_nse], df_textual.iloc[:, pos_d_nse])
        
        # --- FIN CORRECCIÓN v2.14 ---
        
        content_v5 += "Verifica consistencia:<br>" + rep_nse.to_html(classes='df-style')
    except KeyError as e:
        if status_v5 != "Error": status_v5 = "Error"; content_v5 += f"<span class='status-error-inline'>[ERROR]</span> {e}<br>"
    except Exception as e_crosstab: # Captura otros posibles errores de crosstab
        if status_v5 != "Error": status_v5 = "Error"; content_v5 += f"<span class='status-error-inline'>[ERROR Crosstab NSE]</span> {e_crosstab}<br>"
        
    content_v5 += "<hr style='border-top: 1px dotted #ccc;'>"
    
    # 5.3 Geografía (Región 1) - Añadido chequeo case-insensitive v2.16
    content_v5 += f"<h3>5.3: Geografía ({pais_seleccionado_display} - Region 1)</h3>"; status_v5_3 = "Correcto"
    try:
        clasif = CLASIFICACIONES_POR_PAIS.get(pais_clave_interna);
        if not clasif: status_v5_3 = "Info"; content_v5 += f"<span class='status-info-inline'>[INFO]</span> No hay reglas geográficas para {pais_seleccionado_display}."
        else:
            col_reg = 'Region 1 (Centro/Metro/Oeste)'; col_ciu = 'CIUDAD'
            if not all(c in df_textual.columns for c in [col_reg, col_ciu]): raise KeyError(f"Columnas Región/Ciudad no encontradas.")
            err_reg = [];
            for idx, row in df_textual.iterrows():
                reg, ciu = row[col_reg], row[col_ciu]
                if pd.isna(reg) or pd.isna(ciu): continue
                # Convertir a string para comparación insensible a mayúsculas/minúsculas y espacios
                reg_str = str(reg).strip()
                ciu_str = str(ciu).strip()

                # Buscar la región correcta (insensible a mayúsculas/minúsculas)
                found_reg = False
                correct_reg_key = None
                for key in clasif.keys():
                    if key.lower() == reg_str.lower():
                        found_reg = True
                        correct_reg_key = key
                        break
                
                if found_reg:
                    # Buscar la ciudad correcta (insensible a mayúsculas/minúsculas)
                    if not any(ciudad.lower() == ciu_str.lower() for ciudad in clasif[correct_reg_key]):
                         err_reg.append({'Fila': idx + 2, 'Region': reg, 'Ciudad': ciu, 'Error': f"'{ciu}' no encontrada en '{correct_reg_key}' (case insensitive)"})
                else:
                    err_reg.append({'Fila': idx + 2, 'Region': reg, 'Ciudad': ciu, 'Error': f"Región '{reg}' no válida (case insensitive)"})

            if not err_reg: content_v5 += f"<span class='status-correcto-inline'>[Correcto]</span> Consistente."
            else: status_v5_3 = "Incorrecto"; content_v5 += f"<span class='status-incorrecto-inline'>[Incorrecto]</span> {len(err_reg)} inconsistencias.<br>"; df_err = pd.DataFrame(err_reg); content_v5 += "Primeras 5:<br>" + df_err.head().to_html(classes='df-style', index=False)
    except (KeyError, ValueError) as e: status_v5_3 = "Error"; content_v5 += f"<span class='status-error-inline'>[ERROR]</span> {e}<br>"
    if status_v5 == "Correcto" and status_v5_3 not in ["Correcto", "Info"]: status_v5 = status_v5_3
    elif status_v5_3 == "Error": status_v5 = "Error"

    # --- 5.4: Geografía 2 (Solo Perú) - Añadido chequeo case-insensitive v2.16
    if pais_clave_interna == 'Perú':
        content_v5 += "<hr style='border-top: 1px dotted #ccc;'>"
        content_v5 += f"<h3>5.4: Geografía 2 ({pais_seleccionado_display} - Region2)</h3>"
        status_v5_4 = "Correcto" 
        try:
            clasif_r2 = CLASIFICACIONES_PERU_REGION2
            col_reg_r2 = 'Region2'; col_ciu_r2 = 'CIUDAD'
            if not all(c in df_textual.columns for c in [col_reg_r2, col_ciu_r2]): 
                raise KeyError(f"Columnas {col_reg_r2} o {col_ciu_r2} no encontradas para V5.4.")
            err_reg_r2 = []
            for idx, row in df_textual.iterrows():
                reg, ciu = row[col_reg_r2], row[col_ciu_r2]
                if pd.isna(reg) or pd.isna(ciu): continue
                # Convertir a string para comparación insensible
                reg_str = str(reg).strip()
                ciu_str = str(ciu).strip()

                found_reg_r2 = False
                correct_reg_key_r2 = None
                for key in clasif_r2.keys():
                    if key.lower() == reg_str.lower():
                        found_reg_r2 = True
                        correct_reg_key_r2 = key
                        break
                        
                if found_reg_r2:
                    if not any(ciudad.lower() == ciu_str.lower() for ciudad in clasif_r2[correct_reg_key_r2]):
                        err_reg_r2.append({'Fila': idx + 2, 'Region2': reg, 'Ciudad': ciu, 'Error': f"'{ciu}' no en '{correct_reg_key_r2}' (region2, case insensitive)"})
                else:
                    if pd.notna(reg): # Solo reportar si la región no es nula pero inválida
                         err_reg_r2.append({'Fila': idx + 2, 'Region2': reg, 'Ciudad': ciu, 'Error': f"Región '{reg}' no válida (region2, case insensitive)"})
                         
            if not err_reg_r2:
                content_v5 += f"<span class='status-correcto-inline'>[Correcto]</span> Consistente (region2)."
            else:
                status_v5_4 = "Incorrecto"
                content_v5 += f"<span class='status-incorrecto-inline'>[Incorrecto]</span> {len(err_reg_r2)} inconsistencias (region2).<br>"
                df_err_r2 = pd.DataFrame(err_reg_r2)
                content_v5 += "Primeras 5:<br>" + df_err_r2.head().to_html(classes='df-style', index=False)
        except (KeyError, ValueError) as e: 
            status_v5_4 = "Error"
            content_v5 += f"<span class='status-error-inline'>[ERROR]</span> {e}<br>"
        if status_v5 == "Correcto" and status_v5_4 not in ["Correcto", "Info"]: status_v5 = status_v5_4
        elif status_v5_4 == "Error": status_v5 = "Error"
    # --- FIN V5.4 ---

    validation_results.append({'key': key_v5, 'status': status_v5, 'content': content_v5})


    # V6: Origen/Proveedor
    key_v6 = "Origen/Proveedor"; content_v6 = ""; status_v6 = "Info"; prov_cols = ['Origen', 'Proveedor']
    prov_col = next((col for col in prov_cols if col in df_textual.columns), None)
    if prov_col:
        content_v6 += f"<b>'{prov_col}':</b><br>";
        try: cnt = df_textual[prov_col].value_counts(dropna=False).reset_index(); cnt.columns = [prov_col, 'Conteo']; content_v6 += cnt.to_html(classes='df-style', index=False)
        except Exception as e: status_v6 = "Error"; content_v6 += f"<span class='status-error-inline'>[ERROR]</span> {e}<br>"
    else: content_v6 += f"<span class='status-info-inline'>[INFO]</span> No encontrada." 
    validation_results.append({'key': key_v6, 'status': status_v6, 'content': content_v6})

    # V7: Nulos Base Numérica
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

    # V8: Abiertas ('Menciona')
    key_v8 = "Abiertas ('Menciona')"; content_v8 = ""; status_v8 = "Info"
    try:
        id_auth = '[auth]';
        if id_auth not in df_textual_full.columns: raise KeyError(f"'{id_auth}' ausente.")
        cols_m = [c for c in df_textual_full.columns if "menciona" in str(c).lower() and "mencionaste" not in str(c).lower()]; total_p = len(cols_m)
        if not cols_m: content_v8 = "<span class='status-info-inline'>[INFO]</span> No hay columnas 'menciona'." 
        else:
            melted = df_textual_full[[id_auth] + cols_m].melt(id_vars=[id_auth], var_name='Pregunta', value_name='Respuesta')
            final_abiertas = melted.dropna(subset=['Respuesta'])
            if final_abiertas.empty: content_v8 = f"<span class='status-info-inline'>[INFO]</span> {total_p} columnas 'menciona', sin respuestas." 
            else:
                total_r = len(final_abiertas); content_v8 += f"<span class='status-info-inline'>[REPORTE]</span> <b>{total_p}</b> cols, <b>{total_r}</b> respuestas.<br><br>"; 
                df_disp = final_abiertas[[id_auth, 'Respuesta']]
                if total_r > 500: content_v8 += f"(Se muestran las primeras 500)<br>"; df_disp = df_disp.head(500)
                df_disp.columns = [id_auth, 'Respuesta']
                content_v8 += df_disp.to_html(classes='df-style', index=False)
    except Exception as e: status_v8 = "Error"; content_v8 = f"<span class='status-error-inline'>[ERROR]</span> {e}<br>" 
    validation_results.append({'key': key_v8, 'status': status_v8, 'content': content_v8})

    # V9: Ponderador vs Total Filas
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
    except KeyError as e: status_v9 = "Error"; content_v9 = f"<span class='status-error-inline'>[ERROR]</span> {e}"
    except Exception as e: status_v9 = "Error"; content_v9 = f"<span class='status-error-inline'>[ERROR]</span> al sumar '{col_pond}': {e}"
    validation_results.append({'key': key_v9, 'status': status_v9, 'content': content_v9})

    # V10: Suma Ponderador por Demo
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
            if ponderador_numerico.isnull().any(): content_v10 += f"<span class='status-error-inline'>[WARN]</span> '{col_pond}' contiene valores no numéricos o vacíos.<br>"
            temp_df = df_numerico_full.copy(); temp_df['Ponderador_Num'] = ponderador_numerico
            for dem_col in cols_demo:
                suma_grupo = temp_df.groupby(dem_col, dropna=False)['Ponderador_Num'].sum().reset_index()
                total_suma_variable = suma_grupo['Ponderador_Num'].sum()
                if total_suma_variable > 0: suma_grupo['Porcentaje'] = (suma_grupo['Ponderador_Num'] / total_suma_variable) * 100
                else: suma_grupo['Porcentaje'] = 0.0
                suma_grupo.rename(columns={dem_col: 'Categoría', 'Ponderador_Num': 'Suma Ponderador'}, inplace=True)
                suma_grupo['Variable'] = dem_col; 
                suma_grupo['Categoría'] = suma_grupo['Categoría'].fillna('VACÍO/NULO')
                all_results.append(suma_grupo[['Variable', 'Categoría', 'Suma Ponderador', 'Porcentaje']])

            if all_results:
                final_table = pd.concat(all_results, ignore_index=True)
                final_table['Suma Ponderador'] = final_table['Suma Ponderador'].apply(lambda x: f"{x:,.2f}" if pd.notna(x) and x != int(x) else f"{int(x):,}" if pd.notna(x) else "Error")
                final_table['Porcentaje'] = final_table['Porcentaje'].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else "-")
                
                content_v10 += final_table.to_html(classes='df-style', index=False)
            else: 
                content_v10 += "<span class='status-info-inline'>[INFO]</span> No se generaron resultados para la suma de ponderador."; 
                status_v10 = "Error" 
        except Exception as e: 
            status_v10 = "Error"; 
            content_v10 += f"<span class='status-error-inline'>[ERROR]</span> {e}"
    validation_results.append({'key': key_v10, 'status': status_v10, 'content': content_v10})


    # V11: Volumetría (Umbrales Numéricos)
    key_v11 = "Volumetría (Umbrales Numéricos)"; content_v11 = ""; status_v11 = "Correcto"; id_unico = 'Unico'
    errores_umbrales = []
    reglas_pais = THRESHOLDS_POR_PAIS.get(pais_clave_interna, [])
    if not reglas_pais:
        status_v11 = "Info"; content_v11 = f"<span class='status-info-inline'>[INFO]</span> No hay regras de volumetría para {pais_seleccionado_display}." 
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
                continue
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
                    try: valor_violador_str = f"{valor_violador_num:,.2f}" if isinstance(valor_violador_num, (float, np.floating)) and valor_violador_num != int(valor_violador_num) else f"{int(valor_violador_num):,}"
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

    # V12: Duplicados en IDs Principales ([auth] y Unico)
    key_v12 = "Duplicados en IDs Principales"; content_v12 = ""; status_v12 = "Correcto"
    col_num_v12 = 'Unico'; col_txt_v12 = '[auth]'
    try:
        # Checar Numérico ('Unico')
        if col_num_v12 not in df_numerico.columns:
            raise KeyError(f"'{col_num_v12}' (Numérica)")
        dups_num = df_numerico[col_num_v12].duplicated()
        total_dups_num = dups_num.sum()
        if total_dups_num > 0:
            status_v12 = "Incorrecto"
            ids_dup_num = df_numerico[dups_num][col_num_v12].unique()
            content_v12 += f"<span class='status-incorrecto-inline'>[Incorrecto]</span> <b>{total_dups_num}</b> duplicados en <b>'{col_num_v12}'</b> (Num).<br>Primeros 5 valores: {list(ids_dup_num[:5])}<br>"
        else:
            content_v12 += f"<span class='status-correcto-inline'>[Correcto]</span> Sin duplicados en <b>'{col_num_v12}'</b> (Num).<br>"

        # Checar Textual ('[auth]')
        if col_txt_v12 not in df_textual.columns:
            raise KeyError(f"'{col_txt_v12}' (Textual)")
        dups_txt = df_textual[col_txt_v12].duplicated()
        total_dups_txt = dups_txt.sum()
        if total_dups_txt > 0:
            status_v12 = "Incorrecto" 
            ids_dup_txt = df_textual[dups_txt][col_txt_v12].unique()
            content_v12 += f"<span class='status-incorrecto-inline'>[Incorrecto]</span> <b>{total_dups_txt}</b> duplicados en <b>'{col_txt_v12}'</b> (Txt).<br>Primeros 5 valores: {list(ids_dup_txt[:5])}<br>"
        else:
             if status_v12 == "Correcto": 
                 content_v12 += f"<span class='status-correcto-inline'>[Correcto]</span> Sin duplicados en <b>'{col_txt_v12}'</b> (Txt).<br>"
             else: 
                 content_v12 += f"<span class='status-correcto-inline'></span> Sin duplicados en <b>'{col_txt_v12}'</b> (Txt).<br>"

    except KeyError as e:
        status_v12 = "Error"
        content_v12 = f"<span class='status-error-inline'>[ERROR]</span> Columna {e} no encontrada." 
    validation_results.append({'key': key_v12, 'status': status_v12, 'content': content_v12})


    # V13: Duplicados en [panelistid] (Mantiene cambios V2.8)
    key_v13 = "Duplicados en [panelistid]"; content_v13 = ""; status_v13 = "Info" 
    col_panel = '[panelistid]'; col_auth_v13 = '[auth]' 
    try:
        if col_panel not in df_textual_full.columns:
            raise KeyError(f"'{col_panel}' (Textual)")
        if col_auth_v13 not in df_textual_full.columns:
            raise KeyError(f"'{col_auth_v13}' (Textual)") 

        total_filas = len(df_textual_full) 
        dups_mask = df_textual_full[col_panel].duplicated(keep=False)
        total_duplicados = dups_mask.sum()

        if total_duplicados > 0:
            df_dups = df_textual_full[dups_mask]
            ids_unicos_duplicados = df_dups[col_panel].nunique()
            
            content_v13 += f"<span class='status-info-inline'>[REPORTE]</span> Se encontraron <b>{total_duplicados}</b> filas con <b>{ids_unicos_duplicados}</b> '{col_panel}' duplicados.<br>" 
            content_v13 += f"- Total Filas Duplicadas: <b>{total_duplicados:,}</b><br>"
            content_v13 += f"- Total Filas Encuesta: <b>{total_filas:,}</b><br>"
            content_v13 += f"- Porcentaje Duplicado: <b>{(total_duplicados / total_filas) * 100:.2f}%</b><br><br>"
            content_v13 += f"Reporte completo de IDs duplicados y su frecuencia:<br>"
            
            conteo_dups = df_dups.groupby(col_panel)[col_auth_v13].count().reset_index()
            conteo_dups.columns = [col_panel, 'Veces Repetido']
            conteo_dups = conteo_dups.sort_values(by='Veces Repetido', ascending=False)
            
            content_v13 += conteo_dups.to_html(classes='df-style', index=False) 
        
        else:
            content_v13 += f"<span class='status-info-inline'>[REPORTE]</span> No se encontraron duplicados en <b>'{col_panel}'</b>." 
            content_v13 += f"<br>Total filas validadas: <b>{total_filas:,}</b>."
    
    except KeyError as e:
        status_v13 = "Error" 
        content_v13 = f"<span class='status-error-inline'>[ERROR]</span> Columna {e} no encontrada." 
    except Exception as e:
         status_v13 = "Error" 
         content_v13 = f"<span class='status-error-inline'>[ERROR inesperado]</span> {e}" 
         
    validation_results.append({'key': key_v13, 'status': status_v13, 'content': content_v13})


    # --- FIN VALIDACIONES ---

    st.success("Proceso de validación terminado.")
    st.divider()

    # --- ÁREA DE REPORTE ESTILIZADO ---
    sort_order = {'Correcto': 1, 'Incorrecto': 2, 'Error': 3, 'Info': 4}
    sorted_results_temp = sorted(validation_results, key=lambda v: sort_order.get(v['status'], 5))
    final_numbered_results = []
    for i, v in enumerate(sorted_results_temp):
        if v['key'] == "Duplicados en [panelistid]":
            new_title = f"Validación {i + 1}: {v['key']}"
        else:
            new_title = f"Validación {i + 1}: {v['key']}"
        final_numbered_results.append({'title': new_title, 'status': v['status'], 'content': v['content']})

    correct_count = sum(1 for v in validation_results if v['status'] == 'Correcto'); incorrect_count = sum(1 for v in validation_results if v['status'] == 'Incorrecto')
    info_count = sum(1 for v in validation_results if v['status'] == 'Info'); error_count = sum(1 for v in validation_results if v['status'] == 'Error')
    total_validations_pct = correct_count + incorrect_count + error_count 
    correct_pct = (correct_count / total_validations_pct * 100) if total_validations_pct > 0 else 0; 
    incorrect_pct = (incorrect_count / total_validations_pct * 100) if total_validations_pct > 0 else 0

    st.subheader("--- RESUMEN DE VALIDACIÓN ---", divider='violet')
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("✅ Correctos", f"{correct_count}", f"{correct_pct:.1f}%"); col2.metric("❌ Incorrectos", f"{incorrect_count}", f"{incorrect_pct:.1f}%")
    col3.metric("⚠️ Errores", f"{error_count}"); col4.metric("ℹ️ Reportes", f"{info_count}")

    with st.expander("Ver lista detallada de verificaciones", expanded=False):
        summary_list_html = "<div class='summary-list'><ul>";
        for v in final_numbered_results:
            icon = "✅" if v['status'] == 'Correcto' else "❌" if v['status'] == 'Incorrecto' else "⚠️" if v['status'] == 'Error' else "ℹ️"
            status_inline_class = f"status-{v['status'].lower()}-inline"
            summary_list_html += f"<li>{icon} <strong>{v['title']}:</strong> <span class='{status_inline_class}'>{v['status']}</span></li>"
        summary_list_html += "</ul></div>"; st.markdown(summary_list_html, unsafe_allow_html=True)

    st.divider()

    st.subheader("--- REPORTE DETALLADO ---", divider='violet')
    for v in final_numbered_results:
        status_class = f"status-{v['status'].lower()}"
        content_detalle = v['content'].replace("<h3>5.1:", "<h3 class='sub-heading'>5.1:").replace("<h3>5.2:", "<h3 class='sub-heading'>5.2:").replace("<h3>5.3:", "<h3 class='sub-heading'>5.3:").replace("<h3>5.4:", "<h3 class='sub-heading'>5.4:")
        safe_content = content_detalle.replace('<br>', '<br/>')
        safe_content = safe_content.replace('\n', '') 
        html_content = f"""<div class='validation-box {status_class}'><h3>{v['title']}</h3>{safe_content}</div>"""
        st.markdown(html_content, unsafe_allow_html=True)