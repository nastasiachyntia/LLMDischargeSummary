import streamlit as st
from google import genai

# INBOARDS DATA / MODUL SECURITY (Streamlit Secrets)
# SDK Baru otomatis membaca st.secrets["GEMINI_API_KEY"] di background jika namanya sesuai,
# namun untuk memastikan tidak error, kita inisialisasi secara eksplisit:
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("Waduh! Kunci 'GEMINI_API_KEY' tidak ditemukan di Secrets Streamlit kamu.")
    st.stop()

# TITLE & HEADER
st.set_page_config(page_title="AI Resume Medis", page_icon="⚕️")
st.title("⚕️ AI Resume Medis TESTINGGGGGGG ")
st.write("Aplikasiini otomatis menyusun resume medis standar berdasarkan input dokter dengan data  gemini open AI.")

# INPUT DATA PASIEN
nama = st.text_input("Nama Pasien", placeholder="Contoh: Budi Santoso")
umur = st.number_input("Umur Pasien", min_value=0, max_value=120, step=1)
keluhan = st.text_area("Keluhan Saat Ini", placeholder="Contoh: Luka di kaki kanan tidak kunjung sembuh, pusing, dan lemas.")
diagnosis = st.text_area("Diagnosis / Riwayat Penyakit", placeholder="Contoh: Diabetes Melitus Tipe 2, Hipertensi Stage 1")

# BUTTON GENERATE
if st.button("Generate AI Resume", type="primary"):
    # Cek apakah input kosong
    if not nama or not diagnosis or not keluhan:
        st.warning("Mohon lengkapi data Nama, Umur, Diagnosis, dan Keluhan pasien terlebih dahulu!")
    else:
        with st.spinner("Gemini sedang menyusun resume medis profesional..."):
            try:
                # Membuat prompt yang mengarahkan AI agar berformat medis resmi
                prompt = f"""
                Bertindaklah sebagai Dokter Spesialis Senior. Buatkan resume medis profesional, formal, 
                dan terstruktur dalam Bahasa Indonesia yang baik dan benar.

                Format resume harus mencakup:
                1. Identitas Pasien (Nama)
                2. Keluhan Utama (Subjective)
                3. Diagnosis & Riwayat (Assessment)
                4. Rekomendasi Rencana Tindakan / Edukasi Pasien (Plan)

                Data Pasien:
                - Nama Pasien: {nama}
                - Diagnosis: {diagnosis}
                - Umur: {umur}
                - Keluhan saat ini: {keluhan}
                """

                # Memanggil MODEL TERBARU yang aktif saat ini: gemini-2.5-flash
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )

                # Menampilkan Hasil
                st.success("Resume Medis Berhasil Dibuat!")
                st.subheader("📋 Hasil Resume Medis")
                st.markdown(response.text) # Menggunakan markdown agar bullet point & text bold rapi
                
            except Exception as e:
                st.error(f"Gagal menghubungi server Gemini: {e}")
