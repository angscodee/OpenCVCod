import streamlit as st
import cv2
import numpy as np

# ===========================
# CONFIGURACIÓN DE LA PÁGINA
# ===========================
st.set_page_config(page_title="Capítulo 6", page_icon="⚡", layout="wide")
st.title("Capítulo 6: Detección de movimiento (Mapa de energía)")

# ===========================
# RUTA DE IMAGEN DE EJEMPLO
# ===========================
EXAMPLE_IMG_PATH = "img/ejercicio06.png"

# ===========================
# CARGAR IMAGEN DE EJEMPLO
# ===========================
example_img = cv2.imread(EXAMPLE_IMG_PATH)

if example_img is None:
    st.error(f"❌ No se pudo cargar la imagen de ejemplo: {EXAMPLE_IMG_PATH}")
else:
    gray_example = cv2.cvtColor(example_img, cv2.COLOR_BGR2GRAY)

    # Calcular gradientes
    sobel_x = cv2.Sobel(gray_example, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray_example, cv2.CV_64F, 0, 1, ksize=3)

    # Magnitud del gradiente
    energy = cv2.addWeighted(cv2.convertScaleAbs(sobel_x), 0.5,
                             cv2.convertScaleAbs(sobel_y), 0.5, 0)

    # Imagen resaltando las zonas con más energía
    mask = cv2.merge([energy, np.zeros_like(energy), np.zeros_like(energy)])
    highlighted = cv2.addWeighted(cv2.cvtColor(example_img, cv2.COLOR_BGR2RGB), 0.7, mask, 5, 0)

    # Centrar imágenes
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.image(cv2.cvtColor(example_img, cv2.COLOR_BGR2RGB), caption="Original", use_container_width=True)
    with col2:
        st.image(energy, caption="Mapa de energía", use_container_width=True)
    with col3:
        st.image(highlighted, caption="Zonas de alta energía", use_container_width=True)

# ===========================
# PARÁMETROS AJUSTABLES
# ===========================
st.markdown("---")
st.subheader("🎛️ Ajusta los parámetros del detector")

ksize = st.slider("Tamaño del kernel Sobel (impar ≥ 3)", 3, 9, 3, step=2)
alpha = st.slider("Intensidad del resaltado", 0.7, 1.0, 0.7)

# ===========================
# SECCIÓN DE IMAGEN DEL USUARIO
# ===========================
st.markdown("---")
st.subheader("📤 Prueba con tu propia imagen")

uploaded_file = st.file_uploader("Sube una imagen (JPG o PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)

    energy = cv2.addWeighted(cv2.convertScaleAbs(sobel_x), 0.5,
                             cv2.convertScaleAbs(sobel_y), 0.5, 0)

    mask = cv2.merge([energy, np.zeros_like(energy), np.zeros_like(energy)])
    highlighted = cv2.addWeighted(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), 1 - alpha, mask, alpha, 0)

    colA, colB, colC = st.columns([1, 1, 1])
    with colA:
        st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Imagen original", use_container_width=True)
    with colB:
        st.image(energy, caption="Mapa de energía", use_container_width=True)
    with colC:
        st.image(highlighted, caption="Regiones destacadas", use_container_width=True)

else:
    st.info("👆 Sube una imagen para analizar las zonas con mayor energía visual.")

