import streamlit as st
from supabase import create_client

# ----------------------------
# Configuración Supabase
# ----------------------------
SUPABASE_URL = st.secrets["supabase"]["https://esylrswnfmjeoivxtmsp.supabase.co"]
SUPABASE_KEY = st.secrets["supabase"]["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVzeWxyc3duZm1qZW9pdnh0bXNwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTkxNzQ0NjgsImV4cCI6MjA3NDc1MDQ2OH0.oWqMpRJKqVOLw4n8byd5rv_k-dKfxynhGghrKCgcDGk"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ----------------------------
# UI Streamlit
# ----------------------------
st.title("Prueba con Supabase 🚀")

nombre = st.text_input("Nombre")
edad = st.number_input("Edad", min_value=0, step=1)

if st.button("Guardar en Supabase"):
    data = {"nombre": nombre, "edad": edad}
    response = supabase.table("personas").insert(data).execute()
    if response.data:
        st.success("✅ Registro guardado en Supabase")
    else:
        st.error(f"❌ Error: {response}")

if st.button("Leer registros"):
    response = supabase.table("personas").select("*").execute()
    if response.data:
        st.write(response.data)
    else:
        st.warning("No hay datos todavía.")
