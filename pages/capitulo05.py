import streamlit as st
import cv2
import numpy as np
from PIL import Image

# ===========================
# CONFIGURACIÓN DE LA PÁGINA
# ===========================
st.set_page_config(page_title="Capítulo 5", page_icon="👾", layout="wide")
st.title("Capítulo 5: 📍 Detección de Esquinas (Good Features to Track)")

# ===========================
# RUTAS Y EJEMPLOS
# ===========================
EXAMPLE_IMG_PATH = "img/ejercicio05.png"

# ===========================
# FUNCIÓN DE DETECCIÓN DE ESQUINAS
# ===========================
def detectar_esquinas(img, maxCorners, qualityLevel, minDistance):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    corners = cv2.goodFeaturesToTrack(
        gray,
        maxCorners=maxCorners,
        qualityLevel=qualityLevel,
        minDistance=minDistance
    )

    if corners is not None:
        corners = np.float32(corners)
        for item in corners:
            x, y = item[0]
            cv2.circle(img, (int(x), int(y)), 5, (0, 255, 0), -1)
    return img, corners

# ===========================
# IMAGEN DE EJEMPLO
# ===========================
example_img = cv2.imread(EXAMPLE_IMG_PATH)

if example_img is None:
    st.error(f"❌ No se pudo cargar la imagen de ejemplo: {EXAMPLE_IMG_PATH}")
else:
    example_rgb = cv2.cvtColor(example_img, cv2.COLOR_BGR2RGB)

    # Aplicar detección de esquinas con valores predeterminados
    ejemplo_procesado, corners = detectar_esquinas(example_img.copy(), 7, 0.05, 25)
    ejemplo_rgb = cv2.cvtColor(ejemplo_procesado, cv2.COLOR_BGR2RGB)

    st.markdown("### 🧩 Ejemplo de detección de esquinas")
    col1, col2 = st.columns(2)
    with col1:
        st.image(example_rgb, caption="Imagen Original", use_container_width=True)
    with col2:
        st.image(ejemplo_rgb, caption=f"🔹 Esquinas detectadas ({len(corners)} puntos)", use_container_width=True)

# ===========================
# PARÁMETROS AJUSTABLES
# ===========================
st.markdown("---")
st.markdown("### 🎛️ Ajusta los parámetros antes de subir tu imagen")

col1, col2, col3 = st.columns(3)
with col1:
    max_corners = st.slider("Número máximo de esquinas", 1, 50, 7)
with col2:
    quality_level = st.slider("Nivel de calidad mínima", 0.01, 0.5, 0.05)
with col3:
    min_distance = st.slider("Distancia mínima entre esquinas", 1, 100, 25)

# ===========================
# SUBIR IMAGEN DEL USUARIO
# ===========================
st.markdown("---")
st.subheader("📤 Prueba con tu propia imagen:")

uploaded_file = st.file_uploader("Sube tu foto (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Leer imagen
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    user_img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # Aplicar detección con los valores elegidos
    user_result, user_corners = detectar_esquinas(
        user_img.copy(), max_corners, quality_level, min_distance
    )

    # Mostrar resultados
    user_rgb = cv2.cvtColor(user_result, cv2.COLOR_BGR2RGB)

    st.image(user_rgb, caption="📍 Resultado con tus parámetros", use_container_width=True)

    if user_corners is not None:
        st.success(f"Se detectaron {len(user_corners)} esquinas en tu imagen.")
    else:
        st.warning("⚠️ No se detectaron esquinas en la imagen. Prueba con otros parámetros.")
else:
    st.info("👆 Ajusta los parámetros y sube tu imagen para ver el resultado.")

