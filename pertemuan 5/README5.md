Praktikum Grafika Komputer

Pertemuan 5

 **Tugas Praktikum: Menggambar Garis, Lingkaran, dan Poligon**

📋 Deskripsi Proyek

Proyek ini merupakan implementasi algoritma-algoritma dasar dalam grafika komputer untuk menggambar primitif grafis seperti garis, lingkaran, dan poligon. Implementasi dilakukan menggunakan Python dengan library Turtle, tanpa menggunakan library grafis lainnya.

🎯 Tujuan Praktikum

1. Memahami dan mengimplementasikan algoritma DDA untuk menggambar garis
2. Memahami dan mengimplementasikan algoritma Midpoint Circle untuk menggambar lingkaran
3. Menggunakan algoritma garis yang sudah dibuat untuk menggambar poligon
4. Menganalisis proses dan hasil dari setiap algoritma

🛠️ Teknologi yang Digunakan

- **Bahasa Pemrograman:** Python 3.x
- **Library:** Turtle Graphics (standar Python)
- **Platform:** Cross-platform (Windows, macOS, Linux)

📁 Struktur Kode

Kelas Utama: `GraphicsPrimitives`

Kelas ini mengandung semua metode untuk menggambar primitif grafis:

 1. **Metode Konstruktor**
   - Inisialisasi layar Turtle
   - Setup ukuran window dan background
   - Konfigurasi warna untuk setiap primitif

 2. **`draw_pixel(x, y, color)`**
   - Menggambar satu pixel pada koordinat (x, y)
   - Menggunakan warna yang ditentukan

 3. **`draw_line_dda(x1, y1, x2, y2, color)`**
   - **Algoritma:** Digital Differential Analyzer (DDA)
   - **Input:** Koordinat titik awal (x1, y1) dan titik akhir (x2, y2)
   - **Output:** Garis lurus yang menghubungkan kedua titik

 4. **`draw_circle_midpoint(xc, yc, r, color)`**
   - **Algoritma:** Midpoint Circle Algorithm
   - **Input:** Pusat lingkaran (xc, yc) dan radius (r)
   - **Output:** Lingkaran dengan radius r

 5. **`draw_polygon(vertices, color)`**
   - **Algoritma:** Menggunakan DDA untuk setiap sisi
   - **Input:** Daftar titik sudut (vertices)
   - **Output:** Poligon tertutup

 6. **`draw_grid()`**
   - Menggambar sistem koordinat kartesian
   - Menampilkan grid untuk referensi visual

 7. **`draw_all_primitives()`**
   - Menampilkan semua contoh implementasi
   - Demonstrasi penggunaan semua algoritma

 🔧 Algoritma yang Diimplementasikan

 1. **Algoritma DDA (Digital Differential Analyzer) untuk Garis**

**Prinsip Kerja:**
```
1. Hitung selisih: dx = x2 - x1, dy = y2 - y1
2. Tentukan steps = max(|dx|, |dy|)
3. Hitung increment: x_inc = dx/steps, y_inc = dy/steps
4. Gambar pixel di setiap step dengan membulatkan koordinat
```

**Kelebihan:**
- Implementasi sederhana
- Cocok untuk garis dengan kemiringan rendah
- Tidak memerlukan operasi perkalian

**Kekurangan:**
- Membutuhkan pembulatan
- Performa kurang optimal untuk kemiringan curam
- Menggunakan floating point arithmetic

2. **Algoritma Midpoint Circle untuk Lingkaran**

**Prinsip Kerja:**
```
1. Mulai dari titik (0, r)
2. Hitung parameter keputusan: d = 1 - r
3. Untuk setiap x dari 0 ke r/√2:
   - Jika d < 0: pilih pixel E, d baru = d + 2x + 1
   - Jika d ≥ 0: pilih pixel SE, d baru = d + 2(x - y) + 1
   - Gambar 8 titik simetris
```

**Kelebihan:**
- Hanya menggunakan operasi integer
- Efisien (hanya menggambar 1/8 lingkaran)
- Tidak memerlukan fungsi trigonometri

3. **Pembuatan Poligon**

**Prinsip Kerja:**
```
1. Hubungkan setiap titik sudut berurutan dengan DDA
2. Hubungkan titik terakhir ke titik pertama
3. Tandai titik-titik sudut untuk kejelasan
```

🚀 Cara Menjalankan Program

Prasyarat
- Python 3.x terinstal
- Library Turtle (sudah termasuk dalam instalasi standar Python)

Langkah-langkah
1. Clone atau download kode program
2. Buka terminal/command prompt
3. Navigasi ke direktori program
4. Jalankan perintah:
   ```bash
   python praktikum_grafika.py
   ```

Alternatif untuk IDE
1. Buka file `praktikum_grafika.py` di IDE Python favorit (Thonny, VS Code, PyCharm, dll.)
2. Run program dari IDE

 📊 Output Program

Program akan menampilkan window dengan konten berikut:

 1. **Sistem Koordinat**
   - Grid 50x50 pixel
   - Sumbu X dan Y
   - Label koordinat

 2. **Contoh Garis (DDA)**
   - Garis horizontal
   - Garis vertikal
   - Garis miring

 3. **Contoh Lingkaran (Midpoint)**
   - Lingkaran dengan radius 50
   - Lingkaran dengan radius 30

 4. **Contoh Poligon**
   - Segitiga
   - Segi lima (pentagon)
   - Segi enam (hexagon)

 5. **Bentuk Kompleks (Rumah)**
   - Kombinasi persegi (dinding)
   - Segitiga (atap)
   - Persegi panjang (pintu)
   - Lingkaran (jendela)

 📝 Analisis Hasil

 1. **Kualitas Garis (DDA)**
   - Garis tampak kontinu dan halus
   - Akurasi baik untuk kemiringan rendah
   - Terlihat pixelated pada kemiringan tinggi

 2. **Kualitas Lingkaran (Midpoint)**
   - Lingkaran simetris sempurna
   - Tidak ada distorsi bentuk
   - Efisiensi tinggi dalam komputasi

 3. **Kualitas Poligon**
   - Sudut-sudut tajam dan jelas
   - Sisi-sisi lurus dan terhubung dengan baik
   - Dapat menggambar poligon beraturan dan tidak beraturan

 🧪 Testing dan Validasi

 Test Case 1: Garis Lurus
```python
 Garis horizontal
draw_line_dda(-300, 200, -150, 200)
 Garis vertikal  
draw_line_dda(-250, 100, -250, 200)
 Garis miring
draw_line_dda(-300, 150, -150, 250)
```

 Test Case 2: Lingkaran
```python
 Lingkaran besar
draw_circle_midpoint(0, 175, 50)
 Lingkaran kecil
draw_circle_midpoint(0, 100, 30)
```

 Test Case 3: Poligon Beraturan
```python
 Segitiga
triangle = [(200, 200), (300, 200), (250, 150)]
 Segi lima (pentagon)
 Segi enam (hexagon)
```

 📈 Performa dan Optimasi

 Kompleksitas Waktu
- **DDA:** O(max(|dx|, |dy|))
- **Midpoint Circle:** O(r/√2)
- **Poligon n-sisi:** O(n × sisi_terpanjang)

 Optimasi yang Diterapkan
1. **Simetri 8-arah** pada lingkaran
2. **Integer arithmetic** pada Midpoint Circle
3. **Reuse algoritma** DDA untuk poligon
