import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

st.set_page_config(page_title="Control de Gastos", layout="wide")
st.title("💰 Control de Gastos")

# ==============================
# 1. Conectar con Google Sheets
# ==============================
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

client = gspread.authorize(creds)

# Cambia por la URL de tu hoja de Google Sheets
SHEET_URL = "https://docs.google.com/spreadsheets/d/XXXXXXXXXXXX/edit"
sheet = client.open_by_url(SHEET_URL).sheet1

# ==============================
# 2. Entrada de datos
# ==============================
col1, col2 = st.columns([3, 1])

with col1:
    dato = st.text_input("✍️ Ingrese el gasto o dato:")

with col2:
    if st.button("Guardar"):
        if dato.strip():
            sheet.append_row([dato])
            st.success("✅ Registro guardado correctamente")
        else:
            st.warning("⚠️ Escriba un dato antes de guardar")

# ==============================
# 3. Mostrar historial
# ==============================
registros = sheet.get_all_values()

if registros:
    df = pd.DataFrame(registros[1:], columns=registros[0]) if len(registros) > 1 else pd.DataFrame(registros)
    st.subheader("📊 Historial de registros")
    st.dataframe(df, use_container_width=True)
else:
    st.info("No hay registros aún.")
