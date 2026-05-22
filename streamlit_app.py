import streamlit as st
from google import genai

# =========================
# KONFIGURASI API GEMINI
# =========================
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)

except Exception:
    st.error(
        "Waduh! Kunci 'GEMINI_API_KEY' tidak ditemukan di Secrets Streamlit."
    )
    st.stop()

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="AI Resume Medis",
    page_icon="⚕️",
    layout="centered"
)

# =========================
# HEADER
# =========================
st.title("⚕️ AI Resume Medis")
st.write(
    """
    Aplikasi ini membantu menyusun resume medis profesional
    menggunakan Gemini AI berdasarkan data pasien.
    """
)

# =========================
# INPUT DATA PASIEN
# =========================
nama = st.text_input(
    "Nama Pasien",
    placeholder="Contoh: Budi Santoso"
)

umur = st.number_input(
    "Umur Pasien",
    min_value=0,
    max_value=120,
    step=1
)

keluhan = st.text_area(
    "Keluhan Saat Ini",
    placeholder="Contoh: Luka di kaki kanan tidak kunjung sembuh, pusing, dan lemas."
)

diagnosis = st.text_area(
    "Diagnosis / Riwayat Penyakit",
    placeholder="Contoh: Diabetes Melitus Tipe 2, Hipertensi Stage 1"
)

terapi = st.text_area(
    "Terapi / Obat",
    placeholder="Contoh: Metformin 500 mg 2x1"
)

# =========================
# BUTTON GENERATE
# =========================
if st.button("Generate AI Resume", type="primary"):

    # VALIDASI INPUT
    if not nama or not diagnosis or not keluhan:
        st.warning(
            "Mohon lengkapi data Nama, Diagnosis, dan Keluhan pasien terlebih dahulu!"
        )

    else:

        with st.spinner("Gemini sedang menyusun resume medis profesional..."):

            try:

                # =========================
                # PROMPT LLM (Sudah Diperbaiki & Ditutup)
                # =========================
                prompt = f"""Bertindaklah sebagai Dokter Spesialis Senior. Buatkan resume medis profesional, formal, dan terstruktur dalam Bahasa Indonesia yang baik dan benar.

Format resume harus mencakup:
1. Ringkasan Identitas Pasien (Nama, Umur)
2. Keluhan Utama Pasien (Subjective)
3. Hasil Evaluasi & Riwayat Penyakit (Assessment)
4. Rencana Terapi saat ini & Edukasi Tambahan (Plan)

Data Pasien:
- Nama Pasien: {nama}
- Umur Pasien: {umur} tahun
- Keluhan saat ini: {keluhan}
- Diagnosis / Riwayat: {diagnosis}
- Terapi / Obat saat ini: {terapi if terapi else 'Tidak ada obat sebelumnya'}"""

                # =========================
                # PANGGIL API GEMINI
                # =========================
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )

                # =========================
                # TAMPILKAN HASIL
                # =========================
                st.success("Resume Medis Berhasil Dibuat!")
                st.subheader("📋 Hasil Resume Medis Resmi")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"Gagal menghubungi server Gemini: {e}")
