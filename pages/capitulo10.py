import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="Capítulo 10", page_icon="🕹️", layout="wide")
st.title("Capítulo 10: Overlay 3D con imagen PNG")

# =============================
# Cargar imagen base
# =============================
modo = st.radio("Modo de entrada:", ["Subir imagen", "Usar cámara"])

# Cargar imagen PNG sin fondo (desde tu carpeta)
png_file = "img/overlay.png"  # tu imagen sin fondo
overlay = cv2.imread(png_file, cv2.IMREAD_UNCHANGED)  # con canal alpha

# ROI para colocar overlay
x_start = st.slider("X inicio", 0, 500, 100)
y_start = st.slider("Y inicio", 0, 500, 100)
ancho = st.slider("Ancho overlay", 50, 500, 150)
alto = st.slider("Alto overlay", 50, 500, 150)

# =============================
# Función para aplicar overlay con transparencia
# =============================
def put_overlay(base, overlay, x, y, w, h):
    overlay_resized = cv2.resize(overlay, (w, h))
    if overlay_resized.shape[2] == 4:
        alpha = overlay_resized[:, :, 3] / 255.0
        for c in range(3):
            base[y:y+h, x:x+w, c] = (alpha * overlay_resized[:, :, c] +
                                     (1-alpha) * base[y:y+h, x:x+w, c])
    return base

# =============================
# Función para efecto 3D (perspectiva simple)
# =============================
def overlay_3d(base, overlay, x, y, w, h):
    # Puntos destino en la imagen base (simula inclinación 3D)
    pts1 = np.float32([[0,0],[overlay.shape[1],0],[overlay.shape[1],overlay.shape[0]],[0,overlay.shape[0]]])
    pts2 = np.float32([[x, y], [x+w, y+int(h*0.2)], [x+w, y+h], [x, y+h-int(h*0.2)]])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    warped = cv2.warpPerspective(overlay, M, (base.shape[1], base.shape[0]), borderMode=cv2.BORDER_TRANSPARENT)
    
    # Aplicar canal alpha
    if warped.shape[2] == 4:
        alpha = warped[:, :, 3] / 255.0
        for c in range(3):
            base[:, :, c] = (alpha * warped[:, :, c] + (1-alpha) * base[:, :, c])
    return base

# =============================
# Procesar imagen subida
# =============================
if modo == "Subir imagen":
    uploaded_file = st.file_uploader("📤 Sube una imagen", type=["jpg","jpeg","png"])
    if uploaded_file is not None:
        img = np.array(Image.open(uploaded_file).convert("RGB"))
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        img_bgr = overlay_3d(img_bgr, overlay, x_start, y_start, ancho, alto)
        st.image(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB), caption="Resultado 3D", use_container_width=True)

# =============================
# Procesar cámara
# =============================
else:
    cam_file = st.camera_input("📷 Captura de cámara")
    if cam_file is not None:
        img = np.array(Image.open(cam_file).convert("RGB"))
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        img_bgr = overlay_3d(img_bgr, overlay, x_start, y_start, ancho, alto)
        st.image(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB), caption="Resultado 3D cámara", use_container_width=True)

#st.page_link("menu", label="↩️ Regresar al menú principal", icon="🏠")

