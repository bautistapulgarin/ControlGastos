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
    "Otros": [
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
# Función principal
# ----------------------------
def main():
    st.title("Registro de Gastos con Subcategorías Dependientes 🚀")

    with st.form("form_registro"):
        Fecha = st.date_input("Fecha", value=datetime.today())
        Tipo = st.selectbox("Tipo", ["Ingreso", "Gasto"])
        Monto = st.number_input("Monto", min_value=0.0, step=0.01)

        # Selector de categoría
        Categoria = st.selectbox("Categoría", list(categorias.keys()))

        # Selector de subcategoría depende de la categoría
        if Categoria:
            Subcategoria = st.selectbox("Subcategoría", categorias[Categoria])
        else:
            Subcategoria = st.text_input("Subcategoría")

        CategoriaMercado = st.text_input("Categoría de Mercado")
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
