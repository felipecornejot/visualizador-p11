import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from io import BytesIO
import requests

# --- Paleta de Colores ---
# Definición de colores en formato RGB (0-1) para Matplotlib
color_primario_1_rgb = (14/255, 69/255, 74/255) # 0E454A (Oscuro)
color_primario_2_rgb = (31/255, 255/255, 95/255) # 1FFF5F (Verde vibrante)
color_primario_3_rgb = (255/255, 255/255, 255/255) # FFFFFF (Blanco)

# Colores del logo de Sustrend para complementar
color_sustrend_1_rgb = (0/255, 155/255, 211/255) # 009BD3 (Azul claro)
color_sustrend_2_rgb = (0/255, 140/255, 207/255) # 008CCF (Azul medio)
color_sustrend_3_rgb = (0/255, 54/255, 110/255) # 00366E (Azul oscuro)

# Selección de colores para los gráficos
colors_for_charts = [color_primario_1_rgb, color_primario_2_rgb, color_sustrend_1_rgb, color_sustrend_3_rgb]

# --- Configuración de la página de Streamlit ---
st.set_page_config(layout="wide")

st.title('✨ Visualizador de Impactos - Proyecto P11')
st.subheader('Consorcios microbianos para la restauración de suelos agrícolas degradados')
st.markdown("""
    Ajusta los parámetros para explorar cómo las proyecciones de impacto ambiental y económico del proyecto
    varían con diferentes escenarios de superficie tratada, incremento de carbono orgánico y reducción de agua.
""")

# --- 1. Datos del Proyecto (Línea Base) ---
# Datos de línea base extraídos de la ficha técnica P11.docx
# NOTA: Para este proyecto, el "valor_base_ficha_ejemplo" representa una situación sin la implementación
# del proyecto o un valor previo.
data_p11 = {
    "indicador": [
        "CO₂ capturado (tCO₂e/año)",
        "Agua ahorrada (m³/año)",
        "Agroquímicos evitados (ton/año)",
        "Ingresos generados (CLP/año)"
    ],
    "unidad": ["tCO₂e/año", "m³/año", "ton/año", "CLP/año"],
    "valor_base_ficha_ejemplo": [
        70,     # Valor de CO2 capturado sin el proyecto (o un valor de referencia bajo)
        7000,   # Consumo de agua previo (para calcular ahorro)
        3,      # Uso de agroquímicos previo (para calcular evitación)
        18000000 # Ingresos de referencia
    ]
}

df_diagnostico_p11 = pd.DataFrame(data_p11)

# --- 2. Widgets Interactivos para Parámetros (Streamlit) ---
st.sidebar.header('Parámetros de Simulación')

superficie_ha = st.sidebar.slider(
    'Superficie Tratada (ha):',
    min_value=10,
    max_value=200,
    value=35,
    step=10,
    help="Superficie agrícola en hectáreas tratada con los consorcios microbianos."
)

incremento_c_org = st.sidebar.slider(
    'Incremento de Carbono Orgánico (ton C/ha):',
    min_value=0.5,
    max_value=1.0,
    value=0.8,
    step=0.1,
    help="Aumento anual de carbono orgánico en el suelo por hectárea."
)

consumo_riego = st.sidebar.slider(
    'Consumo Base de Riego (m³/ha):',
    min_value=3000,
    max_value=6000,
    value=5000,
    step=500,
    help="Consumo de agua para riego por hectárea sin el proyecto."
)

reduccion_agua = st.sidebar.slider(
    'Reducción de Agua Esperada (%):',
    min_value=0.1,
    max_value=0.25,
    value=0.2,
    step=0.01,
    format='%.1f%%',
    help="Porcentaje de reducción en el consumo de agua de riego gracias al proyecto."
)

volumen_produccion = st.sidebar.slider(
    'Volumen de Producción Tratada (ton/año):',
    min_value=100,
    max_value=500,
    value=300,
    step=20,
    help="Volumen anual de producción agrícola beneficiada por la aplicación de los consorcios."
)

sustitucion_fertilizantes = st.sidebar.slider(
    'Tasa de Sustitución de Fertilizantes (%):',
    min_value=0.1,
    max_value=0.3,
    value=0.2,
    step=0.01,
    format='%.1f%%',
    help="Porcentaje de fertilizantes sintéticos que pueden ser sustituidos por el bioinsumo."
)

precio_bioinsumo = st.sidebar.slider(
    'Precio Bioinsumo (CLP/ton):',
    min_value=2000000,
    max_value=5000000,
    value=3000000,
    step=100000,
    help="Precio de venta estimado del bioinsumo por tonelada."
)

# --- 3. Cálculos de Indicadores ---

co2_capturado = superficie_ha * incremento_c_org * 3.67
agua_ahorrada = superficie_ha * consumo_riego * reduccion_agua
agroquimicos_ev = volumen_produccion * sustitucion_fertilizantes
ingresos_generados = agroquimicos_ev * precio_bioinsumo
alianzas_estrategicas = 4 # Valor fijo según el script original
inversion_id = 150_000_000 # Valor fijo según el script original

st.header('Resultados Proyectados Anuales:')

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="🌳 **CO₂ Capturado**", value=f"{co2_capturado:.2f} tCO₂e")
    st.caption("Cantidad de dióxido de carbono equivalente capturado anualmente.")
with col2:
    st.metric(label="💧 **Agua Ahorrada**", value=f"{agua_ahorrada:.2f} m³")
    st.caption("Volumen de agua ahorrada en el riego agrícola.")
with col3:
    st.metric(label="🧪 **Agroquímicos Evitados**", value=f"{agroquimicos_ev:.2f} ton")
    st.caption("Cantidad de agroquímicos sintéticos cuyo uso se evita.")

col4, col5 = st.columns(2)

with col4:
    st.metric(label="💰 **Ingresos Generados**", value=f"CLP {ingresos_generados:,.2f}")
    st.caption("Ingresos adicionales generados por la venta del bioinsumo.")
with col5:
    st.metric(label="🤝 **Alianzas Estratégicas**", value=f"{alianzas_estrategicas}")
    st.caption("Número de alianzas estratégicas establecidas.")

st.markdown("---")

st.header('📊 Análisis Gráfico de Impactos')

# --- Visualización (Gráficos 2D con Matplotlib) ---
# Cálculo de valores de línea base para los gráficos
base_co2 = df_diagnostico_p11.loc[df_diagnostico_p11['indicador'] == "CO₂ capturado (tCO₂e/año)", 'valor_base_ficha_ejemplo'].iloc[0]
base_agua = df_diagnostico_p11.loc[df_diagnostico_p11['indicador'] == "Agua ahorrada (m³/año)", 'valor_base_ficha_ejemplo'].iloc[0]
base_agroquimicos = df_diagnostico_p11.loc[df_diagnostico_p11['indicador'] == "Agroquímicos evitados (ton/año)", 'valor_base_ficha_ejemplo'].iloc[0]
base_ingresos = df_diagnostico_p11.loc[df_diagnostico_p11['indicador'] == "Ingresos generados (CLP/año)", 'valor_base_ficha_ejemplo'].iloc[0]


# Creamos una figura con 3 subplots (2D)
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 7), facecolor=color_primario_3_rgb)
fig.patch.set_facecolor(color_primario_3_rgb)

# Definición de etiquetas y valores para los gráficos de barras 2D
labels = ['Línea Base', 'Proyección']
bar_width = 0.6
x = np.arange(len(labels))

# --- Gráfico 1: CO₂ Capturado (tCO₂e/año) ---
co2_values = [base_co2, co2_capturado]
bars1 = ax1.bar(x, co2_values, width=bar_width, color=[colors_for_charts[0], colors_for_charts[1]])
ax1.set_ylabel('tCO₂e/año', fontsize=12, color=colors_for_charts[3])
ax1.set_title('CO₂ Capturado', fontsize=14, color=colors_for_charts[3], pad=20)
ax1.set_xticks(x)
ax1.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax1.yaxis.set_tick_params(colors=colors_for_charts[0])
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.tick_params(axis='x', length=0)
# Ajuste dinámico del ylim
max_co2_val = max(co2_values)
ax1.set_ylim(bottom=0, top=max(max_co2_val * 1.15, 1)) # Asegura al menos 1 tCO2e si es muy bajo
for bar in bars1:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, round(yval, 2), ha='center', va='bottom', color=colors_for_charts[0])

# --- Gráfico 2: Agua Ahorrada (m³/año) ---
agua_values = [base_agua, agua_ahorrada]
bars2 = ax2.bar(x, agua_values, width=bar_width, color=[colors_for_charts[2], colors_for_charts[3]])
ax2.set_ylabel('m³/año', fontsize=12, color=colors_for_charts[0])
ax2.set_title('Agua Ahorrada', fontsize=14, color=colors_for_charts[3], pad=20)
ax2.set_xticks(x)
ax2.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax2.yaxis.set_tick_params(colors=colors_for_charts[0])
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.tick_params(axis='x', length=0)
# Ajuste dinámico del ylim
max_agua_val = max(agua_values)
ax2.set_ylim(bottom=0, top=max(max_agua_val * 1.15, 1)) # 15% de margen superior o mínimo 1 m3
for bar in bars2:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, round(yval, 2), ha='center', va='bottom', color=colors_for_charts[0])

# --- Gráfico 3: Ingresos Generados (CLP/año) ---
ingresos_values = [base_ingresos, ingresos_generados]
bars3 = ax3.bar(x, ingresos_values, width=bar_width, color=[colors_for_charts[1], colors_for_charts[0]])
ax3.set_ylabel('CLP/año', fontsize=12, color=colors_for_charts[3])
ax3.set_title('Ingresos Generados', fontsize=14, color=colors_for_charts[3], pad=20)
ax3.set_xticks(x)
ax3.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax3.yaxis.set_tick_params(colors=colors_for_charts[0])
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.tick_params(axis='x', length=0)
# Ajuste dinámico del ylim
max_ingresos_val = max(ingresos_values)
ax3.set_ylim(bottom=0, top=max(max_ingresos_val * 1.15, 1000000)) # 15% de margen superior o mínimo 1.000.000 CLP
for bar in bars3:
    yval = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"CLP {yval:,.0f}", ha='center', va='bottom', color=colors_for_charts[0])

plt.tight_layout(rect=[0, 0.05, 1, 0.95])
st.pyplot(fig)

# --- Funcionalidad de descarga de cada gráfico ---
st.markdown("---")
st.subheader("Descargar Gráficos Individualmente")

# Función auxiliar para generar el botón de descarga
def download_button(fig, filename_prefix, key):
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=300)
    st.download_button(
        label=f"Descargar {filename_prefix}.png",
        data=buf.getvalue(),
        file_name=f"{filename_prefix}.png",
        mime="image/png",
        key=key
    )

# Crear figuras individuales para cada gráfico para poder descargarlas
# Figura 1: CO₂ Capturado
fig_co2, ax_co2 = plt.subplots(figsize=(8, 6), facecolor=color_primario_3_rgb)
ax_co2.bar(x, co2_values, width=bar_width, color=[colors_for_charts[0], colors_for_charts[1]])
ax_co2.set_ylabel('tCO₂e/año', fontsize=12, color=colors_for_charts[3])
ax_co2.set_title('CO₂ Capturado', fontsize=14, color=colors_for_charts[3], pad=20)
ax_co2.set_xticks(x)
ax_co2.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax_co2.yaxis.set_tick_params(colors=colors_for_charts[0])
ax_co2.spines['top'].set_visible(False)
ax_co2.spines['right'].set_visible(False)
ax_co2.tick_params(axis='x', length=0)
ax_co2.set_ylim(bottom=0, top=max(max_co2_val * 1.15, 1))
for bar in ax_co2.patches:
    yval = bar.get_height()
    ax_co2.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, round(yval, 2), ha='center', va='bottom', color=colors_for_charts[0])
plt.tight_layout()
download_button(fig_co2, "CO2_Capturado", "download_co2")
plt.close(fig_co2)

# Figura 2: Agua Ahorrada
fig_agua, ax_agua = plt.subplots(figsize=(8, 6), facecolor=color_primario_3_rgb)
ax_agua.bar(x, agua_values, width=bar_width, color=[colors_for_charts[2], colors_for_charts[3]])
ax_agua.set_ylabel('m³/año', fontsize=12, color=colors_for_charts[0])
ax_agua.set_title('Agua Ahorrada', fontsize=14, color=colors_for_charts[3], pad=20)
ax_agua.set_xticks(x)
ax_agua.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax_agua.yaxis.set_tick_params(colors=colors_for_charts[0])
ax_agua.spines['top'].set_visible(False)
ax_agua.spines['right'].set_visible(False)
ax_agua.tick_params(axis='x', length=0)
ax_agua.set_ylim(bottom=0, top=max(max_agua_val * 1.15, 1))
for bar in ax_agua.patches:
    yval = bar.get_height()
    ax_agua.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, round(yval, 2), ha='center', va='bottom', color=colors_for_charts[0])
plt.tight_layout()
download_button(fig_agua, "Agua_Ahorrada", "download_agua")
plt.close(fig_agua)

# Figura 3: Ingresos Generados
fig_ingresos, ax_ingresos = plt.subplots(figsize=(8, 6), facecolor=color_primario_3_rgb)
ax_ingresos.bar(x, ingresos_values, width=bar_width, color=[colors_for_charts[1], colors_for_charts[0]])
ax_ingresos.set_ylabel('CLP/año', fontsize=12, color=colors_for_charts[3])
ax_ingresos.set_title('Ingresos Generados', fontsize=14, color=colors_for_charts[3], pad=20)
ax_ingresos.set_xticks(x)
ax_ingresos.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax_ingresos.yaxis.set_tick_params(colors=colors_for_charts[0])
ax_ingresos.spines['top'].set_visible(False)
ax_ingresos.spines['right'].set_visible(False)
ax_ingresos.tick_params(axis='x', length=0)
ax_ingresos.set_ylim(bottom=0, top=max(max_ingresos_val * 1.15, 1000000))
for bar in ax_ingresos.patches:
    yval = bar.get_height()
    ax_ingresos.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"CLP {yval:,.0f}", ha='center', va='bottom', color=colors_for_charts[0])
plt.tight_layout()
download_button(fig_ingresos, "Ingresos_Generados", "download_ingresos")
plt.close(fig_ingresos)

st.markdown("---")
st.markdown("### Información Adicional:")
st.markdown(f"- **Estado de Avance y Recomendaciones:** El proyecto se encuentra en una etapa intermedia de desarrollo, con avances significativos en la fase de validación agronómica en cultivos de tomates y cítricos. Se ha logrado establecer una línea base de medición en suelos degradados, permitiendo estimar incrementos en el contenido de carbono orgánico del suelo y mejoras en su estructura física e hídrica.")

st.markdown("---")
# Texto de atribución centrado
st.markdown("<div style='text-align: center;'>Visualizador Creado por el equipo Sustrend SpA en el marco del Proyecto TT GREEN Foods</div>", unsafe_allow_html=True)

# Aumentar el espaciado antes de los logos
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- Mostrar Logos ---
col_logos_left, col_logos_center, col_logos_right = st.columns([1, 2, 1])

with col_logos_center:
    sustrend_logo_url = "https://drive.google.com/uc?id=1vx_znPU2VfdkzeDtl91dlpw_p9mmu4dd"
    ttgreenfoods_logo_url = "https://drive.google.com/uc?id=1uIQZQywjuQJz6Eokkj6dNSpBroJ8tQf8"

    try:
        sustrend_response = requests.get(sustrend_logo_url)
        sustrend_response.raise_for_status()
        sustrend_image = Image.open(BytesIO(sustrend_response.content))

        ttgreenfoods_response = requests.get(ttgreenfoods_logo_url)
        ttgreenfoods_response.raise_for_status()
        ttgreenfoods_image = Image.open(BytesIO(ttgreenfoods_response.content))

        st.image([sustrend_image, ttgreenfoods_image], width=100)
    except requests.exceptions.RequestException as e:
        st.error(f"Error al cargar los logos desde las URLs. Por favor, verifica los enlaces: {e}")
    except Exception as e:
        st.error(f"Error inesperado al procesar las imágenes de los logos: {e}")

st.markdown("<div style='text-align: center; font-size: small; color: gray;'>Viña del Mar, Valparaíso, Chile</div>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown(f"<div style='text-align: center; font-size: smaller; color: gray;'>Versión del Visualizador: 1.8</div>", unsafe_allow_html=True)
st.sidebar.markdown(f"<div style='text-align: center; font-size: x-small; color: lightgray;'>Desarrollado con Streamlit</div>", unsafe_allow_html=True)
