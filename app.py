import streamlit as st
import base64

# ==========================
#      IMAGEN DE FONDO
# ==========================
def set_background(image_file):
    with open(image_file, "rb") as f:
        img_data = f.read()
    b64_encoded = base64.b64encode(img_data).decode()
    style = f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url(data:image/png;base64,{b64_encoded});
            background-size: cover;
            background-attachment: fixed;
        }}
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)


# ==========================
#       CONFIGURACIÓN
# ==========================
st.set_page_config(page_title="OPEN CV - EJERCICIOS", page_icon="👾", layout="wide")
set_background('img/back.png')

# ==========================
#       CSS GENERAL
# ==========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

body {
    font-family: 'Poppins', sans-serif;
    color: #222;
}

/* Ocultar barra superior y el menú de tres puntos */
[data-testid="stHeader"], [data-testid="stToolbar"] {
    display: none;
}

/* --- ESTILO DE LA IMAGEN DE TÍTULO --- */
.title-image-container {
    text-align: center;
    margin-top: -100px;
    margin-bottom: -20px;
}

/* --- SUBTÍTULO --- */
.subtitle {
    text-align: center;
    font-size: 20px;
    color: #555;
    margin-bottom: 60px;
}

/* --- ESTILO DE LAS OPCIONES DE CAPÍTULO (CADA DIV) --- */
.chapter-option {
    padding: 20px 25px;
    border-radius: 0;
    border: none !important;
    cursor: pointer;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    text-decoration: none;
    color: #fff;
    font-weight: 600;
    font-size: 18px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    margin-bottom: 0 !important;
    display: block;
    position: relative;
}

/* Pseudo-elemento para el signo más */
.chapter-option::after {
    content: '+';
    position: absolute;
    right: 25px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 1.5em;
    color: #fff;
}

/* Redondea solo la primera y última opción */
.chapter-option:first-of-type {
    border-top-left-radius: 15px;
    border-top-right-radius: 15px;
}
.chapter-option:last-of-type {
    border-bottom-left-radius: 15px;
    border-bottom-right-radius: 15px;
}

/* Colores alternos para las opciones */
.chapter-option:nth-of-type(4n+1) { background-color: #232933; text-decoration: none; color: #fff; }
.chapter-option:nth-of-type(4n+2) { background-color: #5f11ed; text-decoration: none; color: #fff; }
.chapter-option:nth-of-type(4n+3) { background-color: #574aa1; text-decoration: none; color: #fff; }
.chapter-option:nth-of-type(4n+4) { background-color: #15248a; text-decoration: none; color: #fff; }
.chapter-option:nth-of-type(4n+5) { background-color: #16445e; text-decoration: none; color: #fff; }
.chapter-option:nth-of-type(4n+6) { background-color: #0481cf; text-decoration: none; color: #fff; }


/* Efecto de hover */
.chapter-option:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}

/* Eliminar el estilo por defecto de los enlaces */
a {
    text-decoration: none;
}

/* --- ESTILO PARA LA NOTA INCLINADA --- */
.tilted-card-container {
    text-align: center;
    margin: 50px auto; /* Centra el contenedor y ajusta márgenes superior/inferior */
    max-width: 400px; /* Ajusta este valor para controlar el ancho de la tarjeta */
    transform: rotate(-3deg);
    transition: transform 0.3s ease;
    box-shadow: 5px 5px 15px rgba(0,0,0,0.2);
    display: block; /* Para que max-width funcione correctamente */
    padding: 10px; /* Reducido para que la imagen ocupe más espacio */
    background-color: #f0f0f0;
    border-radius: 10px;
}
.tilted-card-container:hover {
    transform: rotate(0deg) scale(1.05);
    box-shadow: 8px 8px 20px rgba(0,0,0,0.3);
}

/* Estilo para la imagen dentro de la tarjeta inclinada */
.tilted-card-container img {
    width: 100%; /* La imagen ocupará el 100% del ancho del contenedor */
    height: auto;
    display: block;
    margin: 0 auto;
    border-radius: 5px;
}

</style>
""", unsafe_allow_html=True)


# ==========================
# FUNCIÓN PARA MOSTRAR IMAGEN DE TÍTULO
# ==========================
def show_image_centered(image_file, width=400):
    with open(image_file, "rb") as f:
        img_bytes = f.read()
    b64_img = base64.b64encode(img_bytes).decode()
    html_code = f"""
    <div class='title-image-container'>
        <img src="data:image/png;base64,{b64_img}" 
             style="width: auto; height: auto;">
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)

# ==========================
#          TARJETA
# ==========================
def show_tilted_image(image_file): # max_width_percent ya no es necesario aquí
    with open(image_file, "rb") as f:
        img_bytes = f.read()
    b64_img = base64.b64encode(img_bytes).decode()
    html_code = f"""
    <div class='tilted-card-container'>
        <img src="data:image/png;base64,{b64_img}"> 
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)


# ==========================
#      IMAGEN PRINCIPAL
# ==========================
show_image_centered("img/front.png", width=400)
st.markdown('<div class="subtitle">Elige el capítulo que prefieras...</div>', unsafe_allow_html=True)


# ==========================
# LISTA DE CAPÍTULOS CON ENLACES HTML
# ==========================

cards_html = """
<div>
    <a href="capitulo01" target="_self" class="chapter-option">Capítulo 1: Efectos de Onda en Imágenes</a>
    <a href="capitulo02" target="_self" class="chapter-option">Capítulo 2: Filtros de Movimiento</a>
    <a href="capitulo03" target="_self" class="chapter-option">Capítulo 3: Cartoonización</a>
    <a href="capitulo04" target="_self" class="chapter-option">Capítulo 4: Añade un Elementos a tu Foto</a>
    <a href="capitulo05" target="_self" class="chapter-option">Capítulo 5: Detección de Esquinas</a>
    <a href="capitulo06" target="_self" class="chapter-option">Capítulo 6: Detección de movimiento</a>
    <a href="capitulo07" target="_self" class="chapter-option">Capítulo 7: Detección y Segmentación </a>
    <a href="capitulo08" target="_self" class="chapter-option">Capítulo 8: Detección de color</a>
    <a href="capitulo09" target="_self" class="chapter-option">Capítulo 9: Detección de características</a>
    <a href="capitulo10" target="_self" class="chapter-option">Capítulo 10: Overlay 3D con imagen PNG</a>
    <a href="capitulo11" target="_self" class="chapter-option">Capítulo 11: Extracción de características</a>
</div>
"""

st.markdown(cards_html, unsafe_allow_html=True)

show_tilted_image("img/bott.png")