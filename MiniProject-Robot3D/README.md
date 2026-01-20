 🤖 Mini Project Grafika Komputer 3D  
 Simulasi Robot 3D Interaktif dengan Transformasi Geometris

 📌 Deskripsi Proyek
Proyek ini merupakan simulasi Robot 3D interaktif menggunakan Python dan OpenGL (PyOpenGL + GLUT).  
Robot dibangun menggunakan Hierarchical Transformation dengan pendekatan glPushMatrix() dan glPopMatrix() sehingga setiap bagian tubuh bergerak secara terstruktur dan realistis.

Robot ditempatkan pada lingkungan 3D berupa jalan, tanah, air animatif, langit, serta elemen lingkungan tambahan seperti tiang lampu.


 🎯 Tujuan
- Menerapkan transformasi 3D (Translasi, Rotasi, Skala, Refleksi)
- Mengimplementasikan Hierarchical Transformation
- Membuat objek 3D interaktif
- Menampilkan animasi dan pencahayaan OpenGL


 🧩 Fitur Utama
- Robot 3D berbasis primitive OpenGL
- Animasi lengan dan kaki
- Kontrol pergerakan menggunakan keyboard
- Kamera dinamis
- Lingkungan 3D (jalan, tanah, air, langit)
- Efek refleksi
- Lighting dan material


 🛠️ Teknologi
- Python 3
- PyOpenGL
- GLUT


 📂 Struktur File

MiniProject-Robot3D
 ├── robot_uas.py
 └── README.md



 ▶️ Cara Menjalankan
1. Install library:
```bash
pip install PyOpenGL PyOpenGL_accelerate
```

2. Jalankan program:
```bash
python robot_uas.py
```

---

 🎮 Kontrol Keyboard
| Tombol | Fungsi |
|------|------|
| W | Maju |
| S | Mundur |
| A | Kiri |
| D | Kanan |
| J | Rotasi kiri |
| L | Rotasi kanan |
| + | Perbesar |
| - | Perkecil |
| Spasi | Animasi ON/OFF |
| Z | Kamera kiri |
| X | Kamera kanan |
| R | Reset |
| ESC | Keluar |

---

 🧠 Hierarchical Transformation
Robot menggunakan struktur hierarki:
Robot → Body → Head, Arms, Legs

Setiap bagian memiliki transformasi relatif terhadap parent object.

---

 👤 Author
Nama  : Choirul Ardhi Saputra  
Mata Kuliah : Grafika Komputer  
Tahun : 2026
