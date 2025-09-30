import streamlit as st
from supabase import create_client
from datetime import datetime

# ----------------------------
# Configuración Supabase
# ----------------------------
SUPABASE_URL = st.secrets["supabase"]["url"]
SUPABASE_KEY = st.secrets["supabase"]["key"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ----------------------------
# UI Streamlit
# ----------------------------
st.title("Registro de Gastos y Datos de Personas 🚀")

# Formulario para ingresar datos
with st.form("form_registro"):
    fecha = st.date_input("Fecha", value=datetime.today())
    tipo = st.selectbox("Tipo", ["Ingreso", "Gasto"])
    monto = st.number_input("Monto", min_value=0.0, step=0.01)
    categoria = st.text_input("Categoría")
    subcategoria = st.text_input("Subcategoría")
    metodo = st.selectbox("Método", ["Efectivo", "Transferencia", "Tarjeta", "Otro"])
    responsable = st.text_input("Responsable")
    descripcion = st.text_area("Descripción")
    cuenta = st.text_input("Cuenta")
    estado = st.selectbox("Estado", ["Pendiente", "Aprobado", "Rechazado"])

    submitted = st.form_submit_button("Guardar en Supabase")

    if submitted:
        data = {
            "fecha": fecha.isoformat(),
            "tipo": tipo,
            "monto": monto,
            "categoria": categoria,
            "subcategoria": subcategoria,
            "metodo": metodo,
            "responsable": responsable,
            "descripcion": descripcion,
            "cuenta": cuenta,
            "estado": estado
        }
        try:
            response = supabase.table("personas").insert([data]).execute()
            if response.data:
                st.success("✅ Registro guardado en Supabase")
            else:
                st.error(f"❌ Error al guardar: {response}")
        except Exception as e:
            st.error(f"❌ Error inesperado: {e}")

# Botón para leer registros
if st.button("Leer registros"):
    try:
        response = supabase.table("personas").select("*").execute()
        if response.data:
            st.write(response.data)
        else:
            st.warning("⚠️ No hay registros todavía.")
    except Exception as e:
        st.error(f"❌ Error al leer: {e}")
