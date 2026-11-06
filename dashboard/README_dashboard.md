# Dashboard Harga Cabai Cirebon (Streamlit)

## Menjalankan
```bash
pip install -r requirements.txt
streamlit run app.py
```
Buka alamat yang ditampilkan (biasanya http://localhost:8501).

## Data
Folder `data/` sudah berisi berkas minimum yang dibaca dashboard. Untuk memakai hasil terbaru Anda:
- Salin keluaran analisis (`eda_tahap5` … `eda_tahap16`) ke dalam `data/` (sub-folder bebas; aplikasi mencari berkas berdasarkan **nama**),
  atau ubah **Folder data** di sisi kiri lalu klik **Muat ulang data**. Variabel lingkungan `DATA_ROOT` juga bisa dipakai.
- Berkas wajib: `data_harga_eda5.csv` dan `data_perubahan_bersama_eda5.csv` (Tahap 5). Halaman lain menampilkan pesan bila berkas hasilnya belum ada.

## Halaman
Beranda · Harga & selisih · Perubahan harga · Penyesuaian antardaerah (termasuk simulasi) · Risiko ekstrem (termasuk kalkulator frekuensi) ·
Hari raya · Premi & rezim · Klaim & bukti · Kualitas data.

## Catatan
Seluruh hasil adalah keterkaitan statistik, bukan kausalitas. Angka diambil dari keluaran Tahap 5–16; tingkat bukti tiap klaim ada di halaman **Klaim & bukti**.
