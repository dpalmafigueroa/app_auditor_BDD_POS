# --- validador_app.py ---
# Versión Atlantia 1.0 para Streamlit

import streamlit as st
import pandas as pd
import locale
import io # Para leer los archivos subidos

# --- CONFIGURACIÓN DE PÁGINA ---
# Wide layout y título de la pestaña
st.set_page_config(layout="wide", page_title="Validador Atlantia")

# --- CSS PERSONALIZADO ATLANTIA + VALIDACIÓN ---
# Incluye reglas para ocultar menu y footer
atlantia_css = """
<style>
    /* Importar fuentes Atlantia */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Hind:wght@400;500;600&display=swap');

    /* Variables de colores Atlantia */
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
        --atlantia-black: #000000; /* Texto principal */
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
    }

    /* Ocultar menú y footer de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;} /* Oculta la barra superior también */

    /* Tipografía base Atlantia */
    body, * { /* Aplicar a todo */
        font-family: 'Hind', sans-serif;
        color: var(--atlantia-black); /* Color de texto por defecto */
    }

    /* Títulos - Poppins Bold 24-18pt Violet */
    h1, .main-title {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 700 !important;
        font-size: 24pt !important;
        color: var(--atlantia-violet) !important;
    }
    h2, .section-title { /* Aplicado a st.subheader */
        font-family: 'Poppins', sans-serif !important;
        font-weight: 700 !important;
        font-size: 20pt !important;
        color: var(--atlantia-violet) !important;
    }
    h3, .subsection-title { /* Usado para títulos dentro de validaciones */
        font-family: 'Poppins', sans-serif !important;
        font-weight: 700 !important;
        font-size: 16pt !important; /* Ajustado para caber mejor */
        color: var(--atlantia-violet) !important;
    }

    /* Subtítulos de indicadores - Hind 14pt Violet */
    .indicator-subtitle, .metric-label, .stMetric label {
        font-family: 'Hind', sans-serif !important;
        font-weight: 500 !important;
        font-size: 14pt !important;
        color: var(--atlantia-violet) !important;
    }

    /* Cuerpo de texto - Hind 12pt Negro */
    p, .body-text, .stMarkdown, .stText, label, div[data-baseweb="select"] > div { /* Incluir labels y texto de select */
        font-family: 'Hind', sans-serif !important;
        font-weight: 400 !important;
        font-size: 12pt !important;
        color: var(--atlantia-black) !important;
    }

    /* Elementos específicos de Streamlit */
    .stButton button {
        font-family: 'Hind', sans-serif !important;
        font-weight: 600 !important;
        font-size: 12pt !important;
        border-radius: 8px !important;
    }
    .stSelectbox label, .stTextInput label, .stTextArea label, .stFileUploader label { /* Labels de widgets */
        font-family: 'Hind', sans-serif !important;
        font-weight: 600 !important; /* Un poco más de peso */
        font-size: 14pt !important;
        color: var(--atlantia-violet) !important;
    }
    .stDataFrame, .stTable {
        font-family: 'Hind', sans-serif !important;
        font-size: 11pt !important; /* Ligeramente más pequeño para tablas */
    }
    .stExpander summary {
        font-family: 'Hind', sans-serif !important;
        font-weight: 600 !important; /* Más peso */
        font-size: 14pt !important;
        color: var(--atlantia-violet) !important;
    }

    /* --- ESTILOS DE VALIDACIÓN --- */
    .validation-box { border: 1px solid #ddd; border-radius: 8px; padding: 16px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); line-height: 1.6; }
    .validation-box h3 { margin-top: 0; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 2px solid #eee; }
    .validation-box h3.sub-heading { margin-top: 15px; margin-bottom: 10px; padding-bottom: 5px; font-size: 1.1em; color: #333; border-bottom: 1px solid #eee; }
    /* Correcto */
    .status-correcto { background-color: var(--validation-correct-bg); border-left: 5px solid var(--validation-correct-border); }
    .status-correcto h3 { color: var(--validation-correct-text); }
    .status-correcto-inline { color: var(--validation-correct-text); font-weight: bold; }
    /* Incorrecto */
    .status-incorrecto { background-color: var(--validation-incorrect-bg); border-left: 5px solid var(--validation-incorrect-border); }
    .status-incorrecto h3 { color: var(--validation-incorrect-text); }
    .status-incorrecto-inline { color: var(--validation-incorrect-text); font-weight: bold; }
    /* Info */
    .status-info { background-color: var(--validation-info-bg); border-left: 5px solid var(--validation-info-border); }
    .status-info h3 { color: var(--validation-info-text); }
    /* Error */
    .status-error { background-color: var(--validation-error-bg); border-left: 5px solid var(--validation-error-border); }
    .status-error h3 { color: var(--validation-error-text); }
    .status-error-inline { color: var(--validation-error-text); font-weight: bold; }
    /* Tablas dentro de validación */
    .df-style { border-collapse: collapse; width: 95%; margin: 10px auto; font-size: 0.9em; }
    .df-style th, .df-style td { border: 1px solid #ccc; padding: 6px; }
    .df-style th { background-color: #f4f4f4; text-align: left; color: var(--atlantia-black); } /* Asegurar color texto header tabla */
    .df-style tr:nth-child(even) { background-color: #f9f9f9; }
    .df-style td { color: var(--atlantia-black); } /* Asegurar color texto celdas */
    /* Resumen Lista */
    .summary-list ul { list-style-type: none; padding-left: 0; }
    .summary-list li { padding: 5px 0; border-bottom: 1px dotted #eee; }
    .summary-list li strong { color: var(--atlantia-violet); } /* Títulos en lista resumen */

    /* --- FIN ESTILOS VALIDACIÓN --- */

    /* Header principal con gradiente Atlantia (como en tu CSS) */
    .main-header-container { /* Contenedor para aplicar margen */
        margin-bottom: 2rem;
    }
    .main-header {
        text-align: center;
        padding: 1rem 0; /* Menos padding vertical */
        background: linear-gradient(135deg, var(--atlantia-violet) 0%, var(--atlantia-purple) 100%);
        border-radius: 15px;
        color: white;
    }
    .main-header h1 {
        color: white !important; /* Override especifico */
        font-family: 'Poppins', sans-serif !important;
        font-weight: 700 !important;
        font-size: 24pt !important; /* Asegurar tamaño */
        margin-bottom: 0.2rem;
    }
     .main-header .subtitle { /* Clase para el subtítulo */
        color: rgba(255, 255, 255, 0.9) !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 500 !important; /* Ligeramente menos peso */
        font-size: 14pt !important; /* Más pequeño */
        margin-top: 0;
    }
    /* SVG Logo */
     .atlantia-logo {
         width: 40px; /* Más pequeño */
         height: auto;
         vertical-align: middle; /* Alinear con texto */
         margin-right: 0.5rem;
     }

</style>
"""
st.markdown(atlantia_css, unsafe_allow_html=True)

# --- HEADER PERSONALIZADO ---
# Usamos un contenedor para margen
st.markdown('<div class="main-header-container">', unsafe_allow_html=True)
st.markdown("""
<div class="main-header">
    <svg class="atlantia-logo" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="atlantiaGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#04D1CD"/>
                <stop offset="50%" style="stop-color:#6546C3"/>
                <stop offset="100%" style="stop-color:#AA49CA"/>
            </linearGradient>
        </defs>
        <path d="M20,80 L50,20 L80,80 L65,80 L50,50 L35,80 Z" fill="url(#atlantiaGradient)" stroke="white" stroke-width="2"/>
    </svg>
    <h1 style="display: inline-block; vertical-align: middle;">Validador de Bases</h1>
    <div class="subtitle">Powered by Atlantia</div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True) # Cierre del contenedor


# --- CONFIGURACIÓN FIJA (Puedes moverla a un archivo separado si crece) ---
CLASIFICACIONES_POR_PAIS = {
    'Panamá': { # Cambiado a nombre legible
        'Centro': [
            'Aguadulce', 'Antón', 'La Pintada', 'Natá', 'Olá', 'Penonomé',
            'Chagres', 'Ciudad de Colón', 'Colón', 'Donoso', 'Portobelo',
            'Resto del Distrito', 'Santa Isabel', 'La Chorrera', 'Arraiján',
            'Capira', 'Chame', 'San Carlos'
        ],
        'Metro': [
            'Panamá', 'San Miguelito', 'Balboa', 'Chepo', 'Chimán', 'Taboga',
            'Chepigana', 'Pinogana'
        ],
        'Oeste': [
            'Alanje', 'Barú', 'Boquerón', 'Boquete', 'Bugaba', 'David',
            'Dolega', 'Guacala', 'Remedios', 'Renacimiento', 'San Félix',
            'San Lorenzo', 'Tolé', 'Bocas del Toro', 'Changuinola',
            'Chiriquí Grande', 'Chitré', 'Las Minas', 'Los Pozos', 'Ocú',
            'Parita', 'Pesé', 'Santa María', 'Guararé', 'Las Tablas',
            'Los Santos', 'Macaracas', 'Pedasí', 'Pocrí', 'Tonosí',
            'Atalaya', 'Calobre', 'Cañazas', 'La Mesa', 'Las Palmas',
            'Mariato', 'Montijo', 'Río de Jesús', 'San Francisco',
            'Santa Fé', 'Santiago', 'Soná'
        ]
    },
    # --- AÑADE AQUÍ OTROS PAÍSES ---
    # 'Otro País': {
    #    'RegionX': ['CiudadA', 'CiudadB'],
    #    'RegionY': ['CiudadC']
    # }
    # -----------------------------
}
paises_disponibles = list(CLASIFICACIONES_POR_PAIS.keys())

# --- SELECCIÓN DE PAÍS Y CARGA DE ARCHIVOS ---
col_pais, col_vacia = st.columns([1, 2]) # Columna para el selector
with col_pais:
    pais_seleccionado_display = st.selectbox("Selecciona el País:", paises_disponibles)

st.markdown("### Carga de Archivos Excel")
col1_up, col2_up = st.columns(2)
with col1_up:
    uploaded_file_num = st.file_uploader("Carga el archivo Numérico", type=["xlsx"], key="num")
with col2_up:
    uploaded_file_txt = st.file_uploader("Carga el archivo Textual", type=["xlsx"], key="txt")


# --- LÓGICA DE VALIDACIÓN (Solo si ambos archivos están cargados) ---
if uploaded_file_num is not None and uploaded_file_txt is not None:
    st.info(f"Archivos cargados. Iniciando validación para **{pais_seleccionado_display}**...")
    st.divider()

    # Mapear nombre display a clave interna si es necesario (ej. 'Panamá' a 'panama')
    # En este caso coincide, pero si no, harías:
    # pais_clave_interna = 'panama' if pais_seleccionado_display == 'Panamá' else pais_seleccionado_display.lower()
    pais_clave_interna = pais_seleccionado_display # Usamos el mismo nombre por ahora

    validation_results = [] # Reiniciar resultados

    # --- Carga de DataFrames ---
    try:
        df_numerico_full = pd.read_excel(io.BytesIO(uploaded_file_num.getvalue()))
        df_textual_full = pd.read_excel(io.BytesIO(uploaded_file_txt.getvalue()))
        st.success("Archivos leídos correctamente.")
    except Exception as e:
        st.error(f"Error crítico al leer los archivos Excel: {e}")
        st.stop()

    # --- Optimización ---
    # ... (mismo código de optimización que antes) ...
    columnas_necesarias_numerico = ['Unico', 'lastpage', 'lastpage_Parte2']
    columnas_necesarias_textual = [
        '[auth]', 'startdate',
        "Por favor, selecciona el rango de edad en el que te encuentras:",
        '[age]', 'NSE', 'NSE2',
        'Region 1 (Centro/Metro/Oeste)', 'CIUDAD',
        'Origen', 'Proveedor'
    ]
    cols_existentes_num = [col for col in columnas_necesarias_numerico if col in df_numerico_full.columns]
    cols_existentes_txt = [col for col in columnas_necesarias_textual if col in df_textual_full.columns]
    # Usar try-except por si alguna columna ESENCIAL no está
    try:
        df_numerico = df_numerico_full[cols_existentes_num]
        df_textual = df_textual_full[cols_existentes_txt]
    except KeyError as e:
        st.error(f"Error: La columna esencial {e} no se encontró en uno de los archivos. No se puede continuar.")
        st.stop()


    # --- INICIO VALIDACIONES (Mismo código de validaciones V1 a V8 que antes) ---
    # Copia aquí las definiciones de 'key_vX', 'content_vX', 'status_vX'
    # y los bloques try-except para cada validación (V1 a V8)
    # de la Versión 3.2 que te di antes.
    # No los pego aquí para no hacer la respuesta excesivamente larga,
    # pero asegúrate de copiarlos tal cual.

    # --- VALIDACIONES (PEGAR CÓDIGO V1-V8 DE LA VERSIÓN ANTERIOR AQUÍ) ---

    # --- Validación 1 ---
    key_v1 = "Tamaño de las Bases"
    # ... (código V1) ...
    content_v1 = ""
    status_v1 = "Correcto"
    filas_num, cols_num = df_numerico_full.shape
    filas_txt, cols_txt = df_textual_full.shape
    content_v1 += f"  - Numérica: {filas_num} filas x {cols_num} cols.<br>"
    content_v1 += f"  - Textual:  {filas_txt} filas x {cols_txt} cols.<br><br>"
    content_v1 += "  <b>-- Comparación --</b><br>"
    if filas_num == filas_txt and cols_num == cols_txt:
        content_v1 += "  <span class='status-correcto-inline'>[Correcto]</span> Coinciden."
    else:
        status_v1 = "Incorrecto"; content_v1 += "  <span class='status-incorrecto-inline'>[Incorrecto]</span> Diferentes.<br>"
        if filas_num != filas_txt: content_v1 += "   - Filas.<br>"
        if cols_num != cols_txt: content_v1 += "   - Columnas.<br>"
    validation_results.append({'key': key_v1, 'status': status_v1, 'content': content_v1})

    # --- Validación 2 ---
    key_v2 = "Orden de Códigos Únicos"
    # ... (código V2) ...
    content_v2 = ""
    status_v2 = "Correcto"
    columna_num = 'Unico'; columna_txt = '[auth]'
    try:
        codigos_num = df_numerico[columna_num]; codigos_txt = df_textual[columna_txt]
        if len(codigos_num) != len(codigos_txt):
            status_v2 = "Incorrecto"; content_v2 += f"<span class='status-incorrecto-inline'>[Incorrecto]</span> Filas no coinciden.<br>"
            content_v2 += f"  - Num: {len(codigos_num)}, Txt: {len(codigos_txt)}<br>(Error de V1)"
        elif codigos_num.equals(codigos_txt): content_v2 += f"<span class='status-correcto-inline'>[Correcto]</span> Orden idéntico."
        else:
            status_v2 = "Incorrecto"; content_v2 += f"<span class='status-incorrecto-inline'>[Incorrecto]</span> Códigos/orden no coinciden.<br>"
            diferencias = codigos_num != codigos_txt
            diferencias_data = codigos_txt.loc[diferencias]
            reporte_diferencias = pd.DataFrame({'Fila': diferencias_data.index + 2, f'{columna_txt}': diferencias_data.values})
            content_v2 += f"  - Primeras 5 (Fila y {columna_txt}):<br>" + reporte_diferencias.head().to_html(classes='df-style', index=False)
    except KeyError as e: status_v2 = "Error"; content_v2 += f"<span class='status-error-inline'>[ERROR]</span> Col {e} no encontrada."
    validation_results.append({'key': key_v2, 'status': status_v2, 'content': content_v2})

    # --- Validación 3 ---
    key_v3 = "lastpage y lastpage_Parte2"
    # ... (código V3) ...
    content_v3 = ""; status_v3 = "Correcto"
    cols_v3 = ['lastpage', 'lastpage_Parte2']
    for col in cols_v3:
        content_v3 += f"<br><b>  '{col}':</b><br>";
        if col not in df_numerico.columns: status_v3 = "Error"; content_v3 += f"<span class='status-error-inline'>[ERROR]</span> No encontrada.<br>"; continue
        vals = df_numerico[col].dropna().unique()
        if len(vals) <= 1: content_v3 += f"<span class='status-correcto-inline'>[Correcto]</span> Único valor.<br>"
        else: status_v3 = "Incorrecto"; vals_str = ", ".join(map(str, vals)); content_v3 += f"<span class='status-incorrecto-inline'>[Incorrecto]</span> Múltiples: {vals_str}<br>"
    validation_results.append({'key': key_v3, 'status': status_v3, 'content': content_v3})

    # --- Validación 4 ---
    key_v4 = "Periodo Campo ('startdate')"
    # ... (código V4) ...
    content_v4 = ""; status_v4 = "Info"; col_fecha = 'startdate'
    try:
        try: locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        except: content_v4 += "[WARN] Locale ES no set.<br>"; locale.setlocale(locale.LC_TIME, '')
        if col_fecha not in df_textual.columns: raise KeyError(f"'{col_fecha}' ausente.")
        fechas = pd.to_datetime(df_textual[col_fecha], dayfirst=True, errors='coerce').dropna()
        if not fechas.empty:
            f_min, f_max = fechas.min(), fechas.max()
            content_v4 += f"<b>Periodo:</b><br> - Inicio: {f_min.strftime('%d/%b/%Y %H:%M')}<br> - Fin: {f_max.strftime('%d/%b/%Y %H:%M')}<br>"
        else: status_v4 = "Error"; content_v4 += "<span class='status-error-inline'>[ERROR]</span> No hay fechas.<br>"
    except KeyError as e: status_v4 = "Error"; content_v4 += f"<span class='status-error-inline'>[ERROR]</span> Col {e}.<br>"
    validation_results.append({'key': key_v4, 'status': status_v4, 'content': content_v4})

    # --- Validación 5 ---
    key_v5 = "Agrupaciones"
    # ... (código V5) ...
    content_v5 = ""; status_v5 = "Correcto"
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
    # 5.3 Geografía
    content_v5 += f"<h3>5.3: Geografía ({pais_seleccionado_display})</h3>"; status_v5_3 = "Correcto"
    try:
        # USA la variable seleccionada: pais_clave_interna
        clasif = CLASIFICACIONES_POR_PAIS.get(pais_clave_interna)
        if not clasif: raise ValueError(f"Clasif. no definida para '{pais_seleccionado_display}'")
        col_reg = 'Region 1 (Centro/Metro/Oeste)'; col_ciu = 'CIUDAD'
        if not all(c in df_textual.columns for c in [col_reg, col_ciu]): raise KeyError("Region/Ciudad")
        err_reg = []
        for idx, row in df_textual.iterrows():
            reg, ciu = row[col_reg], row[col_ciu]
            if pd.isna(reg) or pd.isna(ciu): continue
            if reg in clasif:
                if ciu not in clasif[reg]: err_reg.append({'idx': idx + 2, 'Reg': reg, 'Ciu': ciu, 'Err': f"'{ciu}' no en '{reg}'"})
            else: err_reg.append({'idx': idx + 2, 'Reg': reg, 'Ciu': ciu, 'Err': f"'{reg}' no válida"})
        if not err_reg: content_v5 += f"<span class='status-correcto-inline'>[Correcto]</span> Consistente."
        else:
            status_v5_3 = "Incorrecto"; content_v5 += f"<span class='status-incorrecto-inline'>[Incorrecto]</span> {len(err_reg)} inconsistencias.<br>"
            df_err = pd.DataFrame(err_reg); content_v5 += "Primeras 5:<br>" + df_err.head().to_html(classes='df-style', index=False)
    except (KeyError, ValueError) as e: status_v5_3 = "Error"; content_v5 += f"<span class='status-error-inline'>[ERROR]</span> {e}<br>"
    if status_v5 == "Correcto": status_v5 = status_v5_3
    validation_results.append({'key': key_v5, 'status': status_v5, 'content': content_v5})

    # --- Validación 6 ---
    key_v6 = "Origen/Proveedor"
    # ... (código V6) ...
    content_v6 = ""; status_v6 = "Info"; prov_cols = ['Origen', 'Proveedor']
    prov_col = next((col for col in prov_cols if col in df_textual.columns), None)
    if prov_col:
        content_v6 += f"<b>'{prov_col}':</b><br>";
        try:
            cnt = df_textual[prov_col].value_counts(dropna=False).reset_index(); cnt.columns = [prov_col, 'Conteo']
            content_v6 += cnt.to_html(classes='df-style', index=False)
        except Exception as e: status_v6 = "Error"; content_v6 += f"<span class='status-error-inline'>[ERROR]</span> {e}<br>"
    else: content_v6 += f"[INFO] No encontrada."
    validation_results.append({'key': key_v6, 'status': status_v6, 'content': content_v6})

    # --- Validación 7 ---
    key_v7 = "Nulos Base Numérica"
    # ... (código V7) ...
    content_v7 = ""; status_v7 = "Correcto"; id_unico = 'Unico'; cols_v7 = ['NSE', 'gender', 'AGErange', 'Region']
    nulos_det = []; no_enc = []; id_ok = id_unico in df_numerico_full.columns
    if not id_ok: content_v7 += f"<span class='status-error-inline'>[WARN]</span> Col '{id_unico}' no encontrada.<br>"
    for col in cols_v7:
        if col not in df_numerico_full.columns: no_enc.append(col); continue
        nulas = df_numerico_full[df_numerico_full[col].isnull()]; cant = len(nulas)
        if cant > 0:
            ids = nulas[id_unico].tolist() if id_ok else []; nulos_det.append({'col': col, 'cant': cant, 'ids': ids})
    if no_enc: status_v7 = "Error"; content_v7 += f"<span class='status-error-inline'>[ERROR]</span> No encontradas: {', '.join(no_enc)}<br>"
    if nulos_det:
        if status_v7 == "Correcto": status_v7 = "Incorrecto"
        content_v7 += f"<span class='status-incorrecto-inline'>[Incorrecto]</span> Nulos:<br><ul>"
        for item in nulos_det:
            content_v7 += f"<li><b>{item['col']}</b>: {item['cant']}"
            if item['ids']: ids_str = ", ".join(map(str, item['ids'])); content_v7 += f"<br>  - IDs: <b>{ids_str}</b>"
            content_v7 += "</li>"
        content_v7 += "</ul>"
    if status_v7 == "Correcto": content_v7 = f"<span class='status-correcto-inline'>[Correcto]</span> Columnas OK."
    validation_results.append({'key': key_v7, 'status': status_v7, 'content': content_v7})

    # --- Validación 8 ---
    key_v8 = "Abiertas ('Menciona')"
    # ... (código V8) ...
    content_v8 = ""; status_v8 = "Info"
    try:
        id_auth = '[auth]';
        if id_auth not in df_textual_full.columns: raise KeyError(f"'{id_auth}' ausente.")
        cols_m = [c for c in df_textual_full.columns if "menciona" in str(c).lower() and "mencionaste" not in str(c).lower()]
        total_p = len(cols_m)
        if not cols_m: content_v8 = "No hay columnas 'menciona'."
        else:
            melted = df_textual_full[[id_auth] + cols_m].melt(id_vars=[id_auth], var_name='Preg', value_name='Resp').dropna(subset=['Resp'])
            if melted.empty: content_v8 = f"{total_p} columnas, sin respuestas."
            else:
                total_r = len(melted); content_v8 += f"<b>{total_p}</b> cols, <b>{total_r}</b> respuestas.<br><br>"
                df_disp = melted[[id_auth, 'Resp']]
                if total_r > 500: content_v8 += f"(Primeras 500)<br>"; df_disp = df_disp.head(500)
                content_v8 += df_disp.to_html(classes='df-style', index=False)
    except Exception as e: status_v8 = "Error"; content_v8 += f"<span class='status-error-inline'>[ERROR]</span> {e}<br>"
    validation_results.append({'key': key_v8, 'status': status_v8, 'content': content_v8})

    # --- FIN VALIDACIONES ---

    st.success("Proceso de validación terminado.")
    st.divider()

    # --- ÁREA DE REPORTE ESTILIZADO ---

    # 2. Ordenar resultados y asignar números
    sort_order = {'Correcto': 1, 'Incorrecto': 2, 'Error': 3, 'Info': 4}
    sorted_results_temp = sorted(validation_results, key=lambda v: sort_order.get(v['status'], 5))
    final_numbered_results = []
    for i, v in enumerate(sorted_results_temp):
        new_title = f"Validación {i + 1}: {v['key']}"
        final_numbered_results.append({'title': new_title, 'status': v['status'], 'content': v['content']})

    # 3. Calcular el Resumen
    correct_count = sum(1 for v in validation_results if v['status'] == 'Correcto')
    incorrect_count = sum(1 for v in validation_results if v['status'] == 'Incorrecto')
    info_count = sum(1 for v in validation_results if v['status'] == 'Info')
    error_count = sum(1 for v in validation_results if v['status'] == 'Error')
    total_validations = correct_count + incorrect_count + error_count
    correct_pct = (correct_count / total_validations * 100) if total_validations > 0 else 0
    incorrect_pct = (incorrect_count / total_validations * 100) if total_validations > 0 else 0

    # 4. Mostrar el Resumen con st.columns
    st.subheader("--- RESUMEN DE VALIDACIÓN ---", divider='violet') # Usar color violeta
    col1, col2, col3, col4 = st.columns(4)
    # Usar métricas para un look más "dashboard"
    col1.metric("✅ Correctos", f"{correct_count}", f"{correct_pct:.1f}%")
    col2.metric("❌ Incorrectos", f"{incorrect_count}", f"{incorrect_pct:.1f}%")
    col3.metric("⚠️ Errores", f"{error_count}")
    col4.metric("ℹ️ Reportes", f"{info_count}")

    # Lista detallada en un expander
    with st.expander("Ver lista detallada de verificaciones", expanded=False):
        summary_list_html = "<div class='summary-list'><ul>"
        for v in final_numbered_results:
            icon = "✅" if v['status'] == 'Correcto' else "❌" if v['status'] == 'Incorrecto' else "⚠️" if v['status'] == 'Error' else "ℹ️"
            summary_list_html += f"<li>{icon} <strong>{v['title']}:</strong> <span class='status-{v['status'].lower()}-inline'>{v['status']}</span></li>"
        summary_list_html += "</ul></div>"
        st.markdown(summary_list_html, unsafe_allow_html=True)

    st.divider()

    # 5. Mostrar el Reporte Detallado
    st.subheader("--- REPORTE DETALLADO ---", divider='violet') # Usar color violeta
    for v in final_numbered_results:
        status_class = f"status-{v['status'].lower()}"
        # Ajustar contenido para sub-headings de V5
        content_detalle = v['content'].replace("<h3>5.1:", "<h3 class='sub-heading'>5.1:")
        content_detalle = content_detalle.replace("<h3>5.2:", "<h3 class='sub-heading'>5.2:")
        content_detalle = content_detalle.replace("<h3>5.3:", "<h3 class='sub-heading'>5.3:")
        html_content = f"""
        <div class='validation-box {status_class}'>
            <h3>{v['title']}</h3>
            {content_detalle.replace('<br>', '<br/>')}
        </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)

    st.success("¡Validación completada!") # Mensaje final más descriptivo
    # st.balloons() # Opcional: Descomentar si quieres la celebración

else:
    st.info("Por favor, carga ambos archivos Excel para iniciar la validación.")

# --- Footer Opcional (Comentado para cliente interno) ---
# st.markdown("---")
# st.markdown("Desarrollado con ❤️ usando Streamlit")