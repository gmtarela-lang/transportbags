import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuración de la página web
st.set_page_config(page_title="Waylogix Business Simulator", layout="wide", page_icon="🎒")

# Estilo personalizado para un look premium
st.markdown("""
    <style>
    .main-title { font-size:32px !important; font-weight: bold; color: #1F4E79; text-align: center; margin-bottom: 30px; }
    .section-title { font-size:20px !important; font-weight: bold; color: #262626; margin-top: 20px; }
    .kpi-box { padding: 20px; background-color: #F2F4F8; border-radius: 10px; border-left: 5px solid #1F4E79; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">WAYLOGIX — SIMULADOR FINANCIERO ESTRATÉGICO</p>', unsafe_allow_html=True)
st.write("Usa el panel de la izquierda para cambiar las variables del negocio y ver el impacto financiero inmediato.")

# ==========================================
# BARRA LATERAL: CONTROL DE VARIABLES (INPUTS)
# ==========================================
st.sidebar.header("🎛️ Variables de Control")

st.sidebar.markdown("### 🌍 Entorno General")
etapas = st.sidebar.slider("Etapas de la ruta (Sarria-Santiago)", min_value=1, max_value=10, value=5)
peregrinos_agencia = st.sidebar.number_input("Peregrinos anuales por agencia", min_value=1000, max_value=50000, value=20000, step=1000)

st.sidebar.markdown("### 💻 Línea 1: Software SaaS")
agencias_saas = st.sidebar.slider("Agencias externas contratando SaaS", min_value=0, max_value=57, value=5)
fee_software = st.sidebar.slider("Fee de software por maleta/etapa (€)", min_value=0.50, max_value=3.00, value=1.00, step=0.10)

st.sidebar.markdown("### 🚚 Línea 2: Transporte Propio")
agencias_transporte = st.sidebar.slider("Volumen transporte propio (equiv. agencias)", min_value=0, max_value=10, value=1)
precio_transporte = st.sidebar.slider("Precio cobrado por maleta/etapa (€)", min_value=4.00, max_value=10.00, value=6.50, step=0.50)
comision_agencia_pct = st.sidebar.slider("Comisión para la agencia aliada (%)", min_value=10, max_value=40, value=20) / 100
coste_ejecucion = st.sidebar.slider("Coste físico de ejecución (combustible/chofer) (€)", min_value=1.00, max_value=5.00, value=2.50, step=0.10)

# ==========================================
# LÓGICA DE CÁLCULO FINANCIERO
# ==========================================
# Cálculos unitarios de transporte
comision_agencia_eur = precio_transporte * comision_agencia_pct
margen_bruto_logistica = precio_transporte - comision_agencia_eur - fee_software
beneficio_neto_unitario_transporte = margen_bruto_logistica - coste_ejecucion

# Volúmenes anuales
servicios_por_agencia = etapas * peregrinos_agencia
total_servicios_saas = servicios_por_agencia * agencias_saas
total_servicios_transporte = servicios_por_agencia * agencias_transporte

# Ingresos y Beneficios Anuales
ingresos_saas = total_servicios_saas * fee_software
ingresos_brutos_transporte = total_servicios_transporte * precio_transporte
beneficio_neto_transporte = total_servicios_transporte * beneficio_neto_unitario_transporte

# Consolidado
ingresos_totales_grupo = ingresos_saas + ingresos_brutos_transporte
ebitda_total_grupo = ingresos_saas + beneficio_neto_transporte

# ==========================================
# DISEÑO DE LA INTERFAZ CENTRAL (OUTPUTS)
# ==========================================

# Fila 1: KPIs Principales
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Facturación Total del Grupo", value=f"{ingresos_totales_grupo:,.2f} €")
with col2:
    st.metric(label="EBITDA / Beneficio Neto Total", value=f"{ebitda_total_grupo:,.2f} €")
with col3:
    margen_consolidado = (ebitda_total_grupo / ingresos_totales_grupo * 100) if ingresos_totales_grupo > 0 else 0
    st.metric(label="Margen del Negocio Combinado", value=f"{margen_consolidado:.1f} %")

st.markdown("---")

# Fila 2: Desglose Unitario y Reparto de Ingresos
col_left, col_right = st.columns(2)

with col_left:
    st.markdown('<p class="section-title">📊 Desglose del Euro de Transporte</p>', unsafe_allow_html=True)
    st.write(f"De los **{precio_transporte:.2f} €** que paga el peregrino por etapa en tu línea propia:")
    st.write(f"* **A la Agencia Aliada (Comisión):** -{comision_agencia_eur:.2f} €")
    st.write(f"* **A la línea de Software Waylogix (Fee):** -{fee_software:.2f} €")
    st.write(f"* **Coste Operativo de Flota (Furgoneta/Gasolina):** -{coste_ejecucion:.2f} €")
    st.markdown(f"🚀 **Beneficio Limpio de Transporte para Waylogix:** **{beneficio_neto_unitario_transporte:.2f} €** por etapa.")

with col_right:
    st.markdown('<p class="section-title">🏢 Rentabilidad por Línea de Negocio</p>', unsafe_allow_html=True)
    df_lineas = pd.DataFrame({
        "Línea de Negocio": ["Software SaaS", "Transporte Propio"],
        "Ingresos Brutos (€)": [ingresos_saas, ingresos_brutos_transporte],
        "Beneficio Neto / EBITDA (€)": [ingresos_saas, beneficio_neto_transporte]
    })
    st.dataframe(df_lineas.style.format({"Ingresos Brutos (€)": "{:,.2f} €", "Beneficio Neto / EBITDA (€)": "{:,.2f} €"}), hide_index=True)

st.markdown("---")

# Fila 3: Gráfico de Estacionalidad Mensual (Plotly)
st.markdown('<p class="section-title">📅 Proyección Mensual y Estacionalidad (Año 1)</p>', unsafe_allow_html=True)

meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
estacionalidad = [0.01, 0.01, 0.04, 0.12, 0.16, 0.16, 0.18, 0.18, 0.14, 0.08, 0.01, 0.01]

beneficios_sw_mes = [ingresos_saas * p for p in estacionalidad]
beneficios_tr_mes = [beneficio_neto_transporte * p for p in estacionalidad]

fig = go.Figure()
fig.add_trace(go.Bar(x=meses, y=beneficios_sw_mes, name="Beneficio Software (SaaS)", marker_color='#1F4E79'))
fig.add_trace(go.Bar(x=meses, y=beneficios_tr_mes, name="Beneficio Neto Transporte", marker_color='#A6ACAF'))

fig.update_layout(
    barmode='stack',
    title="Beneficio Neto Mensual Acumulado por Vía de Ingreso",
    xaxis_title="Meses del Año",
    yaxis_title="Euros (€)",
    legend_title="Líneas de Negocio",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)