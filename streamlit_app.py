import streamlit as st

st.title("Automatic Resume Medis")

nama = st.text_input("Nama Pasien")
umur = st.number_input("Umur", 0, 120)
jk = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])

keluhan = st.text_area("Keluhan Utama")
diagnosis = st.text_area("Diagnosis")
terapi = st.text_area("Terapi")
lab = st.text_area("Hasil Laboratorium")

if st.button("Generate Resume"):

    hasil = f"""
    Pasien {nama}, usia {umur} tahun,
    dengan diagnosis {diagnosis}.

    Keluhan utama:
    {keluhan}

    Terapi:
    {terapi}

    Hasil laboratorium:
    {lab}
    """

    st.subheader("Resume Medis")
    st.write(hasil)
