SISTEM TATA SURYA 2D - GRAFIKA KOMPUTER

Aplikasi simulasi tata surya 2D sederhana yang diimplementasikan menggunakan Python dan library Pygame. Proyek ini berfokus pada penggunaan algoritma grafika komputer manual untuk menggambar dan mentransformasi objek, sesuai dengan materi Grafika Komputer.

🌟 Konsep Grafika yang Digunakan

Proyek ini wajib memanfaatkan minimal 4 materi Grafika Komputer, dan berikut adalah implementasinya:

1.  Algoritma Gambar Lingkaran (Midpoint Circle): 
    Implementasi: Digunakan dalam fungsi `draw_circle_midpoint` di `algorithms.py` untuk menggambar Matahari, planet, bulan, dan komet. Algoritma ini memastikan penggambaran lingkaran yang efisien berbasis piksel.

2.  Algoritma Gambar Poligon/Garis:
    Implementasi: Digunakan untuk:
         Menggambar orbit elips (`draw_ellipse_orbit` di `algorithms.py`) dengan menghasilkan titik-titik dan menghubungkannya menggunakan aproksimasi garis.
         Menggambar elemen-elemen UI (panel, garis, dll.) di `ui.py`.

3.  Transformasi Geometris 2D - Translasi (Translation): 
    Implementasi:
         Fungsi pergeseran kamera (W, A, S, D) di `main.py` yang memindahkan pusat koordinat pandangan (`camera_x`, `camera_y`).
         Fungsi `Transform2D.translate` di `transformations.py` memastikan posisi semua objek langit (planet, asteroid) dirender dengan benar relatif terhadap posisi kamera.

4.  Transformasi Geometris 2D - Skala (Scaling): 
    Implementasi:
         Fungsi Zoom In dan Zoom Out (Scroll/Tombol +/-) di `solar_system.py` yang memodifikasi variabel `zoom`.
         Variabel `zoom` ini berfungsi sebagai faktor skala yang mengubah jarak dan ukuran radius semua benda langit sebelum dirender, memberikan efek pembesaran/pengecilan seluruh sistem.

⚙️ Algoritma Grafika yang Dipakai (Kode Manual)

Semua algoritma ini diimplementasikan secara manual, bukan menggunakan fungsi drawing bawaan Pygame untuk objek utama.

Midpoint Circle Algorithm: Menggunakan pendekatan titik tengah untuk menggambar lingkaran, dengan tambahan aproksimasi anti-aliasing untuk hasil visual yang lebih halus pada resolusi tinggi. (Lihat `algorithms.py`)
Perhitungan Orbit (Translasi dan Rotasi): Posisi planet dihitung menggunakan persamaan orbit elips/lingkaran (Rotasi) dan kemudian diterapkan Translasi relatif terhadap kamera dan Skala (zoom).

 ▶️ Cara Menjalankan Program

Persyaratan
Python: Versi 3.x
Pygame: Library Pygame harus terinstal.

Cara menjalankannya buka file main.py klik jalankan pada text editor.
