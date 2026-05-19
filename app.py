import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

st.title("📝 Sistema de Pedidos")

# Configurar credenciales desde los secretos
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Obtener credenciales del secreto
creds_dict = dict(st.secrets["google"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

# Conectar a Google Sheets
client = gspread.authorize(creds)

# Abrir el spreadsheet por URL
sheet_url = st.secrets["google"]["spreadsheet_url"]
sheet = client.open_by_url(sheet_url).sheet1

# Leer datos
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Mostrar datos
st.subheader("📋 Pedidos actuales")
st.dataframe(df)

# Formulario para nuevo pedido
st.divider()
st.subheader("➕ Nuevo pedido")

with st.form("nuevo_pedido"):
    nombre = st.text_input("Nombre")
    pedido = st.text_area("Pedido")
    enviar = st.form_submit_button("Enviar")

if enviar and nombre and pedido:
    # Agregar nueva fila
    sheet.append_row([nombre, pedido])
    st.success("✅ Pedido guardado!")
    st.balloons()
    st.rerun()