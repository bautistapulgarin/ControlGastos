import streamlit as st
from supabase import create_client
from datetime import date

# ----------------------------
# Conexión Supabase
# ----------------------------
SUPABASE_URL = st.secrets["supabase"]["url"]
SUPABASE_KEY = st.secrets["supabase"]["key"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ----------------------------
# Categorías y Subcategorías
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
    ],
    "Servicios": [
        "Luz / electricidad",
        "Agua / acueducto",
        "Gas",
        "Internet / datos móviles",
        "Telefonía fija / celular",
        "TV por cable / streaming",
        "Suscripciones digitales (Netflix, Spotify, software, apps)",
        "Limpieza / aseo (servicios domésticos)",
        "Seguridad / alarma / vigilancia"
    ],
    "Salud": [
        "Medicamentos",
        "Consulta médica general",
        "Especialistas (odontología, dermatología, oftalmología…)",
        "Exámenes médicos / laboratorio",
        "Gimnasio / actividades físicas",
        "Seguros de salud",
        "Terapias (psicológica, fisioterapia, etc.)",
        "Equipos o productos de salud (mascarillas, termómetros, vitaminas)"
    ],
    "Educación": [
        "Matrícula / colegiatura",
        "Libros / material didáctico",
        "Cursos / talleres / seminarios",
        "Software educativo / apps educativas"
    ],
    "Ocio / Entretenimiento": [
        "Cine / teatro / conciertos",
        "Deportes / hobbies",
        "Salidas / viajes / excursiones",
        "Videojuegos / apps de entretenimiento",
        "Cafés / bares / restaurantes sociales",
        "Libros, revistas, periódicos",
        "Suscripciones de ocio (streaming de películas, música, podcasts)"
    ],
    "Ahorro / Inversión": [
        "Cuenta de ahorro",
        "Fondo de inversión",
        "Criptomonedas / acciones / bolsa",
        "Caja de emergencia",
        "Planes de retiro / pensión",
        "Ahorro para metas específicas (vacaciones, educación, compra de vehículo)",
        "Seguros de vida / seguros patrimoniales"
    ],
    "Otros posibles campos / categorías especiales": [
        "Mascotas: comida, veterinario, juguetes, cuidado",
        "Regalos / donaciones: cumpleaños, navidad, eventos sociales",
        "Hogar: muebles, electrodomésticos, mantenimiento, reparaciones",
        "Ropa y accesorios: ropa diaria, calzado, accesorios, lavandería",
        "Tecnología / gadgets: celulares, computadoras, software, gadgets",
        "Eventos / celebraciones: fiestas, reuniones familiares, bodas"
    ],
    "Compras (Supermercado / Hogar)": [
        "Alimentos básicos",
        "Carnes y proteínas",
        "Frutas y verduras",
        "Lácteos y derivados",
        "Bebidas",
        "Snacks y golosinas",
        "Panadería y repostería",
        "Congelados y preparados",
        "Higiene y cuidado personal",
        "Limpieza y hogar",
        "Mascotas",
        "Otros / misceláneos"
    ]
}

# ----------------------------
# Título
# ----------------------------
st.title("Registro de Gastos - Supabase 🚀")

# ----------------------------
# Selección dinámica de Categoría y Subcategoría
# ----------------------------
categoria = st.selectbox("Categoría", sorted(categorias.keys()), key="categoria")
subcategoria = st.selectbox("Subcategoría", categorias[categoria], key="subcategoria")

# ----------------------------
# Formulario principal
# ----------------------------
with st.form("form_registro"):
    fecha = st.date_input("Fecha", value=date.today())
    tipo = st.selectbox("Tipo", ["Ingreso", "Egreso"])
    monto = st.number_input("Monto", min_value=0.0, step=0.01)
    metodo = st.selectbox("Método de pago", ["Efectivo", "Tarjeta", "Transferencia", "Otro"])
    responsable = st.text_input("Responsable")
    descripcion = st.text_area("Descripción")
    cuenta = st.text_input("Cuenta")
    estado = st.selectbox("Estado", ["Pendiente", "Pagado", "Cancelado"])

    if st.form_submit_button("Guardar en Supabase"):
        data = {
            "Fecha": str(fecha),
            "Tipo": tipo,
            "Monto": monto,
            "Categoria": categoria,
            "Subcategoria": subcategoria,
            "Metodo": metodo,
            "Responsable": responsable,
            "Descripcion": descripcion,
            "Cuenta": cuenta,
            "Estado": estado
        }
        try:
            response = supabase.table("personas").insert([data]).execute()
            if response.data:
                st.success("✅ Registro guardado en Supabase")
            else:
                st.error(f"❌ Error al insertar en Supabase: {response}")
        except Exception as e:
            st.error(f"❌ Error inesperado: {e}")

# ----------------------------
# Mostrar registros existentes
# ----------------------------
if st.button("Leer registros"):
    try:
        response = supabase.table("personas").select("*").execute()
        if response.data:
            st.dataframe(response.data)
        else:
            st.warning("No hay datos todavía.")
    except Exception as e:
        st.error(f"❌ Error al leer registros: {e}")
