import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.title("📝 Pedidos")

# Conexión
conn = st.connection("gsheets", type=GSheetsConnection)

# Leer datos
df = conn.read(worksheet="Sheet1")
st.write("Datos actuales:", df)

# Formulario
with st.form("form"):
    nombre = st.text_input("Nombre")
    pedido = st.text_input("Pedido")
    submit = st.form_submit_button("Guardar")

if submit:
    nuevo = pd.DataFrame({"nombre": [nombre], "pedido": [pedido]})
    df_nuevo = pd.concat([df, nuevo], ignore_index=True)
    conn.update(worksheet="Sheet1", data=df_nuevo)
    st.success("Guardado!")
    st.rerun()