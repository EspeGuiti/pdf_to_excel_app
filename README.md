import streamlit as st
import fitz # PyMuPDF
import pandas as pd
import io

def extract_text_from_pdf(uploaded_file):
doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
text_data = []
for page_num, page in enumerate(doc, start=1):
text = page.get_text()
text_data.append({"Page": page_num, "Text": text.strip()})
return pd.DataFrame(text_data)

def convert_df_to_excel(df):
output = io.BytesIO()
with pd.ExcelWriter(output, engine='openpyxl') as writer:
df.to_excel(writer, index=False, sheet_name='PDF Text')
processed_data = output.getvalue()
return processed_data

# Streamlit UI
st.title("📄 PDF to Excel Converter")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
with st.spinner("Extracting text from PDF..."):
df = extract_text_from_pdf(uploaded_file)

st.success("Text extracted successfully!")
st.dataframe(df)

excel_data = convert_df_to_excel(df)

st.download_button(
label="📥 Download Excel File",
data=excel_data,
file_name="pdf_text_output.xlsx",
mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
