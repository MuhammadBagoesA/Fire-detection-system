# Fire & Smoke Detection

**Fire & Smoke Detection** adalah aplikasi web sederhana berbasis **YOLOv26** untuk mendeteksi keberadaan **api dan asap** pada gambar maupun video.

**Demo Web:**  
*soon*

---

## Fitur Utama

### Upload Media (Gambar atau Video)
Pengguna dapat mengunggah file gambar atau video untuk dianalisis oleh model.

### Contoh Media (Sample Image & Video)
Tersedia contoh gambar dan video yang dapat digunakan langsung tanpa perlu mengunggah file.

### Deteksi Otomatis dengan YOLOv8
Model mendeteksi dua kelas objek:
- Fire
- Smoke

### Visualisasi Hasil Deteksi
Hasil deteksi ditampilkan dengan **bounding box** pada objek yang terdeteksi.

### Alert System
Sistem memberikan peringatan otomatis:
- Fire Detected
- Smoke Detected
- Fire and Smoke Detected

### Pengaturan Confidence Threshold
Slider untuk mengatur sensitivitas deteksi (default **0.1**).

---

## Teknologi yang Digunakan

- **Python 3**
- **Streamlit** – Antarmuka web interaktif
- **Ultralytics YOLOv26** – Deteksi objek
- **OpenCV** – Pemrosesan video dan gambar
- **NumPy** – Operasi array
- **Pillow (PIL)** – Pemrosesan gambar

---

## Manfaat

- Membantu **deteksi dini kebakaran** pada gambar maupun video
- Dapat digunakan sebagai dasar sistem **monitoring keamanan berbasis AI**
- Dapat dikembangkan lebih lanjut untuk:
  - deteksi **real-time webcam / CCTV**
  - sistem **alarm otomatis**
  - integrasi dengan **sistem monitoring keamanan**