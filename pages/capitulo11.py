import streamlit as st
import cv2
import numpy as np
from sklearn.cluster import KMeans
import _pickle as pickle
from PIL import Image

st.set_page_config(page_title="Capítulo 11", page_icon="🕹️", layout="wide")
st.title("Capítulo 11: Extracción de características")

# -------------------------
# Subir imagen o usar carpeta
# -------------------------
modo = st.radio("Selecciona imagen:", ["Subir imagen", "Usar imagen de carpeta"])
if modo == "Subir imagen":
    uploaded_file = st.file_uploader("📤 Sube una imagen", type=["jpg","jpeg","png"])
    if uploaded_file is not None:
        img = np.array(Image.open(uploaded_file).convert("RGB"))
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
elif modo == "Usar imagen de carpeta":
    img_path = "img/sample.png"  # coloca tu imagen aquí
    img_bgr = cv2.imread(img_path)

if 'img_bgr' in locals():
    st.image(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB), caption="Imagen seleccionada", use_container_width=True)

    # -------------------------
    # Extracción de características
    # -------------------------
    class DenseDetector(): 
        def __init__(self, step_size=20, feature_scale=20, img_bound=20): 
            self.initXyStep = step_size
            self.initFeatureScale = feature_scale
            self.initImgBound = img_bound

        def detect(self, img):
            keypoints = []
            rows, cols = img.shape[:2]
            for x in range(self.initImgBound, rows, self.initFeatureScale):
                for y in range(self.initImgBound, cols, self.initFeatureScale):
                    keypoints.append(cv2.KeyPoint(float(x), float(y), self.initXyStep))
            return keypoints

    class SIFTExtractor():
        def __init__(self):
            self.extractor = cv2.SIFT_create()

        def compute(self, image, kps): 
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            kps, des = self.extractor.detectAndCompute(gray_image, None)
            return kps, des

    class Quantizer(object): 
        def __init__(self, num_clusters=32):
            self.extractor = SIFTExtractor()
            self.num_clusters = num_clusters 

        def quantize(self, datapoints): 
            kmeans = KMeans(self.num_clusters, n_init=10, max_iter=50, tol=1.0)
            res = kmeans.fit(datapoints)
            return kmeans, res.cluster_centers_

        def normalize(self, input_data): 
            sum_input = np.sum(input_data)
            return input_data / sum_input if sum_input > 0 else input_data

        def get_feature_vector(self, img, kmeans, centroids): 
            kps = DenseDetector().detect(img) 
            kps, fvs = SIFTExtractor().compute(img, kps) 
            labels = kmeans.predict(fvs) 
            fv = np.zeros(self.num_clusters) 
            for i, item in enumerate(fvs): 
                fv[labels[i]] += 1 
            fv_image = np.reshape(fv, ((1, fv.shape[0]))) 
            return self.normalize(fv_image)

    # -------------------------
    # Ejecutar extracción
    # -------------------------
    kps_all = DenseDetector().detect(img_bgr)
    kps, fvs = SIFTExtractor().compute(img_bgr, kps_all)

    st.write(f"Cantidad de features detectados: {len(fvs)}")

    if len(fvs) > 0:
        quantizer = Quantizer(num_clusters=16)
        kmeans, centroids = quantizer.quantize(fvs)
        fv = quantizer.get_feature_vector(img_bgr, kmeans, centroids)
        st.write("Feature vector normalizado:")
        st.write(fv)

        # Mostrar histograma de clusters
        import matplotlib.pyplot as plt
        hist = np.histogram(kmeans.labels_, bins=16, range=(0,16))[0]
        fig, ax = plt.subplots()
        ax.bar(range(len(hist)), hist)
        ax.set_title("Distribución de clusters de features")
        st.pyplot(fig)

# st.page_link("menu", label="↩️ Regresar al menú principal", icon="🏠")

