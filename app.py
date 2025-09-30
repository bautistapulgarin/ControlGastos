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
# Diccionario Categoría -> Subcategorías
# ----------------------------
categorias = {
    "Alimentación": [
        "Frutas y verduras",
        "Panadería / repostería",
        "Restaurante / comida rápida",
        "Comida para llevar / delivery",
        "Snacks / café / bebidas",
        "Bebidas alcohólicas",
        "Otros alimentos especiales (orgánicos, dietéticos, suplementos)"
    ],
    "Transporte": [
        "Gasolina / combustible",
        "Transporte público (bus, metro, SITP, tren)",
        "Taxi / Uber / apps de transporte",
        "Mantenimiento de vehículo (aceite, revisión, reparaciones)",
        "Seguros de vehículo",
        "Peajes / parqueaderos",
        "Estacionamiento mensual / mensualidad de transporte",
        "Bicicleta / patineta / movilidad eléctrica"
    ]
    # ... agrega las demás categorías como antes
}

# ----------------------------
# Inicializar session_state para categoría/subcategoría
# ----------------------------
if "Categoria" not in st.session_state:
    st.session_state.Categoria = ""
if "Subcategoria" not in st.session_state:
    st.session_state.Subcategoria = ""

# ----------------------------
# Función principal
# ----------------------------
st.title("Registro de Gastos con Subcategorías Dependientes 🚀")

# Selección de categoría
Categoria = st.selectbox("Categoría", list(categorias.keys()), index=0)
if Categoria != st.session_state.Categoria:
    st.session_state.Categoria = Categoria
    st.session_state.Subcategoria = categorias[Categoria][0]  # reinicia subcategoría al cambiar categoría

# Selección de subcategoría
Subcategoria = st.selectbox(
    "Subcategoría",
    categorias[st.session_state.Categoria],
    index=categorias[st.session_state.Categoria].index(st.session_state.Subcategoria)
)
st.session_state.Subcategoria = Subcategoria

# Otros campos
Fecha = st.date_input("Fecha", value=datetime.today())
Tipo = st.selectbox("Tipo", ["Ingreso", "Gasto"])
Monto = st.number_input("Monto", min_value=0.0, step=0.01)
CategoriaMercado = st.text_input("Categoría de Mercado")
Metodo = st.selectbox("Método", ["Efectivo", "Transferencia", "Tarjeta", "Otro"])
Responsable = st.text_input("Responsable")
Descripcion = st.text_area("Descripción")
Cuenta = st.text_input("Cuenta")
Estado = st.selectbox("Estado", ["Pendiente", "Aprobado", "Rechazado"])

# Botón de guardar
if st.button("Guardar en Supabase"):
    data = {
        "Fecha": Fecha.isoformat(),
        "Tipo": Tipo,
        "Monto": Monto,
        "Categoria": st.session_state.Categoria,
        "Subcategoria": st.session_state.Subcategoria,
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
