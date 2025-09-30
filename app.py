import streamlit as st
from supabase import create_client
from datetime import datetime  # 🔹 IMPORTANTE

# ----------------------------
# Configuración Supabase
# ----------------------------
SUPABASE_URL = st.secrets["supabase"]["url"]
SUPABASE_KEY = st.secrets["supabase"]["key"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ----------------------------
# Función principal
# ----------------------------
def main():
    st.title("Registro de Gastos y Datos de Personas 🚀")

    # Formulario para ingresar datos
    with st.form("form_registro"):
        Fecha = st.date_input("Fecha", value=datetime.today())
        Tipo = st.selectbox("Tipo", ["Ingreso", "Gasto"])
        Monto = st.number_input("Monto", min_value=0.0, step=0.01)
        Categoria = st.text_input("Categoría")
        Subcategoria = st.text_input("Subcategoría")
        CategoriaMercado = st.text_input("Categoría de Mercado")  # 🔹 Nuevo campo
        Metodo = st.selectbox("Método", ["Efectivo", "Transferencia", "Tarjeta", "Otro"])
        Responsable = st.text_input("Responsable")
        Descripcion = st.text_area("Descripción")
        Cuenta = st.text_input("Cuenta")
        Estado = st.selectbox("Estado", ["Pendiente", "Aprobado", "Rechazado"])

        submitted = st.form_submit_button("Guardar en Supabase")

        if submitted:
            data = {
                "Fecha": Fecha.isoformat(),
                "Tipo": Tipo,
                "Monto": Monto,
                "Categoria": Categoria,
                "Subcategoria": Subcategoria,
                "CategoriaMercado": CategoriaMercado,
                "Metodo": Metodo,
                "Responsable": Responsable,
                "Descripcion": Descripcion,
                "Cuenta": Cuenta,
                "Estado": Estado
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

# ----------------------------
# Ejecutar la app
# ----------------------------
if __name__ == "__main__":
    main()
