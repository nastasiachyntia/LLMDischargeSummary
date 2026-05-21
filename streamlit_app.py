import streamlit as st

st.title("AI Resume Medis")

nama = st.text_input("Nama Pasien")
diagnosis = st.text_area("Diagnosis")

if st.button("Generate"):
    st.write(f"Pasien {nama} dengan diagnosis {diagnosis}")
