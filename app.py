import streamlit as st
from PIL import Image
import numpy as np
import random

# NLP / LLM
from textblob import TextBlob
from transformers import pipeline

st.set_page_config(page_title="Ultimate AI OCR MVP", layout="centered")
st.title("🤖 Multi-Strategy AI OCR + NLP MVP")

uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg","jpeg","png","tiff"])

def safe_run(func, name, default=""):
    """Run a function safely. Always return something."""
    try:
        return func()
    except Exception as e:
        return f"[{name} failed → fallback used] {default}"

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)

    strategies = []

    # --- Strategy 1: Try pytesseract (if available) ---
    def strat_tesseract():
        import pytesseract
        return pytesseract.image_to_string(image)
    strategies.append(("Tesseract OCR", strat_tesseract))

    # --- Strategy 2: Pixel intensity hack (fake OCR baseline) ---
    def strat_pixels():
        arr = np.array(image)
        mean_val = arr.mean()
        return f"Image brightness level {mean_val:.2f} → might contain text."
    strategies.append(("Pixel Analysis", strat_pixels))

    # --- Strategy 3: Transformers tiny model generator ---
    def strat_transformers():
        gen = pipeline("text-generation", model="distilgpt2")
        return gen("OCR output:", max_new_tokens=20)[0]["generated_text"]
    strategies.append(("Generative AI (LLM)", strat_transformers))

    # --- Strategy 4: Random Markov-ish fallback ---
    def strat_random():
        words = ["AI","Quantum","Vision","Agent","Future","Neural","Twin","Cognitive","Knowledge","Graph"]
        return " ".join(random.choices(words, k=8))
    strategies.append(("Random AI Generator", strat_random))

    # Run all strategies safely
    st.subheader("🔍 Multi-Strategy Outputs")
    results = []
    for name, func in strategies:
        out = safe_run(func, name, default="No result")
        st.write(f"**{name}:** {out}")
        results.append(out)

    # --- Correction with TextBlob ---
    st.subheader("✅ Spell + Grammar Correction")
    for i, text in enumerate(results, 1):
        if text and not text.startswith("["):
            corrected = str(TextBlob(text).correct())
            st.write(f"Method {i}: {corrected}")
