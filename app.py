import streamlit as st
from PIL import Image
import numpy as np

# OCR libraries
import easyocr
import keras_ocr
from textblob import TextBlob

st.set_page_config(page_title="Robust AI OCR MVP", layout="centered")
st.title("🤖 Multi-Agent OCR + NLP MVP")

uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg","jpeg","png","tiff"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)

    img_array = np.array(image)
    results = []

    # --- Strategy 1: EasyOCR ---
    try:
        reader = easyocr.Reader(['en'], gpu=False)
        res = reader.readtext(img_array, detail=0)
        if res:
            results.append(" ".join(res))
    except Exception as e:
        results.append(f"[EasyOCR failed: {e}]")

    # --- Strategy 2: Keras-OCR ---
    try:
        pipeline = keras_ocr.pipeline.Pipeline()
        prediction_groups = pipeline.recognize([img_array])
        text = " ".join([word for word, box in prediction_groups[0]])
        if text:
            results.append(text)
    except Exception as e:
        results.append(f"[Keras-OCR failed: {e}]")

    # --- Combine results ---
    st.subheader("🔍 Extracted Sentences")
    for i, txt in enumerate(results, 1):
        st.write(f"Method {i}: {txt}")

    # --- Correction Step ---
    st.subheader("✅ Corrected Sentences (Spell + Grammar)")
    for i, txt in enumerate(results, 1):
        if txt and not txt.startswith("["):
            corrected = str(TextBlob(txt).correct())
            st.write(f"Method {i}: {corrected}")
