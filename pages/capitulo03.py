import streamlit as st
import cv2
import numpy as np

# ===========================
# CONFIGURACIÓN DE LA PÁGINA
# ===========================
st.set_page_config(page_title="Capítulo 3", page_icon="👾", layout="wide")
st.title("Capítulo 3: ✨ Cartoonización")

# ===========================
# RUTAS
# ===========================
EXAMPLE_IMG_PATH = 'img/ejercicio03.png'

# ===========================
# FUNCIÓN PARA CARTOON
# ===========================
def cartoonize_image(img, smoothness=9, edges_thickness=150):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        blockSize=9,
        C=9
    )
    color = cv2.bilateralFilter(img, d=9, sigmaColor=edges_thickness, sigmaSpace=smoothness)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return cartoon

# ===========================
# IMAGEN DE EJEMPLO
# ===========================
st.subheader("Ejemplo de Cartoonización")
example_img = cv2.imread(EXAMPLE_IMG_PATH)
if example_img is not None:
    target_width = 400
    h_orig, w_orig = example_img.shape[:2]
    scale_ratio = target_width / w_orig
    target_height = int(h_orig * scale_ratio)
    example_resized = cv2.resize(example_img, (target_width, target_height))

    # Cartoon ejemplo con parámetros predeterminados
    cartoon_example = cartoonize_image(example_resized, smoothness=9, edges_thickness=150)

    col1, col2 = st.columns(2)
    with col1:
        st.image(cv2.cvtColor(example_resized, cv2.COLOR_BGR2RGB), caption="Original (Ejemplo)", use_container_width=True)
    with col2:
        st.image(cv2.cvtColor(cartoon_example, cv2.COLOR_BGR2RGB), caption="Cartoon (Ejemplo)", use_container_width=True)

# ===========================
# SLIDERS PARA PARÁMETROS DEL USUARIO
# ===========================
st.markdown("---")
st.subheader("Define los parámetros que deseas aplicar a tu imagen:")
smoothness = st.slider("Suavidad del color", 1, 15, 9, step=1)
edges_thickness = st.slider("Grosor de líneas / detalle de bordes", 50, 300, 150, step=5)

# ===========================
# SUBIR IMAGEN DEL USUARIO
# ===========================
st.subheader("📤 Sube tu propia imagen")
uploaded_file = st.file_uploader("Elige una imagen", type=["jpg","jpeg","png"])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    cartoon_result = cartoonize_image(img, smoothness, edges_thickness)

    col1, col2 = st.columns(2)
    with col1:
        st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Original", use_container_width=True)
    with col2:
        st.image(cv2.cvtColor(cartoon_result, cv2.COLOR_BGR2RGB), caption="Cartoonizado", use_container_width=True)
else:
    st.info("👆 Ajusta los parámetros y sube una imagen para ver el resultado.")


