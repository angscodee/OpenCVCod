import streamlit as st
import cv2
import numpy as np

st.set_page_config(page_title="Capítulo 4", page_icon="🥸", layout="wide")
st.title("Capítulo 4: 📸 Añade un Elementos a tu Foto")

# ===========================
# RUTAS
# ===========================
MOUTH_CASCADE_PATH = 'cascade_files/haarcascade_mcs_mouth.xml'
MUSTACHE_LOCAL_PATH = 'img/moustache.png'
EXAMPLE_IMG_PATH = 'img/ejercicio04.png'

# ===========================
# CARGAR CLASIFICADOR
# ===========================
mouth_cascade = None
classifier = cv2.CascadeClassifier(MOUTH_CASCADE_PATH)
if classifier.empty():
    st.error(f"❌ No se pudo cargar el clasificador de boca. Verifica la ruta: {MOUTH_CASCADE_PATH}")
else:
    mouth_cascade = classifier

# ===========================
# FUNCIÓN PARA APLICAR BIGOTE
# ===========================
def apply_mustache(frame, mouth_rects, mustache):
    if mustache is None or frame is None:
        return frame

    output_frame = frame.copy()
    offset_x = 10  # mover a la derecha en píxeles

    for (x, y, w, h) in mouth_rects:
        mustache_y = int(y - 0.7 * h)
        mustache_resized = cv2.resize(mustache, (int(w * 2), int(h * 2)))
        mustache_h, mustache_w = mustache_resized.shape[:2]

        x_center = x + w // 2
        x1 = x_center - mustache_w // 2 + offset_x  # aplicar desplazamiento
        x2 = x1 + mustache_w
        y1 = mustache_y
        y2 = mustache_y + mustache_h

        # Validación de límites
        if y1 < 0: 
            y1 = 0
            y2 = mustache_h
        if y2 > output_frame.shape[0]:
            y2 = output_frame.shape[0]
            y1 = y2 - mustache_h
        if x1 < 0: 
            x1 = 0
            x2 = mustache_w
        if x2 > output_frame.shape[1]:
            x2 = output_frame.shape[1]
            x1 = x2 - mustache_w

        # Alpha blending
        if mustache_resized.shape[2] == 4:
            alpha_mustache = mustache_resized[:, :, 3] / 255.0
            roi = output_frame[y1:y2, x1:x2]
            for c in range(3):
                roi[:, :, c] = (alpha_mustache * mustache_resized[:, :, c] +
                                (1 - alpha_mustache) * roi[:, :, c])
            output_frame[y1:y2, x1:x2] = roi
        break
    return output_frame

# ===========================
# IMAGEN DE EJEMPLO
# ===========================
example_img = cv2.imread(EXAMPLE_IMG_PATH)
if example_img is None:
    st.error(f"❌ No se pudo cargar la imagen de ejemplo: {EXAMPLE_IMG_PATH}")
else:
    example_rgb = cv2.cvtColor(example_img, cv2.COLOR_BGR2RGB)
    mustache_local = cv2.imread(MUSTACHE_LOCAL_PATH, cv2.IMREAD_UNCHANGED)

    # Redimensionar para ancho fijo
    target_width = 400
    h_orig, w_orig = example_rgb.shape[:2]
    scale_ratio = target_width / w_orig
    target_height = int(h_orig * scale_ratio)
    example_resized = cv2.resize(example_rgb, (target_width, target_height))

    # Columnas para centrar la fila
    col_left, col_orig, col_effect, col_right = st.columns([1,1,1,1])

    # Placeholder para la imagen con efecto
    effect_placeholder = col_effect.empty()

    with col_orig:
        st.image(example_resized, caption="Original", use_container_width=True)

    with col_effect:
        # Creamos la imagen blur inicialmente
        blur_img = cv2.GaussianBlur(example_resized, (25,25), 0)
        effect_placeholder.image(blur_img, caption="Con efecto", use_container_width=True)

        btn_center = st.empty()
        if btn_center.button("Ver efecto"):
            gray = cv2.cvtColor(example_img, cv2.COLOR_BGR2GRAY)
            mouth_rects = mouth_cascade.detectMultiScale(
                gray, scaleFactor=1.7, minNeighbors=11, minSize=(25,25)
            )
            result = apply_mustache(example_img, mouth_rects, mustache_local)
            result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
            result_resized = cv2.resize(result_rgb, (target_width, target_height))
            effect_placeholder.image(result_resized, caption="Con bigote", use_container_width=True)

# ===========================
# SECCIÓN SUBIR TU PROPIA IMAGEN
# ===========================
st.markdown("---")
st.subheader("Prueba con tu propia imagen:")
col1, col2 = st.columns(2)
uploaded_mustache = None

with col1:
    uploaded_file = st.file_uploader("1. Sube tu foto (JPG, PNG)", type=["jpg","jpeg","png"])
with col2:
    uploaded_mustache_file = st.file_uploader("2. Sube el bigote (Opcional, PNG)", type=["png"])
    if uploaded_mustache_file:
        uploaded_mustache = uploaded_mustache_file
    else:
        if mustache_local is not None:
            class LocalMustache:
                def read(self):
                    _, buffer = cv2.imencode('.png', mustache_local)
                    return buffer.tobytes()
            uploaded_mustache = LocalMustache()

if uploaded_file and uploaded_mustache and mouth_cascade is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    mustache_bytes = np.asarray(bytearray(uploaded_mustache.read()), dtype=np.uint8)
    mustache_img = cv2.imdecode(mustache_bytes, cv2.IMREAD_UNCHANGED)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mouth_rects = mouth_cascade.detectMultiScale(gray, scaleFactor=1.7, minNeighbors=11, minSize=(25,25))
    result_frame = apply_mustache(frame, mouth_rects, mustache_img)
    rgb_frame = cv2.cvtColor(result_frame, cv2.COLOR_BGR2RGB)
    st.image(rgb_frame, caption="¡Felicidades, tienes mostacho!", use_container_width=True)

