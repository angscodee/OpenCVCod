import streamlit as st
import cv2
import numpy as np
import math

# ===============================
# CONFIGURACIÓN DE PÁGINA
# ===============================
st.set_page_config(page_title="Capítulo 01", page_icon="🌊", layout="wide")

# ===============================
# ESTILO Y TÍTULO
# ===============================
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
<h1 style='text-align: center; color: #ffffff;'>🌊 Capítulo 1: Efectos de Onda en Imágenes</h1>
<p style='text-align: center; color: #cccccc;'>
Aplicamos transformaciones trigonométricas para generar efectos ondulatorios sobre una imagen.
</p>
""", unsafe_allow_html=True)

# ===============================
# SUBIR IMAGEN
# ===============================
uploaded_file = st.file_uploader("📤 Sube una imagen", type=["jpg", "jpeg", "png"])

# Si no se sube imagen, usar la de ejemplo
if uploaded_file is None:
    st.info("🔹 No subiste ninguna imagen, se usará el ejemplo por defecto (`ejercicio01.png`).")
    uploaded_file = "img/ejercicio01.png"

# ===============================
# LEER IMAGEN
# ===============================
file_bytes = np.asarray(bytearray(open(uploaded_file, "rb").read()), dtype=np.uint8)
img = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)
rows, cols = img.shape

# ===============================
# Mostrar imagen original centrada y reducida
# ===============================
st.subheader("📸 Imagen Original")
col_empty1, col_img, col_empty2 = st.columns([1, 2, 1])
with col_img:
    st.image(
        img,
        caption="Imagen Original",
        use_container_width=False,
        width=int(cols * 0.5),
        channels="GRAY"
    )

# ===============================
# GENERAR LOS EFECTOS
# ===============================

# Efecto 1: Onda Vertical
img_output_v = np.zeros(img.shape, dtype=img.dtype)
for i in range(rows):
    for j in range(cols):
        offset_x = int(25.0 * math.sin(2 * 3.14 * i / 180))
        if j + offset_x < cols:
            img_output_v[i, j] = img[i, (j + offset_x) % cols]

# Efecto 2: Onda Horizontal
img_output_h = np.zeros(img.shape, dtype=img.dtype)
for i in range(rows):
    for j in range(cols):
        offset_y = int(16.0 * math.sin(2 * 3.14 * j / 150))
        if i + offset_y < rows:
            img_output_h[i, j] = img[(i + offset_y) % rows, j]

# Efecto 3: Multidireccional
img_output_m = np.zeros(img.shape, dtype=img.dtype)
for i in range(rows):
    for j in range(cols):
        offset_x = int(20.0 * math.sin(2 * 3.14 * i / 150))
        offset_y = int(20.0 * math.cos(2 * 3.14 * j / 150))
        if i + offset_y < rows and j + offset_x < cols:
            img_output_m[i, j] = img[(i + offset_y) % rows, (j + offset_x) % cols]

# Efecto 4: Cóncavo
img_output_c = np.zeros(img.shape, dtype=img.dtype)
for i in range(rows):
    for j in range(cols):
        offset_x = int(128.0 * math.sin(2 * 3.14 * i / (2 * cols)))
        if j + offset_x < cols:
            img_output_c[i, j] = img[i, (j + offset_x) % cols]

# ===============================
# MOSTRAR RESULTADOS EN FILA
# ===============================
st.markdown("---")
st.subheader("🎨 Comparativa de Efectos de Onda")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.image(img_output_v, caption="⬆️ Onda Vertical", use_container_width=True, channels="GRAY")
with col2:
    st.image(img_output_h, caption="➡️ Onda Horizontal", use_container_width=True, channels="GRAY")
with col3:
    st.image(img_output_m, caption="🌪️ Multidireccional", use_container_width=True, channels="GRAY")
with col4:
    st.image(img_output_c, caption="🔮 Cóncavo", use_container_width=True, channels="GRAY")
