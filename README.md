# Analisis Komoditas Pangan Kota Cirebon vs Kabupaten Cirebon

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Grafik-Plotly-3F4F75?logo=plotly&logoColor=white)
![Data](https://img.shields.io/badge/Data-PIHPS%20Bank%20Indonesia-1E3A8A)

Dashboard interaktif dan arsip hasil analisis tentang **keterkaitan harga** dan **risiko lonjakan ekstrem** komoditas pangan strategis di **Kota Cirebon** dan **Kabupaten Cirebon**, dengan fokus pada **tiga jenis cabai**. Data yang dipakai adalah data harian PIHPS Bank Indonesia, Januari 2020 – September 2026.

> ⚠️ **Penting:** seluruh hasil adalah **keterkaitan statistik**, bukan sebab-akibat. Proyek ini tidak menjelaskan *mengapa* harga melonjak (pasokan, cuaca, hari raya) dan tidak menunjukkan bahwa satu wilayah *menyebabkan* perubahan harga di wilayah lain.

---

## 📌 Daftar isi

1. [Pertanyaan yang dijawab](#-pertanyaan-yang-dijawab)
2. [Temuan utama](#-temuan-utama)
3. [Isi dashboard](#-isi-dashboard)
4. [Struktur repositori](#-struktur-repositori)
5. [Cara menjalankan di komputer sendiri](#-cara-menjalankan-di-komputer-sendiri)
6. [Cara membagikan secara online (Streamlit Cloud)](#-cara-membagikan-secara-online-streamlit-cloud)
7. [Data dan sumbernya](#-data-dan-sumbernya)
8. [Metode analisis singkat](#-metode-analisis-singkat)
9. [Keterbatasan](#-keterbatasan)
10. [Pemecahan masalah](#-pemecahan-masalah)
11. [Memperbarui atau menambah data](#-memperbarui-atau-menambah-data)
12. [Lisensi dan kontak](#-lisensi-dan-kontak)

---

## ❓ Pertanyaan yang dijawab

1. **Seberapa cepat** harga di Kota dan Kabupaten Cirebon saling menyesuaikan bila terjadi selisih?
2. **Wilayah mana** yang lebih aktif menyesuaikan?
3. **Seberapa besar dan sering** lonjakan harga ekstrem terjadi?
4. Apakah lonjakan ekstrem di satu wilayah **diikuti serentak** di wilayah lain?
5. Adakah **pola di sekitar hari raya** (Idulfitri dan Iduladha)?
6. Mengapa harga di Kota **biasanya sedikit lebih mahal**?

**Cakupan komoditas (8):** beras kualitas medium I, bawang merah, bawang putih, cabai merah besar, cabai merah keriting, cabai rawit merah, daging ayam ras, telur ayam ras.
Analisis mendalam (penyesuaian, risiko ekstrem, hari raya, premi) dikerjakan untuk **tiga cabai**; lima komoditas lain berfungsi sebagai **pembanding**.

---

## 🔑 Temuan utama

| # | Temuan | Angka (rentang antar-spesifikasi) | Tingkat bukti |
|---|--------|-----------------------------------|---------------|
| 1 | Selisih harga Kota–Kabupaten **cepat menutup**: separuhnya hilang dalam sekitar 1–2 hari kerja | half-life **0,9–1,7 hari** | Temuan (Tingkat 1) |
| 2 | **Kabupaten** yang aktif menyesuaikan ke Kota | koreksi α_B **0,23–0,42** per hari kerja | Temuan (Tingkat 1) |
| 3 | Lonjakan ekstrem terjadi **serentak** di kedua wilayah, bukan menjalar bertahap | peluang ikut melonjak **0,63–0,83** (acuan jika saling bebas: 0,05) | Temuan (Tingkat 1) |
| 4 | Risiko harian lonjakan ≥20% | sekitar **1,7–2,9 kejadian per 250 hari kerja** (interval 1 hari) | Indikasi (Tingkat 2) |
| 5 | Premi Kota berupa **markup nominal** yang relatif tetap, bukan proporsional terhadap harga | sekitar **Rp 900–1.400** | Indikasi (Tingkat 2) |
| 6 | Harga cabai cenderung naik menjelang Iduladha dan turun sepekan sesudah hari raya | pola **deskriptif**, 7 peristiwa, tidak lolos koreksi Holm | Indikasi (Tingkat 2) |

**Yang tidak disimpulkan:** bahwa Kota "memimpin" Kabupaten atau sebaliknya (kedua arah punya daya prediksi dan selisihnya tidak signifikan); bentuk ekor distribusi lonjakan (berat atau terbatas) karena tidak teridentifikasi; dan "tidak ada asimetri" (uji asimetri berdaya rendah, sehingga hasil tidak signifikan bukan bukti simetri).

---

## 📊 Isi dashboard

| Tab | Yang bisa dilakukan |
|-----|---------------------|
| 🏠 **Ringkasan** | Angka kunci, enam pesan utama dengan tingkat buktinya, dan ringkasan klaim |
| 📈 **Harga** | Pilih komoditas dan rentang tanggal, tandai lonjakan dan hari raya, lihat selisih Kota–Kabupaten, zoom dengan slider |
| 🔁 **Penyesuaian** | Kecepatan penyesuaian (half-life), siapa yang menyesuaikan (α), dan simulasi interaktif |
| ⚡ **Risiko** | Besar dan frekuensi lonjakan, keserentakan ekstrem (χ), serta kalkulator frekuensi dari data |
| 🎉 **Hari raya** | Pola harga sebelum dan sesudah Idulfitri dan Iduladha, lintasan per tahun |
| 💰 **Premi Kota** | Mengapa Kota sedikit lebih mahal: uji markup nominal vs proporsional, rezim, elastisitas jangka panjang |
| ✅ **Bukti & batasan** | Register klaim dengan tingkat bukti, daftar keterbatasan, definisi istilah |
| 🧪 **Data & unduhan** | Pemeriksaan integritas, kelengkapan data, unduh tabel hasil |

Tersedia **Mode presentasi** di sisi kiri untuk huruf dan grafik yang lebih besar saat dipresentasikan.

> 💡 Tambahkan tangkapan layar di sini agar README lebih menarik: simpan gambar di folder `docs/` lalu tulis `![Tampilan dashboard](docs/screenshot.png)`.

---

## 🗂️ Struktur repositori

```
analisis-komoditas-pangan-kota-cirebon-kabupaten-cirebon/
├── README.md              ← berkas ini (harus di folder paling luar)
├── requirements.txt       ← daftar paket Python (lihat bagian instalasi)
├── dashboard/
│   └── app.py             ← kode dashboard Streamlit
└── data/                  ← keluaran analisis (dibaca dashboard)
    ├── data_harga_eda5.csv                  harga harian terbersih (Tahap 5)
    ├── data_perubahan_bersama_eda5.csv      perubahan harga pada tanggal bersama (Tahap 5)
    ├── kalender_libur_resmi_2020_2026_vs_data_PIHPS.csv
    ├── t12a_rezim.csv                       rezim rata-rata selisih
    ├── t13a_markup.csv, t13b_dols.csv       uji markup dan elastisitas jangka panjang
    ├── t13g_chi_final.csv                   keserentakan ekstrem (χ)
    ├── t14a_evt_skala_interval.csv          risiko ekstrem (level kembali, laju lonjakan)
    ├── t14b_ecm_spesifikasi.csv             half-life dan koefisien koreksi
    ├── t14c_hari_raya_peristiwa.csv         pola hari raya
    ├── t15a_keluarga_utama.csv              uji utama (koreksi uji ganda Holm)
    ├── t15b_analisis_daya.csv               analisis daya uji asimetri
    ├── t15e_*.csv                           arah pengaruh dan kekhasan cabai
    ├── t15f_daftar_klaim.csv                register klaim dan tingkat bukti
    └── t16e_definisi.csv, t16e_keterbatasan.csv
```

Dashboard mencari berkas **berdasarkan nama**, jadi susunan sub-folder di dalam `data/` bebas.

---

## 💻 Cara menjalankan di komputer sendiri

**Kebutuhan:** Python 3.10 atau lebih baru dan Git.

```bash
# 1. Unduh repositori
git clone https://github.com/liwauddin928-arch/analisis-komoditas-pangan-kota-cirebon-kabupaten-cirebon.git
cd analisis-komoditas-pangan-kota-cirebon-kabupaten-cirebon

# 2. (Disarankan) buat lingkungan virtual
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux

# 3. Pasang paket
pip install -r requirements.txt

# 4. Jalankan dari folder paling luar (tempat folder data berada)
streamlit run dashboard/app.py
```

Browser akan terbuka di `http://localhost:8501`.

**Isi `requirements.txt` yang dibutuhkan:**

```
streamlit>=1.40
pandas>=2.0
numpy>=1.26
plotly>=5.20
```

> ⚠️ Jalankan perintah dari **folder paling luar**, bukan dari dalam `dashboard/`. Dashboard membaca folder `./data` relatif terhadap tempat perintah dijalankan. Bila Anda menjalankannya dari tempat lain, ubah kolom **📁 Folder data** di sisi kiri dashboard, atau atur variabel lingkungan `DATA_ROOT`.

---

## ☁️ Cara membagikan secara online (Streamlit Cloud)

1. Pastikan `requirements.txt` ada di folder paling luar dan hanya berisi empat paket di atas.
2. Buka [share.streamlit.io](https://share.streamlit.io) dan masuk dengan akun GitHub.
3. Klik **Create app**, pilih repositori ini dan cabang `main`.
4. Pada **Main file path**, isi `dashboard/app.py`.
5. Klik **Deploy**. Tautan publik akan muncul setelah beberapa menit.
6. Tempel tautan itu di bagian **Website** pada kolom *About* repositori.

---

## 🗃️ Data dan sumbernya

- **Sumber:** Pusat Informasi Harga Pangan Strategis (PIHPS) Nasional, Bank Indonesia.
- **Periode:** Januari 2020 – September 2026, data harian hari kerja.
- **Cakupan:** Kota Cirebon dan Kabupaten Cirebon, 8 komoditas.
- **Observasi bersama:** 1.690 tanggal per komoditas (tanggal ketika harga valid di kedua wilayah).
- **Perubahan perlakuan hari libur:** pada 2020–2022 hari libur resmi hampir selalu kosong; sejak 2023 sebagian besar berisi harga hari sebelumnya yang dibawa ("hari beku"). Hari beku diperlakukan sebagai tidak ada pengamatan pada analisis lanjut.

Gunakan data sesuai ketentuan penggunaan dari sumber aslinya. Berkas di folder `data/` adalah **hasil olahan**, bukan pengganti data resmi.

---

## 🔬 Metode analisis singkat

| Pertanyaan | Metode |
|------------|--------|
| Kecepatan dan arah penyesuaian | Model koreksi kesalahan (*error correction model*), half-life, koefisien α_B dan α_K |
| Banyak uji sekaligus | Koreksi Holm pada keluarga uji utama (18 uji), bootstrap untuk selang kepercayaan 90% |
| Daya uji | Analisis daya dan efek minimum yang terdeteksi untuk uji asimetri |
| Risiko lonjakan ekstrem | Teori nilai ekstrem (*peaks over threshold*), level kembali 250 interval, laju klaster ≥20% |
| Keserentakan ekstrem | Ukuran ketergantungan ekstrem χ pada kuantil 0,90–0,95, dengan uji placebo lintas komoditas |
| Pola hari raya | Studi peristiwa (*event study*) dengan uji tanda-balik (*sign-flip*) dan koreksi Holm |
| Premi Kota | Uji markup nominal vs proporsional (AIC), regresi kointegrasi DOLS, rezim rata-rata selisih |

**Tingkat bukti** adalah konsistensi temuan pada variasi keputusan pemodelan dan koreksi uji ganda. Ia **bukan** probabilitas kebenaran dan bukan bukti kausal.

---

## ⚠️ Keterbatasan

- Hasil adalah **asosiasi statistik**, bukan kausalitas.
- **Bentuk ekor** distribusi lonjakan (berat atau terbatas) tidak dapat dibedakan; yang dilaporkan hanya besar dan frekuensi lonjakan.
- Uji **asimetri** berdaya rendah; hasil tidak signifikan bukan bukti simetri.
- Pola **hari raya** hanya bersandar pada 7 peristiwa per hari raya dan tiga cabai bergerak bersama, jadi bukan tiga bukti yang terpisah.
- **Tanggal patahan rezim** adalah estimasi statistik dan tidak boleh dikaitkan dengan peristiwa tertentu.
- Angka bergantung pada spesifikasi (log vs rupiah, rata-rata global vs per rezim), karena itu dilaporkan sebagai **rentang**.
- Dasar kebijakan resmi perubahan perlakuan hari libur PIHPS sejak 2023 belum ditemukan.

Daftar lengkapnya ada di tab **Bukti & batasan** pada dashboard.

---

## 🛠️ Pemecahan masalah

| Masalah | Penyebab dan solusi |
|---------|---------------------|
| `Berkas … belum ditemukan di folder data` padahal berkas ada | Daftar berkas lama masih tersimpan. Klik **🔄 Muat ulang data**, atau hentikan (`Ctrl+C`) lalu jalankan ulang. Pastikan perintah dijalankan dari folder paling luar |
| Dashboard berhenti dengan pesan data tidak ditemukan | `data_harga_eda5.csv` dan `data_perubahan_bersama_eda5.csv` wajib ada di dalam folder `data/` |
| `ModuleNotFoundError` | Jalankan `pip install -r requirements.txt` pada lingkungan yang sedang aktif |
| Tampilan lama tidak berubah | Tekan `C` di halaman dashboard lalu pilih *Clear cache*, atau segarkan browser |
| Gagal saat deploy ke Streamlit Cloud | Periksa `requirements.txt` (jangan berisi hasil `pip freeze` seluruh lingkungan) dan **Main file path** `dashboard/app.py` |

---

## 🔄 Memperbarui atau menambah data

1. Jalankan ulang tahap analisis di notebook sehingga berkas keluaran terbaru terbentuk.
2. Salin berkas keluaran ke folder `data/` (timpa berkas lama dengan nama yang sama).
3. Jangan mengubah nama berkas, karena dashboard mencarinya berdasarkan nama.
4. Jalankan dashboard dan klik **🔄 Muat ulang data**.
5. Buka tab **Data & unduhan** dan pastikan seluruh pemeriksaan integritas berstatus ✅.
6. *Commit* dan *push* perubahan ke GitHub.

---

## 📄 Lisensi dan kontak

- **Lisensi:** tentukan sendiri (misalnya MIT untuk kode). Tambahkan berkas `LICENSE` bila diperlukan. Data tetap tunduk pada ketentuan sumber aslinya.
- **Pembuat:** [@liwauddin928-arch](https://github.com/liwauddin928-arch)
- **Saran dan masalah:** gunakan tab **Issues** pada repositori ini.

**Cara mengutip (contoh):**
> Liwauddin. (2026). *Analisis Komoditas Pangan Kota Cirebon dan Kabupaten Cirebon: Keterkaitan Harga dan Risiko Lonjakan Ekstrem* [Dashboard dan arsip analisis]. GitHub.
