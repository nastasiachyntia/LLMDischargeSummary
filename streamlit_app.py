import streamlit as st
import google.generativeai as genai

# API KEY (Sudah benar menggunakan st.secrets)
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except KeyError:
    st.error("API Key 'GEMINI_API_KEY' tidak ditemukan di Secrets Streamlit!")

# MODEL (Diubah ke model terbaru yang aktif)
# Kamu bisa pakai 'gemini-2.5-flash' atau 'gemini-1.5-flash'
model = genai.GenerativeModel("gemini-1.5-flash")

# TITLE
st.title("⚕️ AI Resume Medis")
st.write("Isi data di bawah ini untuk membuat resume medis otomatis.")

# INPUT
nama = st.text_input("Nama Pasien")
diagnosis = st.text_area("Diagnosis / Riwayat Penyakit")
keluhan = st.text_area("Keluhan Saat Ini")

# BUTTON
if st.button("Generate AI Resume"):
    # Validasi: Memastikan user sudah mengisi semua kolom sebelum menembak API
    if nama and diagnosis and keluhan:
        with st.spinner("Sedang meracik resume medis..."):
            try:
                prompt = f"""
                Buatkan resume medis profesional dalam Bahasa Indonesia yang rapi.
                 Gunakan format medis yang standar (seperti subjektif, objektif, asesmen).

                Nama pasien: {nama}

                Diagnosis:
                {diagnosis}

                Keluhan:
                {keluhan}
                """

                response = model.generate_content(prompt)

                st.success("Resume berhasil dibuat!")
                st.subheader("Hasil Resume Medis")
                st.markdown(response.text) # Menggunakan st.markdown agar format teks dari Gemini (seperti bold/bullet) muncul dengan rapi
                
            except Exception as e:
                st.error(f"Terjadi kesalahan saat menghubungi Gemini: {e}")
    else:
        st.warning("Mohon lengkapi semua data (Nama, Diagnosis, dan Keluhan) terlebih dahulu!")
