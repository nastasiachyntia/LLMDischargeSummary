import streamlit as st
from google import genai
import datetime

# =========================
# KONFIGURASI API GEMINI
# =========================
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("Kunci 'GEMINI_API_KEY' tidak ditemukan di Secrets Streamlit.")
    st.stop()

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="AI Resume Medis STARKES",
    page_icon="⚕️",
    layout="centered"
)

st.title("⚕️ Standar Akreditasi Resume Medis (Discharge Summary)")
st.write("Format ini disesuaikan dengan Standar STARKES (AKP 5.2, HPK) & PMK Rekam Medis.")

# =========================
# INPUT DATA PASIEN (WAJIB STARKES)
# =========================
st.subheader("1. Identitas & Administrasi Pasien")
col1, col2 = st.columns(2)
with col1:
    nama = st.text_input("Nama Pasien*", placeholder="Contoh: Budi Santoso")
    no_rm = st.text_input("Nomor Rekam Medis (RM)*", placeholder="Contoh: 01-23-45")
with col2:
    umur = st.number_input("Umur Pasien*", min_value=0, max_value=120, step=1)
    gender = st.selectbox("Jenis Kelamin*", ["Laki-laki", "Perempuan"])

col3, col4 = st.columns(2)
with col3:
    tgl_masuk = st.date_input("Tanggal Masuk RS", datetime.date.today())
with col4:
    tgl_keluar = st.date_input("Tanggal Keluar RS", datetime.date.today())

st.subheader("2. Data Klinis (Anamnesis & Pemeriksaan)")
keluhan = st.text_area("Keluhan Utama / Indikasi Rawat (Subjective)*", placeholder="Alasan pasien masuk RS...")
pemeriksaan_penunjang = st.text_area("Hasil Pemeriksaan Penunjang Signifikan", placeholder="Hasil Lab abnormal, Rontgen, EKG, dll (Kosongkan jika tidak ada)")

st.subheader("3. Diagnosis, Tindakan & Terapi (Objective & Assessment)")
diagnosis = st.text_area("Diagnosis Utama & Diagnosis Sekunder (Komorbiditas)*", placeholder="Contoh: Utama: STEMI, Sekunder: DM Tipe 2")
tindakan = st.text_area("Prosedur / Tindakan Medis (ICD-9-CM)", placeholder="Contoh: Pemasangan LAD Ring / PCI (Kosongkan jika tidak ada)")
terapi = st.text_area("Terapi / Obat untuk Dibawa Pulang*", placeholder="Nama obat, dosis, frekuensi, rute pemberian...")

st.subheader("4. Rencana Tindak Lanjut (Plan & Edukasi HPK)")
instruksi_kontrol = st.text_input("Jadwal Kontrol Kembali*", placeholder="Contoh: Poli Jantung, Selasa 26 Mei 2026")
kondisi_pulang = st.selectbox("Kondisi Pasien Saat Pulang*", ["Sembuh", "Membaik", "Pindah RS/Dirujuk", "Pulang Paksa", "Meninggal Dunia"])

# =========================
# BUTTON GENERATE WITH STRICT PROMPT
# =========================
if st.button("Generate Resume Medis Resmi", type="primary"):

    # Validasi Kolom Wajib (Mencegah AI menebak data kosong)
    if not (nama and no_rm and keluhan and diagnosis and terapi and instruksi_kontrol):
        st.warning("Mohon lengkapi semua data bertanda bintang (*) terlebih dahulu agar AI tidak mengarang data!")
    else:
        with st.spinner("Menyusun Ringkasan Pulang sesuai standar akreditasi..."):
            try:
                # PROMPT KETAT: Melarang Halusinasi Medis
                prompt = f"""Bertindaklah sebagai Asisten Transkripsi Medis Resmi dan Auditor Akreditasi STARKES. 
Tugas Anda adalah menyusun data pasien berikut menjadi format Ringkasan Pulang (Discharge Summary) yang legal, rapi, dan terstruktur.

PANTANGAN UTAMA (STRICT RULES):
1. JANGAN PERNAH MENGARANG, MENAMBAHKAN, ATAU MENGASUMSIKAN DIAGNOSIS, GEJALA, ATAU OBAT YANG TIDAK TERTULIS DI BAWAH INI.
2. JANGAN MEMBUAT DATA HALUSINASI. Jika data penunjang atau tindakan tertulis kosong, tulis "Tidak ada" atau "Tidak dilakukan".
3. Fokus pada penataan struktur bahasa medis yang formal (Dilarang bercerita fiktif).

DATA PASIEN:
- Nama Pasien: {nama}
- No. Rekam Medis: {no_rm}
- Umur / Gender: {umur} Tahun / {gender}
- Tanggal Masuk: {tgl_masuk} | Tanggal Keluar: {tgl_keluar}
- Keluhan Utama (Indikasi Rawat): {keluhan}
- Hasil Penunjang (Lab/Rad): {pemeriksaan_penunjang if pemeriksaan_penunjang else 'Tidak Ada / Tidak Dilampirkan'}
- Diagnosis Utama/Sekunder: {diagnosis}
- Tindakan/Prosedur Medis: {tindakan if tindakan else 'Tidak Ada Tindakan Invasif/Operatif'}
- Terapi Obat Pulang: {terapi}
- Kondisi Saat Pulang: {kondisi_pulang}
- Jadwal Kontrol Kembali: {instruksi_kontrol}

FORMAT OUTPUT YANG WAJIB DIHASILKAN (Gunakan Markdown):
### RINGKASAN PULANG (DISCHARGE SUMMARY)
*Memenuhi Standar Akreditasi Kemenkes (STARKES AKP 5.2 & HPK)*

**I. IDENTITAS & ADMINISTRASI PASIEN**
* Nama Pasien: ...
* No. RM: ...
* Umur / Jenis Kelamin: ...
* Waktu Rawat: [Tanggal Masuk] s.d [Tanggal Keluar]

**II. RINGKASAN KLINIS (STARKES AKP 5.2.a)**
* Keluhan Utama / Indikasi Rawat Inap: ...
* Hasil Pemeriksaan Penunjang Signifikan: ...

**III. DIAGNOSIS & TINDAKAN (STARKES AKP 5.2.b & c)**
* Diagnosis Utama: ...
* Diagnosis Sekunder/Komorbid: ...
* Prosedur / Tindakan Medis: ...

**IV. PENATALAKSANAAN & TERAPI PULANG (STARKES AKP 5.2.d)**
* Daftar Obat Pulang (Aturan Pakai & Dosis): ...

**V. INSTRUKSI PASCA RAWAT & EDUKASI (STARKES AKP 5.2.e & f / HPK 2.1)**
* Kondisi Pasien Saat Pulang: ...
* Rencana Tindak Lanjut / Jadwal Kontrol: ...
* Edukasi Pasien (Tanda Bahaya Spesifik): (Berikan instruksi tanda bahaya darurat/red flags yang *hanya* relevan dengan diagnosis yang diinput di atas untuk segera ke IGD).

---
**LEMBAR PENGESAHAN SERAH TERIMA INFORMASI**
[ Slot Tanda Tangan DPJP ]                     [ Slot Tanda Tangan Pasien/Keluarga ]
"""

                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )

                st.success("Resume Medis Berhasil Distrukturkan!")
                st.subheader("📋 Hasil Ringkasan Pulang Resmi (Siap Cetak)")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Gagal menghubungi server Gemini: {e}")
