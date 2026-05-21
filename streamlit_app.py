import streamlit as st
import google.generativeai as genai

# API KEY
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# MODEL
model = genai.GenerativeModel("gemini-1.5-flash")

# UI
st.title("AI Resume Medis")

nama = st.text_input("Nama Pasien")
umur = st.number_input("Umur", 0, 120)

keluhan = st.text_area("Keluhan Utama")
diagnosis = st.text_area("Diagnosis")
terapi = st.text_area("Terapi")

# BUTTON
if st.button("Generate AI Resume"):

    prompt = f"""
    Buatkan resume medis profesional Bahasa Indonesia.

    Nama Pasien: {nama}
    Umur: {umur}

    Keluhan:
    {keluhan}

    Diagnosis:
    {diagnosis}

    Terapi:
    {terapi}

    Format:
    1. Diagnosis
    2. Keluhan utama
    3. Terapi
    4. Kondisi pasien
    """

    response = model.generate_content(prompt)

    st.subheader("Hasil Resume Medis")
    st.write(response.text)
