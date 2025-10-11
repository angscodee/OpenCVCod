import streamlit as st
import cv2
import numpy as np
from PIL import Image

# ==============================
# CONFIGURACIÓN DE PÁGINA
# ==============================
st.set_page_config(page_title="Capítulo 9", page_icon="👾", layout="wide")

# ==============================
# TÍTULO
# ==============================
st.markdown("""
<h1 style='text-align: center; color: #ffffff;'>Capítulo 9: Detección de características (SIFT y Dense)</h1>
<p style='text-align: center; color: #cccccc;'>
Explora cómo funcionan los detectores de puntos clave en imágenes usando SIFT y un detector denso.
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
# CLASES DE DETECTORES
# ==============================
class DenseDetector:
    def __init__(self, step_size=20, feature_scale=20, img_bound=20):
        self.initXyStep = step_size
        self.initFeatureScale = feature_scale
        self.initImgBound = img_bound

    def detect(self, img):
        keypoints = []
        rows, cols = img.shape[:2]
        for x in range(self.initImgBound, rows, self.initFeatureScale):
            for y in range(self.initImgBound, cols, self.initFeatureScale):
                keypoints.append(cv2.KeyPoint(float(y), float(x), self.initXyStep))
        return keypoints


class SIFTDetector:
    def __init__(self):
        self.detector = cv2.SIFT_create()

    def detect(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return self.detector.detect(gray, None)

# ==============================
# SUBIR IMAGEN
# ==============================
uploaded_file = st.file_uploader("📸 Sube una imagen para detectar puntos clave", type=["jpg", "jpeg", "png"])

# Si no se sube imagen, usar la de ejemplo
if uploaded_file is None:
    st.info("🔹 No subiste ninguna imagen, se usará el ejemplo por defecto (`ejercicio09.png`).")
    uploaded_file = "img/ejercicio09.png"

# ==============================
# PROCESAMIENTO
# ==============================
image = Image.open(uploaded_file)
img = np.array(image)
img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

# Seleccionar método
metodo = st.radio("Selecciona el método de detección:", ("Dense Detector", "SIFT Detector"), index=0, horizontal=True)

if metodo == "Dense Detector":
    detector = DenseDetector()
else:
    detector = SIFTDetector()

# Detectar puntos
keypoints = detector.detect(img_bgr)
img_result = cv2.drawKeypoints(
    img_bgr, keypoints, None,
    flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,
    color=(0, 255, 0)
)

# Convertir a RGB
img_result_rgb = cv2.cvtColor(img_result, cv2.COLOR_BGR2RGB)

# ==============================
# MOSTRAR RESULTADO
# ==============================
st.subheader(f"🔍 Resultado con {metodo}")
st.image(img_result_rgb, caption=f"Características detectadas usando {metodo}", use_container_width=True)


