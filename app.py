import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import json

st.title("📝 Sistema de Pedidos")

# Configurar credenciales desde los secretos
if "google" not in st.secrets:
    st.error("⚠️ No se encontraron los secretos de Google. Configúralos en Settings → Secrets")
    st.stop()

# Crear credenciales
credentials = Credentials.from_service_account_info(
    st.secrets["google"],
    scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
)

# Conectar a Google Sheets
gc = gspread.authorize(credentials)

# Abrir el spreadsheet
spreadsheet_url = st.secrets["google"]["spreadsheet_url"]
try:
    sheet = gc.open_by_url(spreadsheet_url).sheet1
except Exception as e:
    st.error(f"❌ Error al conectar: {e}")
    st.info("Asegurate de que el enlace del spreadsheet sea correcto y que la cuenta de servicio tenga permisos")
    st.stop()

# Leer datos existentes
try:
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
except:
    df = pd.DataFrame(columns=["nombre", "pedido"])

# Mostrar pedidos existentes
st.subheader("📋 Pedidos actuales")
if not df.empty:
    st.dataframe(df)
else:
    st.info("No hay pedidos aún")

# Formulario para nuevos pedidos
st.divider()
st.subheader("➕ Nuevo pedido")

with st.form("pedido_form"):
    nombre = st.text_input("👤 Tu nombre")
    pedido = st.text_area("📦 Tu pedido")
    enviar = st.form_submit_button("📤 Enviar pedido")

if enviar:
    if nombre and pedido:
        # Agregar nueva fila
        nueva_fila = [nombre, pedido]
        sheet.append_row(nueva_fila)
        st.success(f"✅ ¡Gracias {nombre}! Pedido guardado.")
        st.balloons()
        st.rerun()
    else:
        st.warning("Completá ambos campos")