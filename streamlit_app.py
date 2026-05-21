import streamlit as st
import google.generativeai as genai

# API KEY
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# MODEL
model = genai.GenerativeModel("gemini-pro")

# TITLE
st.title("AI Resume Medis")

# INPUT
nama = st.text_input("Nama Pasien")
diagnosis = st.text_area("Diagnosis")
keluhan = st.text_area("Keluhan")

# BUTTON
if st.button("Generate AI Resume"):

    prompt = f"""
    Buatkan resume medis profesional Bahasa Indonesia.

    Nama pasien: {nama}

    Diagnosis:
    {diagnosis}

    Keluhan:
    {keluhan}
    """

    response = model.generate_content(prompt)

    st.subheader("Hasil Resume")
    st.write(response.text)
