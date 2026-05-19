import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Pedidos - DeliRomá", page_icon="📝")
st.title("📝 Sistema de Pedidos")
st.markdown("Completá el formulario para hacer tu pedido")

# Conectar a Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Leer datos existentes
try:
    datos = conn.read(worksheet="Sheet1")
    datos = datos.dropna(how="all")
except:
    datos = pd.DataFrame()

# Formulario
with st.form(key="pedido_form"):
    nombre = st.text_input("👤 Tu nombre")
    pedido = st.text_area("📦 Tu pedido")
    enviar = st.form_submit_button("📤 Enviar pedido")

if enviar:
    if nombre and pedido:
        nuevo = pd.DataFrame([{"nombre": nombre, "pedido": pedido}])
        datos_actualizados = pd.concat([datos, nuevo], ignore_index=True)
        conn.update(worksheet="Sheet1", data=datos_actualizados)
        st.success(f"✅ ¡Gracias {nombre}! Pedido guardado.")
        st.balloons()
        st.rerun()
    else:
        st.warning("Completá ambos campos")