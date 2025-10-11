import streamlit as st
import cv2
import numpy as np
from PIL import Image

# ==============================
# CONFIGURACIÓN DE PÁGINA
# ==============================
st.set_page_config(page_title="Capítulo 8", page_icon="👾", layout="wide")

# ==============================
# TÍTULO Y DESCRIPCIÓN
# ==============================
st.markdown("""
<h1 style='text-align: center; color: #ffffff;'>Capítulo 8: Detección de color (azul)</h1>
<p style='text-align: center; color: #cccccc;'>
Este capítulo muestra cómo detectar un color específico (en este caso, azul) usando el modelo de color HSV.
</p>
""", unsafe_allow_html=True)

# Fondo degradado
st.markdown("""
<style>
body {
    background-color: #0f2027;
    background-image: linear-gradient(315deg, #2c5364 0%, #203a43 50%, #0f2027 100%);
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# SUBIR IMAGEN
# ==============================
uploaded_file = st.file_uploader("📸 Sube una imagen para detectar el color azul", type=["jpg", "jpeg", "png"])

# Si no se sube imagen, usar la de ejemplo
if uploaded_file is None:
    st.info("🔹 No subiste ninguna imagen, se usará el ejemplo por defecto (`ejercicio08.png`).")
    uploaded_file = "img/ejercicio08.png"

# Convertir imagen a formato OpenCV
image = Image.open(uploaded_file)
img = np.array(image)
img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

# ==============================
# DETECCIÓN DE COLOR (azul)
# ==============================
hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
lower_blue = np.array([60, 100, 100])
upper_blue = np.array([180, 255, 255])

mask = cv2.inRange(hsv, lower_blue, upper_blue)
result = cv2.bitwise_and(img_bgr, img_bgr, mask=mask)
result = cv2.medianBlur(result, ksize=5)

# Convertir a RGB para mostrar
original_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

# ==============================
# MOSTRAR RESULTADOS
# ==============================
st.subheader("🎯 Resultado de la detección de color:")

col1, col2 = st.columns(2)
with col1:
    st.image(original_rgb, caption="Imagen original", use_container_width=True)
with col2:
    st.image(result_rgb, caption="Regiones con color azul detectado", use_container_width=True)


