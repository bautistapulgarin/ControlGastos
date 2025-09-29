import streamlit as st
from supabase import create_client, Client

# ==============================
# CONFIGURACIÓN DE SUPABASE (usa secrets en Streamlit)
# ==============================
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ==============================
# INTERFAZ EN STREAMLIT
# ==============================
st.title("📊 Control de Gastos - Personas")

with st.form("formulario_personas"):
    nombre = st.text_input("Nombre")
    edad = st.number_input("Edad", min_value=1, max_value=120, step=1)
    submit = st.form_submit_button("Guardar en Supabase")

# ==============================
# INSERCIÓN EN TABLA
# ==============================
if submit:
    try:
        data = {
            "nombre": nombre,
            "edad": int(edad)
        }
        
        response = supabase.table("personas").insert(data).execute()

        if hasattr(response, "data") and response.data:
            st.success("✅ Registro guardado correctamente")
            st.json(response.data)
        else:
            st.warning("⚠️ No se insertó ningún dato. Revisa los valores.")

    except Exception as e:
        st.error(f"❌ Error al insertar en Supabase: {str(e)}")
