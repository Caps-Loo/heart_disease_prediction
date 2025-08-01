import streamlit as st
import pandas as pd
import joblib
import warnings
warnings.filterwarnings('ignore')

# Load model
model = joblib.load("best_heart_disease_model.pkl")

# === HEADER ===
st.markdown("<h1 style='text-align: center;'>🫀 HeartWise</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Prediksi Risiko Penyakit Jantung</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Analisis risiko kesehatan berbasis Machine Learning.</p>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center;'>
    <img src='https://ik.imagekit.io/royalassets/Blog/gejala-serangan-jantung.jpg' width='600'>
</div>
""", unsafe_allow_html=True)

# === INPUT USER ===
st.markdown("## 📝 Input Manual Pengguna")

col1, col2 = st.columns(2)

with col1:
    cp = st.selectbox("Jenis Nyeri Dada", ["Tidak Nyeri", "Nyeri Ringan", "Nyeri Sedang", "Nyeri Berat"])
    thalach = st.slider("Detak Jantung Maksimum yang Dicapai", 71, 202, 150)
    slope = st.selectbox("Kemiringan Segmen ST Puncak Latihan", ["Menurun", "Datar", "Menanjak"])
    oldpeak = st.slider("Depresi ST yang Diinduksi oleh Latihan", 0.0, 6.2, 1.0, 0.1)
    exang = st.selectbox("Angina yang Diinduksi oleh Latihan", ["Tidak", "Ya"])
    ca = st.slider("Jumlah Pembuluh Darah Utama", 0, 3, 0)

with col2:
    thal = st.selectbox("Thalassemia", ["Normal", "Cacat Tetap", "Reversibel", "Tidak Diketahui"])
    sex = st.selectbox("Jenis Kelamin", ["Perempuan", "Laki-laki"])
    age = st.slider("Usia", 29, 77, 55)
    trestbps = st.slider("Tekanan Darah Saat Istirahat", 94, 200, 130)
    chol = st.slider("Jumlah Kolesterol", 126, 564, 246)
    fbs = st.selectbox("Gula Darah Puasa > 120 mg/dl", ["Tidak", "Ya"])
    restecg = st.selectbox("Hasil EKG Saat Istirahat", ["Normal", "Kelainan ST-T", "Hipertrofi Ventrikel Kiri"])

# === KONVERSI KE ANGKA ===
cp_map = {"Tidak Nyeri": 0, "Nyeri Ringan": 1, "Nyeri Sedang": 2, "Nyeri Berat": 3}
slope_map = {"Menurun": 0, "Datar": 1, "Menanjak": 2}
sex_map = {"Perempuan": 0, "Laki-laki": 1}
exang_map = {"Tidak": 0, "Ya": 1}
thal_map = {"Tidak Diketahui": 0, "Normal": 1, "Cacat Tetap": 2, "Reversibel": 3}
restecg_map = {"Normal": 0, "Kelainan ST-T": 1, "Hipertrofi Ventrikel Kiri": 2}
fbs_map = {"Tidak": 0, "Ya": 1}

input_data = pd.DataFrame([[
    age, sex_map[sex], cp_map[cp], trestbps, chol,
    fbs_map[fbs], restecg_map[restecg], thalach, exang_map[exang],
    oldpeak, slope_map[slope], ca, thal_map[thal]
]], columns=['age', 'sex', 'cp', 'trestbps', 'chol',
             'fbs', 'restecg', 'thalach', 'exang',
             'oldpeak', 'slope', 'ca', 'thal'])

# === TAMPILKAN DATA INPUT (opsional) ===
with st.expander("📋 Lihat Data Input"):
    st.dataframe(input_data)

# === TOMBOL PREDIKSI ===
st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        height: 50px;
        font-size: 20px;
        font-weight: bold;
        background-color: #4da3ff;
        color: white;
        border-radius: 8px;
        border: none;
        transition: background 0.2s, box-shadow 0.2s;
        box-shadow: 0 2px 8px rgba(77,163,255,0.08);
        cursor: pointer;
    }
    div.stButton > button:hover {
        background-color: #2176c7;
        box-shadow: 0 4px 16px rgba(33,118,199,0.15);
    }
    </style>
""", unsafe_allow_html=True)

if st.button("🔍 Prediksi", use_container_width=True):
    prediction = model.predict(input_data)[0]
    proba = model.predict_proba(input_data)[0][1]

    st.subheader("🔎 Hasil Prediksi")
    if prediction == 1:
        st.error("🚨 Tinggi Risiko Penyakit Jantung")
        st.metric("Probabilitas", f"{proba:.2%}")
        st.markdown("👉 **Segera konsultasikan ke dokter.** Hindari stres, perbanyak olahraga ringan, dan cek rutin.")
        
        # === SARAN PENCEGAHAN & PENANGGULANGAN ===
        st.markdown("---")
        st.markdown("### 🩺 Saran Pencegahan & Penanggulangan")
        
        # Membuat tabs untuk kategori saran
        tab1, tab2, tab3, tab4 = st.tabs(["💊 **Medis**", "🥗 **Pola Makan**", "🏃‍♂️ **Olahraga**", "🧘‍♀️ **Gaya Hidup**"])
        
        with tab1:
            st.markdown("""
            #### 🔬 Tindakan Medis Segera:
            
            **🚨 Prioritas Utama:**
            - **Konsultasi ke dokter kardiolog** dalam 1-2 minggu
            - **Pemeriksaan lanjutan**: EKG, Echocardiogram, Stress Test
            - **Cek laboratorium**: Profil lipid lengkap, HbA1c, Troponin
            - **Monitor tekanan darah** harian di rumah
            
            **💊 Kemungkinan Terapi:**
            - Obat penurun kolesterol (Statin)
            - Obat pengontrol tekanan darah (ACE inhibitor/ARB)
            - Aspirin dosis rendah (sesuai resep dokter)
            - Obat pengontrol gula darah (jika diabetes)
            
            **⚠️ Tanda Bahaya - Segera ke UGD:**
            - Nyeri dada hebat > 15 menit
            - Sesak napas mendadak
            - Keringat dingin + mual
            - Nyeri menjalar ke lengan/leher/rahang
            """)
        
        with tab2:
            st.markdown("""
            #### 🍎 Pola Makan Jantung Sehat:
            
            **✅ KONSUMSI LEBIH BANYAK:**
            - **Ikan berlemak**: Salmon, makarel, sarden (2-3x/minggu)
            - **Sayuran hijau**: Bayam, brokoli, kangkung
            - **Buah-buahan**: Alpukat, berry, apel, jeruk
            - **Kacang-kacangan**: Almond, walnut, kacang merah
            - **Whole grains**: Oatmeal, quinoa, beras merah
            - **Olive oil** untuk memasak
            
            **❌ HINDARI/BATASI:**
            - **Garam**: Maksimal 1 sendok teh/hari
            - **Gula tambahan**: Minuman manis, kue, permen
            - **Lemak jenuh**: Daging berlemak, mentega, santan kental
            - **Makanan olahan**: Sosis, nugget, makanan kaleng
            - **Gorengan dan makanan cepat saji**
            
            **📊 Porsi Ideal:**
            - Sayur: 2-3 porsi/hari
            - Buah: 2 porsi/hari  
            - Protein: Seukuran telapak tangan
            - Karbohidrat: 1/4 piring
            """)
        
        with tab3:
            st.markdown("""
            #### 🏃‍♂️ Program Olahraga Aman:
            
            **🎯 Target Mingguan:**
            - **150 menit olahraga sedang** ATAU **75 menit olahraga berat**
            - **2-3 hari latihan kekuatan**
            - **Setiap hari**: Aktivitas ringan 30 menit
            
            **🚶‍♂️ Olahraga Kardio Aman:**
            - **Jalan cepat**: 30-45 menit, 5x/minggu
            - **Berenang**: 20-30 menit, 3x/minggu
            - **Bersepeda santai**: 30-60 menit
            - **Senam aerobik ringan**: 20-30 menit
            
            **💪 Latihan Kekuatan:**
            - Push-up (sesuai kemampuan)
            - Angkat beban ringan (0.5-2 kg)
            - Resistance band exercises
            - Yoga atau Pilates
            
            **⚠️ Aturan Keamanan:**
            - Mulai perlahan, tingkatkan bertahap
            - Stop jika merasa nyeri dada/sesak
            - Pemanasan 5-10 menit
            - Pendinginan 5-10 menit
            - Monitor denyut nadi saat olahraga
            """)
        
        with tab4:
            st.markdown("""
            #### 🧘‍♀️ Perubahan Gaya Hidup:
            
            **🚭 Berhenti Merokok:**
            - **Segera hentikan** - risiko menurun 50% dalam 1 tahun
            - Gunakan nicotine patch/gum jika perlu
            - Hindari asap rokok (perokok pasif)
            - Konsultasi program berhenti merokok
            
            **😴 Kualitas Tidur:**
            - **7-8 jam tidur** setiap malam
            - **Jadwal tidur teratur** (jam yang sama)
            - Hindari kafein 6 jam sebelum tidur
            - Kamar gelap, sejuk, dan tenang
            
            **🧠 Manajemen Stres:**
            - **Meditasi/mindfulness**: 10-20 menit/hari
            - **Teknik pernapasan dalam**
            - **Hobi yang menyenangkan**: Berkebun, membaca, musik
            - **Sosialisasi** dengan keluarga/teman
            - **Batasi berita negatif** dan media sosial
            
            **⚖️ Kontrol Berat Badan:**
            - **BMI ideal**: 18.5-24.9
            - **Lingkar pinggang**: <90cm (pria), <80cm (wanita)
            - **Penurunan bertahap**: 0.5-1 kg/minggu
            - **Catat makanan** harian (food diary)
            
            **🩺 Monitoring Rutin:**
            - **Cek tekanan darah**: 2x/hari
            - **Timbang berat badan**: 1x/minggu  
            - **Cek gula darah**: Sesuai anjuran dokter
            - **Kontrol dokter**: Setiap 1-3 bulan
            """)
        
        # Alert box dengan action plan
        st.markdown("---")
        st.info("""
        ### 📋 **Rencana Aksi 30 Hari Pertama:**
        
        **Minggu 1-2:**
        ✅ Konsultasi dokter & pemeriksaan lanjutan  
        ✅ Mulai jalan kaki 15-20 menit/hari  
        ✅ Kurangi garam & gula dalam makanan  
        
        **Minggu 3-4:**
        ✅ Tingkatkan olahraga jadi 30 menit/hari  
        ✅ Terapkan pola makan mediterania  
        ✅ Mulai teknik relaksasi/meditasi  
        
        **🎯 Target 1 Bulan:** Penurunan berat 2-4 kg, tekanan darah terkontrol, kolesterol mulai turun
        """)
        
    else:
        st.success("✅ Risiko Rendah")
        st.metric("Probabilitas", f"{proba:.2%}")
        st.markdown("👍 **Tetap jaga pola hidup sehat!**")
        
        # Saran untuk risiko rendah
        st.markdown("---")
        st.markdown("### 🌟 Saran Mempertahankan Kesehatan Jantung")
        
        st.info("""
        **🎯 Tetap Waspada & Jaga Konsistensi:**
        
        **✅ Lanjutkan Kebiasaan Baik:**
        - Olahraga teratur 150 menit/minggu
        - Konsumsi buah & sayur 5 porsi/hari
        - Tidur cukup 7-8 jam/malam
        - Kelola stres dengan baik
        
        **🩺 Pemeriksaan Rutin:**
        - Cek kesehatan umum: 1 tahun sekali
        - Monitor tekanan darah: 3-6 bulan sekali
        - Cek kolesterol: 1-2 tahun sekali
        
        **⚠️ Tetap Hindari:**
        - Merokok dan alkohol berlebihan
        - Makanan tinggi garam & lemak jenuh
        - Gaya hidup sedentari (kurang gerak)
         
        """)

# === EDUKASI PENGGUNA ===
with st.expander("📖 Deskripsi Fitur"):
    st.markdown("""
    ### 🔍 Penjelasan Setiap Fitur Input:

    - **Usia (`age`)**: Umur pasien dalam tahun. Risiko penyakit jantung biasanya meningkat seiring bertambahnya usia.

    - **Jenis Kelamin (`sex`)**:
        - `0`: Perempuan
        - `1`: Laki-laki  
        Studi menunjukkan laki-laki memiliki risiko sedikit lebih tinggi.

    - **Jenis Nyeri Dada (`cp`)**:
        - `0`: Tidak Nyeri
        - `1`: Nyeri Ringan
        - `2`: Nyeri Sedang
        - `3`: Nyeri Berat  
        Nyeri dada tipe berat biasanya lebih mengarah ke masalah jantung.

    - **Tekanan Darah Saat Istirahat (`trestbps`)**: Tekanan darah saat tidak beraktivitas. Tekanan tinggi meningkatkan risiko jantung.

    - **Kolesterol (`chol`)**: Jumlah kolesterol dalam darah (mg/dL). Nilai tinggi berhubungan dengan penumpukan plak.

    - **Gula Darah Puasa (`fbs`)**:
        - `1`: >120 mg/dL
        - `0`: ≤120 mg/dL  
        Diabetes atau pra-diabetes meningkatkan risiko kardiovaskular.

    - **Hasil EKG Saat Istirahat (`restecg`)**:
        - `0`: Normal
        - `1`: ST-T abnormal
        - `2`: Hipertrofi ventrikel kiri  
        Kelainan jantung bisa terdeteksi dari EKG.

    - **Detak Jantung Maksimum (`thalach`)**: Maksimum denyut jantung saat olahraga. Nilai rendah dapat menunjukkan masalah jantung.

    - **Angina Saat Latihan (`exang`)**:
        - `1`: Ya
        - `0`: Tidak  
        Jika nyeri dada muncul saat latihan, bisa jadi ada sumbatan.

    - **Oldpeak (`oldpeak`)**: Penurunan segmen ST dibandingkan saat istirahat. Nilai tinggi menunjukkan iskemia.

    - **Kemiringan ST (`slope`)**:
        - `0`: Menurun
        - `1`: Datar
        - `2`: Menanjak  
        Bentuk ST dapat mengindikasikan stres pada jantung.

    - **Jumlah Pembuluh Tersumbat (`ca`)**: Jumlah pembuluh darah utama yang menunjukkan penyumbatan (0–3). Semakin banyak, semakin tinggi risiko.

    - **Thalassemia (`thal`)**:
        - `1`: Normal
        - `2`: Cacat Tetap (Fixed Defect)
        - `3`: Defek Reversibel
        - `0`: Tidak Diketahui  
        Kondisi ini dapat memengaruhi transportasi oksigen dalam darah.
    """)

# === DISCLAIMER ===
with st.expander("⚠️ Disclaimer & Saran Medis"):
    st.markdown("""
    🔔 **Catatan Penting:**

    - Hasil prediksi ini dihasilkan oleh model machine learning berbasis data.
    - Model ini **tidak menggantikan diagnosis medis langsung** dari tenaga kesehatan profesional.
    - Selalu **konsultasikan ke dokter** atau ahli medis untuk pemeriksaan lanjutan dan akurat.
    - Prediksi hanya memberikan **indikasi risiko**, bukan keputusan medis mutlak.
    - **Saran pencegahan** yang diberikan bersifat umum dan sebaiknya disesuaikan dengan kondisi individual masing-masing.

    🙏 Terima kasih telah menggunakan **HeartWise**. Sehat Selalu!
    """)

# === FOOTER ===
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("© 2025 Raihan Pratama. All Rights Reserved.", unsafe_allow_html=True)