import streamlit as st
import pandas as pd
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import io

# 🧠 Le decimos a pytesseract dónde está el ejecutable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image_pdf(uploaded_file):
    images = convert_from_bytes(uploaded_file.read(), dpi=300)
    text_data = []
    for i, img in enumerate(images):
        text = pytesseract.image_to_string(img)
        text_data.append({"Page": i + 1, "Text": text.strip()})
    return pd.DataFrame(text_data)

def convert_df_to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='OCR Text')
    return output.getvalue()

st.title("📄 PDF (Image OCR) to Excel Converter")

uploaded_file = st.file_uploader("Upload a scanned/image PDF", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Performing OCR on PDF..."):
        df = extract_text_from_image_pdf(uploaded_file)

    st.success("OCR completed successfully!")
    st.dataframe(df)

    excel_data = convert_df_to_excel(df)

    st.download_button(
        label="📥 Download Excel File",
        data=excel_data,
        file_name="ocr_text_output.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )