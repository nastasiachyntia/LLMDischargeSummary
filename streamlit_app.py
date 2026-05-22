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
                # PROMPT LLM
                # =========================
                prompt = f"""
