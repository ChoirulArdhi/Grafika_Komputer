 JUDUL PROYEK
 🤖 Simulasi Robot 3D Interaktif Menggunakan OpenGL

 KONSEP GRAFIKA KOMPUTER YANG DIGUNAKAN

 1. Representasi Objek 3D
Objek robot 3D dibangun menggunakan **primitive OpenGL** berupa kubus (cube) yang tersusun dari **vertex, edge, dan polygon**.  
Setiap bagian tubuh robot (kepala, badan, lengan, dan kaki) direpresentasikan sebagai objek 3D terpisah, kemudian disusun menjadi satu kesatuan model robot.

Pendekatan ini menunjukkan pemahaman terhadap:
- Struktur dasar objek 3D
- Penyusunan objek kompleks dari bentuk sederhana


2. Transformasi Geometris 3D
Proyek ini mengimplementasikan beberapa transformasi 3D, yaitu:

- **Translasi**  
  Digunakan untuk memindahkan robot di sepanjang sumbu X dan Z menggunakan input keyboard (W, A, S, D).

- **Rotasi**  
  Digunakan untuk:
  - Mengatur arah hadap robot sesuai arah pergerakan
  - Menganimasikan lengan dan kaki saat berjalan

- **Skala**  
  Digunakan untuk memperbesar dan memperkecil ukuran robot secara keseluruhan.

- **Refleksi**  
  Diimplementasikan dengan membalik sumbu Y untuk menampilkan refleksi robot pada permukaan.

3. Hierarchical Transformation
Robot dibangun menggunakan konsep **Hierarchical Transformation**, di mana setiap bagian tubuh memiliki hubungan parent–child:

- Body sebagai root object
- Head, arms, dan legs sebagai child object

Dengan pendekatan ini:
- Rotasi lengan terjadi pada titik bahu
- Rotasi kaki terjadi pada titik pinggul
- Transformasi child mengikuti transformasi parent

Konsep ini diimplementasikan menggunakan `glPushMatrix()` dan `glPopMatrix()`.

4. Viewing dan Proyeksi 3D
Sistem kamera menggunakan:
- **Proyeksi perspektif** dengan `gluPerspective()`
- **Kamera dinamis** dengan `gluLookAt()`

Kamera dapat diputar menggunakan keyboard sehingga pengguna dapat melihat objek dari berbagai sudut pandang, memperkuat pemahaman konsep ruang 3D.

5. Warna, Pencahayaan, dan Ilusi Kedalaman
Untuk membentuk ilusi kedalaman ruang 3D, proyek ini menggunakan:
- Pewarnaan objek berbeda untuk setiap bagian robot
- Lighting (ambient dan diffuse light)
- Overlapping objek
- Perbedaan ukuran dan posisi objek terhadap kamera
- Efek refleksi

DESKRIPSI PROYEK
Aplikasi ini merupakan simulasi robot 3D interaktif yang bergerak di dalam sebuah mini scene 3D berupa jalan raya, tanah, air animatif, dan langit.  
Robot dapat dikendalikan menggunakan keyboard untuk bergerak, berputar, serta menampilkan animasi berjalan.

Setiap bagian robot disusun menggunakan konsep hierarchical modeling sehingga gerakan robot terlihat lebih realistis dan terstruktur.  
Lingkungan 3D dan kamera perspektif memberikan kesan ruang dan kedalaman, sesuai dengan konsep dasar grafika komputer 3D.

Proyek ini termasuk dalam kategori **Mini Scene / Simulasi 3D**.

CARA MENJALANKAN PROGRAM

 1. Install Library
```bash
pip install PyOpenGL PyOpenGL_accelerate
````

2. Jalankan Program

```bash
python robot_uas.py
```

STRUKTUR FILE

```
MiniProject-GrafikaKomputer3D
 ├── robot_uas.py
 └── README.md
```

 IDENTITAS MAHASISWA

* **Nama** : Choirul Ardhi Saputra
* **NIM** : 2355201033
* **Program Studi** : Ilmu Komputer
* **Universitas** : Universitas Nahdlatul Ulama Blitar
