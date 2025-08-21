import streamlit as st
from PIL import Image
import pytesseract
from textblob import TextBlob

st.set_page_config(page_title="AI Image → Sentence MVP", layout="centered")

st.title("🧠 AI Agentic MVP (OCR + Spell/Grammar Fix)")

uploaded_file = st.file_uploader("📤 Upload an image (jpg/jpeg/png/tiff)", 
                                 type=["jpg", "jpeg", "png", "tiff"])

if uploaded_file:
    # Load image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # OCR extraction
    raw_text = pytesseract.image_to_string(image)

    if raw_text.strip():
        st.subheader("🔍 Extracted Sentence (OCR)")
        st.write(raw_text)

        # Basic NLP correction
        corrected = str(TextBlob(raw_text).correct())

        st.subheader("✅ Corrected Sentence (Spell + Grammar)")
        st.write(corrected)
    else:
        st.warning("⚠️ No readable text found in image. Try clearer input.")
