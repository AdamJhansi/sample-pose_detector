# Pose Detector and Exercise Counter

Aplikasi Python yang menggunakan MediaPipe untuk mendeteksi pose dan menghitung gerakan olahraga (push-up dan squat) secara real-time menggunakan webcam.

## Fitur

- Deteksi pose real-time menggunakan webcam
- Penghitungan push-up dan squat secara otomatis
- Pengecekan form gerakan yang akurat
- Tampilan sudut gerakan
- Informasi FPS
- Tombol reset dan close

## Persyaratan Sistem

- Python 3.7 atau lebih baru
- Webcam
- Sistem operasi: Windows/Linux/MacOS

## Instalasi

1. Clone repository ini:
```bash
git clone https://github.com/username/pose_detector.git
cd pose_detector
```

2. Buat dan aktifkan virtual environment (opsional tapi direkomendasikan):
```bash
# Windows
python -m venv venv
venv\Scripts\activate
```

3. Instal dependensi yang diperlukan:
```bash
pip install -r requirements.txt
```

## Penggunaan

1. Jalankan aplikasi:
```bash
python main.py
```

2. Posisikan diri Anda di depan webcam:
   - Untuk push-up: pastikan seluruh tubuh terlihat dalam frame
   - Untuk squat: pastikan tubuh bagian bawah terlihat dalam frame

3. Kontrol:
   - Tekan 'R' untuk mereset penghitungan
   - Tekan 'Q' atau klik tombol close untuk keluar

## Penjelasan File

- `main.py`: File utama yang menjalankan aplikasi
- `pose_detector.py`: Kelas untuk mendeteksi pose menggunakan MediaPipe
- `exercise_detector.py`: Kelas untuk mendeteksi dan menghitung gerakan olahraga
- `utils.py`: Fungsi-fungsi utilitas untuk perhitungan sudut dan tampilan

## Tips Penggunaan

1. Pastikan pencahayaan ruangan cukup
2. Kenakan pakaian yang kontras dengan latar belakang
3. Jaga jarak yang tepat dari kamera (1-2 meter)
4. Lakukan gerakan dengan form yang benar:
   - Push-up: tubuh lurus, siku ditekuk hingga 90 derajat
   - Squat: punggung lurus, lutut ditekuk hingga 90 derajat

## Troubleshooting

1. Jika kamera tidak terdeteksi:
   - Pastikan webcam terhubung dengan benar
   - Periksa izin akses kamera
   - Coba ganti indeks kamera di `main.py` (baris `cap = cv2.VideoCapture(0)`)

2. Jika deteksi tidak akurat:
   - Sesuaikan threshold di `exercise_detector.py`
   - Pastikan pencahayaan cukup
   - Periksa form gerakan

## Kontribusi

Silakan buat pull request untuk kontribusi. Untuk perubahan besar, buka issue terlebih dahulu untuk mendiskusikan perubahan yang diinginkan.

## Lisensi

[MIT License](LICENSE) 