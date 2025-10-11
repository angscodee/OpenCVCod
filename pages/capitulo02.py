import streamlit as st
import cv2
import numpy as np

# ===========================
# CONFIGURACIÓN DE LA PÁGINA
# ===========================
st.set_page_config(page_title="Capítulo 2", page_icon="👾", layout="wide")

# ===========================
# ESTILO Y TÍTULO
# ===========================
st.markdown("""
<style>
body {
    background-color: #0f2027;
    background-image: linear-gradient(315deg, #2c5364 0%, #203a43 50%, #0f2027 100%);
    color: white;
}
h1, h2, h3, p {
    color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style='text-align: center; color: #ffffff;'>🎞️ Capítulo 2: Filtros de Movimiento</h1>
<p style='text-align: center; color: #cccccc;'>
En este capítulo aplicamos un filtro <b>Motion Blur</b> para simular movimiento en una imagen.
</p>
""", unsafe_allow_html=True)

# ===========================
# SUBIR IMAGEN
# ===========================
uploaded_file = st.file_uploader("📤 Sube una imagen", type=["jpg", "jpeg", "png"])

# Si no se sube imagen, usar la de ejemplo
if uploaded_file is None:
    st.info("🔹 No subiste ninguna imagen, se usará el ejemplo por defecto (`ejercicio02.png`).")
    uploaded_file = "img/ejercicio02.png"

# ===========================
# LEER IMAGEN
# ===========================
file_bytes = np.asarray(bytearray(open(uploaded_file, "rb").read()), dtype=np.uint8)
img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

# ===========================
# EFECTO: Motion Blur
# ===========================
st.markdown("---")
st.subheader("⚙️ Aplicar Filtro Motion Blur")

size = st.slider("📏 Tamaño del desenfoque (kernel)", 3, 50, 15, step=2)

# Crear kernel de desenfoque
kernel_motion_blur = np.zeros((size, size))
kernel_motion_blur[int((size - 1) / 2), :] = np.ones(size)
kernel_motion_blur = kernel_motion_blur / size

# Aplicar filtro
output = cv2.filter2D(img, -1, kernel_motion_blur)

# ===========================
# MOSTRAR RESULTADO
# ===========================
st.subheader("✨ Imagen con efecto Motion Blur")
col1, col2 = st.columns(2)
with col1:
    st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Original", use_container_width=True)
with col2:
    st.image(cv2.cvtColor(output, cv2.COLOR_BGR2RGB), caption="Con Motion Blur", use_container_width=True)



