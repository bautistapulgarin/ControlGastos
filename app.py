import streamlit as st
from supabase import create_client, Client

# ===============================
# Configuración de Supabase
# ===============================
SUPABASE_URL = "https://TU_URL.supabase.co"   # 👈 pon aquí tu URL
SUPABASE_KEY = "TU_API_KEY"                   # 👈 pon aquí tu API KEY

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("✅ App de prueba con Supabase")

# ===============================
# Insertar datos
# ===============================
st.subheader("Insertar un registro")

name = st.text_input("Nombre")
if st.button("Guardar en Supabase"):
    if name.strip() != "":
        try:
            response = supabase.table("test").insert({"name": name}).execute()
            st.success(f"Registro insertado: {response.data}")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Escribe un nombre antes de guardar.")

# ===============================
# Leer datos
# ===============================
st.subheader("Ver registros guardados")
if st.button("Cargar datos"):
    try:
        response = supabase.table("test").select("*").execute()
        st.write(response.data)
    except Exception as e:
        st.error(f"Error: {e}")
