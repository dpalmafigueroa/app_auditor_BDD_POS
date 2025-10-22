# --- validador_app.py ---
# Versión 1.0 para Streamlit

import streamlit as st
import pandas as pd
import locale
import io # Para leer los archivos subidos

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title="Validador de Bases Excel")

st.title("📊 Validador de Bases Numérica y Textual")
st.markdown("Sube tus archivos Excel (Numérico y Textual) para iniciar la validación.")

# --- CONFIGURACIÓN FIJA (Puedes moverla a un archivo separado si crece) ---
PAIS_SELECCIONADO = 'panama' # Podrías hacerlo seleccionable con st.selectbox
CLASIFICACIONES_POR_PAIS = {
    'panama': {
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
    }
}

# --- CARGA DE ARCHIVOS ---
uploaded_file_num = st.file_uploader("Carga el archivo Excel Numérico", type=["xlsx"])
uploaded_file_txt = st.file_uploader("Carga el archivo Excel Textual", type=["xlsx"])

# --- LÓGICA DE VALIDACIÓN (Solo si ambos archivos están cargados) ---
if uploaded_file_num is not None and uploaded_file_txt is not None:
    st.info("Archivos cargados. Iniciando validación...")

    # Lista para almacenar los resultados
    validation_results = []

    # --- Carga de DataFrames desde archivos subidos ---
    try:
        # Usamos io.BytesIO para que pandas lea el archivo en memoria
        df_numerico_full = pd.read_excel(io.BytesIO(uploaded_file_num.getvalue()))
        df_textual_full = pd.read_excel(io.BytesIO(uploaded_file_txt.getvalue()))
        st.success("Archivos leídos correctamente.")
    except Exception as e:
        st.error(f"Error crítico al leer los archivos Excel: {e}")
        st.stop() # Detiene la ejecución si no puede leer los archivos

    # --- Optimización de Memoria (Opcional, pero buena práctica) ---
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
    df_numerico = df_numerico_full[cols_existentes_num]
    df_textual = df_textual_full[cols_existentes_txt]

    # --- INICIO DEL ÁREA DE VALIDACIONES ---

    # --- Validación 1: Tamaño de las bases ---
    key_v1 = "Tamaño de las Bases"
    content_v1 = ""
    status_v1 = "Correcto"
    filas_num, cols_num = df_numerico_full.shape
    filas_txt, cols_txt = df_textual_full.shape
    content_v1 += f"  - Dimensiones de la base numérica: {filas_num} filas y {cols_num} columnas.<br>"
    content_v1 += f"  - Dimensiones de la base textual:  {filas_txt} filas y {cols_txt} columnas.<br><br>"
    content_v1 += "  <b>-- Comparación de Dimensiones --</b><br>"
    if filas_num == filas_txt and cols_num == cols_txt:
        content_v1 += "  <span class='status-correcto-inline'>[Correcto]</span> Las bases coinciden en tamaño."
    else:
        status_v1 = "Incorrecto"
        content_v1 += "  <span class='status-incorrecto-inline'>[Incorrecto]</span> Las dimensiones son diferentes.<br>"
        if filas_num != filas_txt: content_v1 += "   - Discrepancia en Filas.<br>"
        if cols_num != cols_txt: content_v1 += "   - Discrepancia en Columnas.<br>"
    validation_results.append({'key': key_v1, 'status': status_v1, 'content': content_v1})

    # --- Validación 2: Verificación de Orden de Códigos Únicos ---
    key_v2 = "Verificación de Orden de Códigos Únicos"
    content_v2 = ""
    status_v2 = "Correcto"
    columna_num = 'Unico'
    columna_txt = '[auth]'
    try:
        codigos_num = df_numerico[columna_num]
        codigos_txt = df_textual[columna_txt]
        if len(codigos_num) != len(codigos_txt):
            status_v2 = "Incorrecto"
            content_v2 += f"<span class='status-incorrecto-inline'>[Incorrecto]</span> El número de filas no coincide.<br>"
            content_v2 += f"  - Filas numéricas ('{columna_num}'): {len(codigos_num)}<br>"
            content_v2 += f"  - Filas textuales ('{columna_txt}'): {len(codigos_txt)}<br>"
        elif codigos_num.equals(codigos_txt):
            content_v2 += f"<span class='status-correcto-inline'>[Correcto]</span> El orden es idéntico."
        else:
            status_v2 = "Incorrecto"
            content_v2 += f"<span class='status-incorrecto-inline'>[Incorrecto]</span> Los códigos o su orden no coinciden.<br>"
            diferencias = codigos_num != codigos_txt
            diferencias_data = codigos_txt.loc[diferencias]
            reporte_diferencias = pd.DataFrame({
                'Numero de Fila (Excel)': diferencias_data.index + 2,
                f'{columna_txt} (Base Textual)': diferencias_data.values
            })
            content_v2 += f"  - Primeras 5 diferencias (Fila y {columna_txt}):<br>"
            # Convertimos el DataFrame a HTML para mostrarlo bonito
            content_v2 += reporte_diferencias.head().to_html(classes='df-style', index=False)
    except KeyError as e:
        status_v2 = "Error"
        content_v2 += f"<span class='status-error-inline'>[ERROR]</span> Columna {e} no encontrada."
    validation_results.append({'key': key_v2, 'status': status_v2, 'content': content_v2})

    # --- Validación 3: lastpage y lastpage_Parte2 ---
    key_v3 = "lastpage y lastpage_Parte2"
    content_v3 = ""
    status_v3 = "Correcto"
    columnas_a_revisar_v3 = ['lastpage', 'lastpage_Parte2']
    for col in columnas_a_revisar_v3:
        content_v3 += f"<br><b>  Revisando columna: '{col}'...</b><br>"
        if col not in df_numerico.columns:
            status_v3 = "Error"
            content_v3 += f"  <span class='status-error-inline'>[ERROR]</span> Columna '{col}' no encontrada.<br>"
            continue
        valores_unicos = df_numerico[col].dropna().unique()
        if len(valores_unicos) <= 1:
            content_v3 += f"  <span class='status-correcto-inline'>[Correcto]</span> Debe haber solo un único valor.<br>"
        else:
            status_v3 = "Incorrecto"
            valores_str = ", ".join(map(str, valores_unicos))
            content_v3 += f"  <span class='status-incorrecto-inline'>[Incorrecto]</span> Hay más de un valor: {valores_str}<br>"
    validation_results.append({'key': key_v3, 'status': status_v3, 'content': content_v3})

    # --- Validación 4: Periodo del campo (Análisis de 'startdate') ---
    key_v4 = "Periodo del Campo (Análisis de 'startdate')"
    content_v4 = ""
    status_v4 = "Info"
    columna_fecha = 'startdate'
    try:
        try: locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        except locale.Error:
            content_v4 += "[ADVERTENCIA] No se pudo usar locale español.<br>"
            locale.setlocale(locale.LC_TIME, '') # Usa el default
        if columna_fecha not in df_textual.columns:
            raise KeyError(f"'{columna_fecha}' no encontrada.")
        fechas = pd.to_datetime(df_textual[columna_fecha], dayfirst=True, errors='coerce')
        fechas_validas = fechas.dropna()
        if not fechas_validas.empty:
            fecha_min, fecha_max = fechas_validas.min(), fechas_validas.max()
            content_v4 += "<b>[INFO] Reporte del periodo:</b><br>"
            content_v4 += f"  - Inicio: {fecha_min.strftime('%d/%b/%Y %H:%M')}<br>"
            content_v4 += f"  - Fin:    {fecha_max.strftime('%d/%b/%Y %H:%M')}<br>"
        else:
            status_v4 = "Error"; content_v4 += "  <span class='status-error-inline'>[ERROR]</span> No hay fechas válidas.<br>"
    except KeyError as e:
        status_v4 = "Error"; content_v4 += f"<span class='status-error-inline'>[ERROR]</span> Columna {e} no encontrada.<br>"
    validation_results.append({'key': key_v4, 'status': status_v4, 'content': content_v4})

    # --- Validación 5: Validación de Agrupaciones ---
    key_v5 = "Validación de Agrupaciones"
    content_v5 = ""
    status_v5 = "Correcto"
    # 5.1 Edad
    content_v5 += "<h3>5.1: Edad vs [age]</h3>"
    col_g_edad = "Por favor, selecciona el rango de edad en el que te encuentras:"
    col_d_edad = '[age]'
    try:
        if not all(c in df_textual.columns for c in [col_g_edad, col_d_edad]): raise KeyError("Edad/[age]")
        reporte_edad = df_textual.groupby(col_g_edad)[col_d_edad].agg(['count', 'min', 'max'])
        reporte_edad.columns = ['Total', 'Min', 'Max']
        content_v5 += reporte_edad.to_html(classes='df-style')
    except KeyError as e: status_v5 = "Error"; content_v5 += f"<span class='status-error-inline'>[ERROR]</span> Faltan columnas: {e}<br>"
    content_v5 += "<hr style='border-top: 1px dotted #ccc;'>"
    # 5.2 NSE
    content_v5 += "<h3>5.2: NSE vs NSE2</h3>"
    col_g_nse = 'NSE'; col_d_nse = 'NSE2'
    try:
        if not all(c in df_textual.columns for c in [col_g_nse, col_d_nse]): raise KeyError("NSE/NSE2")
        reporte_nse = pd.crosstab(df_textual[col_g_nse], df_textual[col_d_nse])
        content_v5 += "Verifica consistencia (una columna por fila):<br>"
        content_v5 += reporte_nse.to_html(classes='df-style')
    except KeyError as e:
        if status_v5 != "Error": status_v5 = "Error"
        content_v5 += f"<span class='status-error-inline'>[ERROR]</span> Faltan columnas: {e}<br>"
    content_v5 += "<hr style='border-top: 1px dotted #ccc;'>"
    # 5.3 Geografía
    content_v5 += "<h3>5.3: Geografía (Región vs Ciudad)</h3>"
    status_v5_3 = "Correcto"
    try:
        clasif = CLASIFICACIONES_POR_PAIS.get(PAIS_SELECCIONADO)
        if not clasif: raise ValueError(f"Clasif. no definida para '{PAIS_SELECCIONADO}'")
        col_reg = 'Region 1 (Centro/Metro/Oeste)'; col_ciu = 'CIUDAD'
        if not all(c in df_textual.columns for c in [col_reg, col_ciu]): raise KeyError("Region/Ciudad")
        errores_reg = []
        for idx, row in df_textual.iterrows():
            reg, ciu = row[col_reg], row[col_ciu]
            if pd.isna(reg) or pd.isna(ciu): continue
            if reg in clasif:
                if ciu not in clasif[reg]: errores_reg.append({'idx': idx + 2, 'Reg': reg, 'Ciu': ciu, 'Err': f"'{ciu}' no en '{reg}'"})
            else: errores_reg.append({'idx': idx + 2, 'Reg': reg, 'Ciu': ciu, 'Err': f"'{reg}' no válida"})
        if not errores_reg: content_v5 += f"<span class='status-correcto-inline'>[Correcto]</span> Agrupación consistente."
        else:
            status_v5_3 = "Incorrecto"
            content_v5 += f"<span class='status-incorrecto-inline'>[Incorrecto]</span> {len(errores_reg)} inconsistencias.<br>"
            df_err_geo = pd.DataFrame(errores_reg)
            content_v5 += "Primeras 5:<br>" + df_err_geo.head().to_html(classes='df-style', index=False)
    except (KeyError, ValueError) as e:
        status_v5_3 = "Error"; content_v5 += f"<span class='status-error-inline'>[ERROR]</span> {e}<br>"
    if status_v5 == "Correcto": status_v5 = status_v5_3
    validation_results.append({'key': key_v5, 'status': status_v5, 'content': content_v5})

    # --- Validación 6: Origen/Proveedor ---
    key_v6 = "Conteo Origen/Proveedor"
    content_v6 = ""
    status_v6 = "Info"
    prov_cols = ['Origen', 'Proveedor']
    prov_col = next((col for col in prov_cols if col in df_textual.columns), None)
    if prov_col:
        content_v6 += f"<b>[INFO] Analizando columna: '{prov_col}'</b><br>"
        try:
            conteo = df_textual[prov_col].value_counts(dropna=False).reset_index()
            conteo.columns = [prov_col, 'Conteo']
            content_v6 += conteo.to_html(classes='df-style', index=False)
        except Exception as e: status_v6 = "Error"; content_v6 += f"<span class='status-error-inline'>[ERROR]</span> {e}<br>"
    else: content_v6 += f"[INFO] No se encontró 'Origen' ni 'Proveedor'."
    validation_results.append({'key': key_v6, 'status': status_v6, 'content': content_v6})

    # --- Validación 7: Nulos Base Numérica ---
    key_v7 = "Nulos en Base Numérica"
    content_v7 = ""
    status_v7 = "Correcto"
    id_unico = 'Unico'
    cols_v7 = ['NSE', 'gender', 'AGErange', 'Region']
    nulos_det = []
    no_enc = []
    id_ok = id_unico in df_numerico_full.columns
    if not id_ok: content_v7 += f"<span class='status-error-inline'>[ADVERTENCIA]</span> Col '{id_unico}' no encontrada.<br>"
    for col in cols_v7:
        if col not in df_numerico_full.columns: no_enc.append(col); continue
        filas_nulas = df_numerico_full[df_numerico_full[col].isnull()]
        cant = len(filas_nulas)
        if cant > 0:
            ids = filas_nulas[id_unico].tolist() if id_ok else []
            nulos_det.append({'col': col, 'cant': cant, 'ids': ids})
    if no_enc: status_v7 = "Error"; content_v7 += f"<span class='status-error-inline'>[ERROR]</span> Columnas no encontradas: {', '.join(no_enc)}<br>"
    if nulos_det:
        if status_v7 == "Correcto": status_v7 = "Incorrecto"
        content_v7 += f"<span class='status-incorrecto-inline'>[Incorrecto]</span> Nulos encontrados:<br><ul>"
        for item in nulos_det:
            content_v7 += f"<li><b>{item['col']}</b>: {item['cant']} nulos"
            if item['ids']: ids_str = ", ".join(map(str, item['ids'])); content_v7 += f"<br>  - IDs ({id_unico}): <b>{ids_str}</b>"
            content_v7 += "</li>"
        content_v7 += "</ul>"
    if status_v7 == "Correcto": content_v7 = f"<span class='status-correcto-inline'>[Correcto]</span> Columnas ({', '.join(cols_v7)}) sin nulos."
    validation_results.append({'key': key_v7, 'status': status_v7, 'content': content_v7})

    # --- Validación 8: Respuestas Abiertas (Menciona) ---
    key_v8 = "Respuestas Abiertas (Menciona)"
    content_v8 = ""
    status_v8 = "Info"
    try:
        id_auth = '[auth]'
        if id_auth not in df_textual_full.columns: raise KeyError(f"'{id_auth}' no encontrado.")
        cols_m = [c for c in df_textual_full.columns if "menciona" in str(c).lower() and "mencionaste" not in str(c).lower()]
        total_p = len(cols_m)
        if not cols_m: content_v8 = "No se encontraron columnas con 'menciona'."
        else:
            melted = df_textual_full[[id_auth] + cols_m].melt(id_vars=[id_auth], var_name='Preg', value_name='Resp').dropna(subset=['Resp'])
            if melted.empty: content_v8 = f"Se analizaron {total_p} columnas, sin respuestas."
            else:
                total_r = len(melted)
                content_v8 += f"<b>[INFO] Reporte:</b><br>"
                content_v8 += f"Se analizaron {total_p} columnas.<br>"
                content_v8 += f"Se encontraron {total_r} respuestas.<br><br>"
                df_disp = melted[[id_auth, 'Resp']]
                if total_r > 500: content_v8 += f"(Primeras 500 de {total_r})<br>"; df_disp = df_disp.head(500)
                content_v8 += df_disp.to_html(classes='df-style', index=False)
    except Exception as e: status_v8 = "Error"; content_v8 += f"<span class='status-error-inline'>[ERROR]</span> {e}<br>"
    validation_results.append({'key': key_v8, 'status': status_v8, 'content': content_v8})

    # --- FIN DEL ÁREA DE VALIDACIONES ---
    st.success("Proceso de validación terminado.")
    st.divider()

    # --- ÁREA DE REPORTE ESTILIZADO ---
    # 1. Definir los estilos CSS (dentro de st.markdown)
    styles = """
    <style>
        .validation-box { border: 1px solid #ddd; border-radius: 8px; padding: 16px; margin-bottom: 15px; font-family: Arial, sans-serif; box-shadow: 0 2px 4px rgba(0,0,0,0.05); line-height: 1.6; }
        .validation-box h3 { margin-top: 0; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 2px solid #eee; }
        .validation-box h3.sub-heading { margin-top: 15px; margin-bottom: 10px; padding-bottom: 5px; font-size: 1.1em; color: #333; border-bottom: 1px solid #eee; }
        /* Correcto */
        .status-correcto { background-color: #E8F5E9; border-left: 5px solid #4CAF50; }
        .status-correcto h3 { color: #1B5E20; }
        .status-correcto-inline { color: #1B5E20; font-weight: bold; }
        /* Incorrecto */
        .status-incorrecto { background-color: #FFEBEE; border-left: 5px solid #F44336; }
        .status-incorrecto h3 { color: #B71C1C; }
        .status-incorrecto-inline { color: #B71C1C; font-weight: bold; }
        /* Info */
        .status-info { background-color: #E3F2FD; border-left: 5px solid #2196F3; }
        .status-info h3 { color: #0D47A1; }
        /* Error */
        .status-error { background-color: #FFF3E0; border-left: 5px solid #FF9800; }
        .status-error h3 { color: #E65100; }
        .status-error-inline { color: #E65100; font-weight: bold; }
        /* Tablas */
        .df-style { border-collapse: collapse; width: 95%; margin: 10px auto; font-size: 0.9em; } /* Ajustado ancho */
        .df-style th, .df-style td { border: 1px solid #ccc; padding: 6px; } /* Menos padding */
        .df-style th { background-color: #f4f4f4; text-align: left; }
        .df-style tr:nth-child(even) { background-color: #f9f9f9; }
        /* Resumen */
        .summary-container { background-color: #fdfdfd; border: 1px solid #ccc; border-radius: 8px; padding: 20px; margin-bottom: 25px; }
        .summary-container h2 { text-align: center; color: #333; margin-top: 0; }
        .summary-list ul { list-style-type: none; padding-left: 0; }
        .summary-list li { padding: 5px; border-bottom: 1px dotted #eee; }
    </style>
    """
    st.markdown(styles, unsafe_allow_html=True)

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
    st.subheader("--- RESUMEN DE VALIDACIÓN ---", divider='rainbow')
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.success(f"✅ Correctos: {correct_count} ({correct_pct:.1f}%)")
    with col2: st.error(f"❌ Incorrectos: {incorrect_count} ({incorrect_pct:.1f}%)")
    with col3: st.warning(f"⚠️ Errores: {error_count}")
    with col4: st.info(f"ℹ️ Reportes: {info_count}")

    with st.expander("Ver lista detallada de verificaciones"):
        summary_list_html = "<div class='summary-list'><ul>"
        for v in final_numbered_results:
            icon = "✅" if v['status'] == 'Correcto' else "❌" if v['status'] == 'Incorrecto' else "⚠️" if v['status'] == 'Error' else "ℹ️"
            summary_list_html += f"<li>{icon} <strong>{v['title']}:</strong> <span class='status-{v['status'].lower()}-inline'>{v['status']}</span></li>"
        summary_list_html += "</ul></div>"
        st.markdown(summary_list_html, unsafe_allow_html=True)

    st.divider()

    # 5. Mostrar el Reporte Detallado
    st.subheader("--- REPORTE DETALLADO ---", divider='rainbow')
    for v in final_numbered_results:
        status_class = f"status-{v['status'].lower()}"
        # Usamos st.markdown para renderizar el HTML
        # Nota: Los <h3> internos se renderizarán como markdown, no con el estilo CSS aplicado a .validation-box h3
        # Para mantener el estilo exacto, se tendría que construir todo el HTML manualmente.
        # Streamlit busca un equilibrio entre facilidad y personalización.
        html_content = f"""
        <div class='validation-box {status_class}'>
            <h3>{v['title']}</h3>
            {v['content'].replace('<br>', '<br/>')}
        </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)

    st.balloons() # ¡Una pequeña celebración al final! 🎉

else:
    st.warning("Por favor, carga ambos archivos Excel para iniciar la validación.")