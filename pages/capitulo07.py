import streamlit as st
import cv2
import numpy as np
from PIL import Image
import random

# ==============================
# CONFIGURACIÓN DE PÁGINA
# ==============================
st.set_page_config(page_title="Capítulo 7", page_icon="🎨", layout="wide")

# ==============================
# TÍTULO Y ESTILO
# ==============================
st.markdown("""
<h1 style='text-align: center; color: #ffffff;'>🎨 Capítulo 7: Detección y Segmentación con Watershed</h1>
<p style='text-align: center; color: #cccccc;'>
El algoritmo <b>Watershed</b> permite identificar y separar regiones u objetos dentro de una imagen.
</p>
""", unsafe_allow_html=True)

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
# IMAGEN DE EJEMPLO
# ==============================
EXAMPLE_PATH = "img/ejercicio07.png"

st.markdown("---")
st.subheader("🖼️ Ejemplo de segmentación con Watershed")

example_img = cv2.imread(EXAMPLE_PATH)
if example_img is None:
    st.error(f"❌ No se pudo cargar la imagen de ejemplo: {EXAMPLE_PATH}")
else:
    # Convertir a escala de grises
    gray = cv2.cvtColor(example_img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Apertura morfológica
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=3)

    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    ret, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0

    markers = cv2.watershed(example_img, markers)

    # Crear imagen coloreada
    segmented = np.zeros_like(example_img)
    for marker_id in np.unique(markers):
        if marker_id <= 1:
            continue
        mask = (markers == marker_id)
        color = (random.randint(100, 255), random.randint(0, 100), random.randint(150, 255))  # morado rosado
        segmented[mask] = color

    # Combinar con la original
    blended = cv2.addWeighted(cv2.cvtColor(example_img, cv2.COLOR_BGR2RGB), 0.6, segmented, 0.8, 0)

    # Mostrar resultados
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(cv2.cvtColor(example_img, cv2.COLOR_BGR2RGB), caption="Original", use_container_width=True)
    with col2:
        st.image(thresh, caption="Umbralización", use_container_width=True)
    with col3:
        st.image(blended, caption="Resultado (Watershed coloreado)", use_container_width=True)

# ==============================
# PARÁMETROS Y SUBIDA DE IMAGEN
# ==============================
st.markdown("---")
st.subheader("🎛️ Prueba con tu propia imagen")

iterations = st.slider("Iteraciones de limpieza (morfología)", 1, 6, 3)
threshold_ratio = st.slider("Nivel de separación (0.5 - 0.9)", 0.5, 0.9, 0.7)

uploaded_file = st.file_uploader("📸 Sube una imagen con formas u objetos", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img = np.array(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=iterations)

    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    ret, sure_fg = cv2.threshold(dist_transform, threshold_ratio * dist_transform.max(), 255, 0)

    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    ret, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0

    markers = cv2.watershed(img, markers)

    segmented = np.zeros_like(img)
    for marker_id in np.unique(markers):
        if marker_id <= 1:
            continue
        mask = (markers == marker_id)
        color = (random.randint(100, 255), random.randint(0, 100), random.randint(150, 255))
        segmented[mask] = color

    blended = cv2.addWeighted(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), 0.6, segmented, 0.8, 0)

    colA, colB, colC = st.columns(3)
    with colA:
        st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Original", use_container_width=True)
    with colB:
        st.image(thresh, caption="Umbralización", use_container_width=True)
    with colC:
        st.image(blended, caption="Resultado (Watershed coloreado)", use_container_width=True)

else:
    st.info("👆 Sube una imagen para aplicar el algoritmo Watershed.")

