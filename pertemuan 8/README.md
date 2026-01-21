 Praktikum Transformasi 3D - Mini Project Grafika Komputer

🎯 Deskripsi Proyek

Mini project ini merupakan implementasi sistem transformasi geometri 3D interaktif yang menampilkan objek-objek 3D hasil transformasi geometris secara kreatif dan edukatif. Program ini menerapkan **keempat jenis transformasi 3D** (translasi, rotasi, skala, dan refleksi) dengan visualisasi real-time dan kontrol interaktif.

 🎮 Fitur Utama

 **1. Objek 3D yang Tersedia:**
- **KUBUS** - 8 vertices, 6 permukaan persegi dengan warna berbeda
- **PIRAMIDA** - 5 vertices, 5 permukaan segitiga
- **PRISMA** - 6 vertices, 5 permukaan (2 segitiga, 3 persegi panjang)

 **2. Transformasi 3D yang Diimplementasikan:**
✅ **TRANSLASI 3D** - Menggeser objek dalam ruang 3D  
✅ **ROTASI 3D** - Memutar objek terhadap sumbu X, Y, Z  
✅ **SKALA 3D** - Mengubah ukuran objek secara proporsional  
✅ **REFLESI 3D** - Mencerminkan objek terhadap bidang koordinat  

 **3. Fitur Interaktif:**
- Kontrol keyboard real-time untuk semua transformasi
- Animasi otomatis demonstrasi transformasi
- Toggle wireframe dan permukaan berwarna
- Sistem koordinat 3D visual
- Panel informasi dengan rumus matematika
- Multiple camera control

 📚 Teori Transformasi 3D

 **A. TRANSLASI 3D**
Menggeser objek sejauh vektor T = (tx, ty, tz)

**Rumus Matematika:**  
```
P' = P + T
(x', y', z') = (x + tx, y + ty, z + tz)
```

**Matriks Homogen (4×4):**
```
[ 1  0  0  tx ]
[ 0  1  0  ty ]
[ 0  0  1  tz ]
[ 0  0  0  1  ]
```

 **B. ROTASI 3D**
Memutar objek sebesar sudut θ terhadap sumbu koordinat

 **Rotasi terhadap sumbu X:**
```
Rx(θ) = [[1,     0,      0, 0],
         [0,  cosθ,  -sinθ, 0],
         [0,  sinθ,   cosθ, 0],
         [0,     0,      0, 1]]
```

 **Rotasi terhadap sumbu Y:**
```
Ry(θ) = [[ cosθ,  0,  sinθ, 0],
         [    0,  1,     0, 0],
         [-sinθ,  0,  cosθ, 0],
         [    0,  0,     0, 1]]
```

 **Rotasi terhadap sumbu Z:**
```
Rz(θ) = [[cosθ, -sinθ,  0, 0],
         [sinθ,  cosθ,  0, 0],
         [   0,     0,  1, 0],
         [   0,     0,  0, 1]]
```

 **C. SKALA 3D**
Mengubah ukuran objek dengan faktor S = (sx, sy, sz)

**Rumus Matematika:**  
```
P' = S × P
(x', y', z') = (sx·x, sy·y, sz·z)
```

**Matriks Homogen:**
```
[ sx  0   0  0 ]
[ 0  sy   0  0 ]
[ 0   0  sz  0 ]
[ 0   0   0  1 ]
```

 **D. REFLEKSI 3D**
Mencerminkan objek terhadap bidang koordinat

 **Refleksi terhadap bidang YZ (sumbu X):**
```
Mx = [[-1, 0, 0, 0],
      [ 0, 1, 0, 0],
      [ 0, 0, 1, 0],
      [ 0, 0, 0, 1]]
```

 **Refleksi terhadap bidang XZ (sumbu Y):**
```
My = [[1,  0, 0, 0],
      [0, -1, 0, 0],
      [0,  0, 1, 0],
      [0,  0, 0, 1]]
```

 **Refleksi terhadap bidang XY (sumbu Z):**
```
Mz = [[1, 0,  0, 0],
      [0, 1,  0, 0],
      [0, 0, -1, 0],
      [0, 0,  0, 1]]
```

 🛠️ Teknologi yang Digunakan

 **Dependencies:**
```python
 Library utama
pip install pygame numpy

 Versi yang digunakan
- Python 3.10+
- PyGame 2.6.1
- NumPy 1.24+
```

 **Struktur Kode:**
```
Transformasi3D/
├── __init__()                      Inisialisasi sistem
├── project_3d_to_2d()             Proyeksi perspektif
├── apply_rotation()               Matriks rotasi 3D
├── apply_transformation()         Transformasi gabungan
├── draw_object()                  Rendering objek 3D
├── draw_axes()                    Sistem koordinat
├── draw_control_panel()           UI informasi
├── handle_input()                 Input keyboard
├── update_animation()             Animasi otomatis
└── run()                          Main loop
```

 🚀 Instalasi dan Menjalankan

 **1. Prerequisites:**
- Python 3.10 atau lebih baru
- pip package manager

 **2. Instalasi Dependencies:**
```bash
 Install PyGame dan NumPy
pip install pygame numpy
```

 **3. Menjalankan Program:**
```bash
 Clone atau download kode
git clone <repository-url>
cd praktikum-transformasi-3d

 Jalankan program
python transformasi_3d.py
```

 **4. Alternatif untuk IDE:**
- Buka file `transformasi_3d.py` di IDE Python favorit
- Pastikan PyGame dan NumPy sudah terinstall
- Run program dari menu Run/Execute

 🎮 Panduan Kontrol

 **Pemilihan Objek:**
| Tombol | Objek | Deskripsi |
|--------|-------|-----------|
| **1** | Kubus | Objek kubus 3D dengan 8 vertices |
| **2** | Piramida | Limas segitiga dengan 5 vertices |
| **3** | Prisma | Prisma segitiga dengan 6 vertices |

 **Mode Transformasi:**
| Tombol | Mode | Fungsi |
|--------|------|---------|
| **T** | Translasi | Mode pergeseran objek |
| **R** | Rotasi | Mode rotasi objek |
| **S** | Skala | Mode perubahan ukuran |
| **F** | Refleksi | Mode pencerminan objek |

 **Kontrol Transformasi:**
| Tombol | Sumbu X | Sumbu Y | Sumbu Z |
|--------|---------|---------|---------|
| **Q** | X - | Y - | Z - |
| **W** | X + | Y + | Z + |
| **A** | X - | Y - | Z - |
| **S** | X + | Y + | Z + |
| **Z** | X - | Y - | Z - |
| **C** | X + | Y + | Z + |

*Kontrol spesifik tergantung mode transformasi yang aktif*

 **Kontrol Kamera dan Tampilan:**
| Tombol | Fungsi |
|--------|---------|
| **← → ↑ ↓** | Rotasi Kamera |
| **SPACE** | Reset semua transformasi |
| **V** | Toggle Wireframe (on/off) |
| **B** | Toggle Faces (permukaan warna) |
| **N** | Toggle Sumbu Koordinat |
| **ESC** | Keluar dari program |

 📊 Output Program

 **1. Visual 3D:**
- **Window utama** dengan objek 3D interaktif
- **Sumbu koordinat** X (merah), Y (hijau), Z (biru)
- **Objek 3D** dengan wireframe dan permukaan berwarna
- **Animasi real-time** transformasi

 **2. Panel Informasi:**
```
Kiri Atas:
- Judul program dan institusi
- Objek aktif dan mode transformasi
- Parameter transformasi terkini

Kanan Atas:
- Panduan kontrol lengkap
- Tombol dan fungsinya

Bawah:
- Rumus matematika transformasi
- Penjelasan konsep teoritis
```

 **3. Console Output:**
```
======================================================================
PRAKTIKUM TRANSFORMASI 3D - GRAFIKA KOMPUTER
Program Studi Ilmu Komputer
Universitas Nahdlatul Ulama Blitar
======================================================================

Mini Project: Sistem Transformasi 3D Interaktif
Menerapkan 4 transformasi: Translasi, Rotasi, Skala, Refleksi

Kontrol:
1-3: Ganti objek (Kubus/Piramida/Prisma)
T/R/S/F: Mode transformasi
Q/W, A/S, Z/X: Kontrol transformasi
Panah: Rotasi Kamera
SPACE: Reset  V: Wireframe  B: Faces  N: Sumbu
ESC: Keluar
----------------------------------------------------------------------
```

 🔬 Implementasi Teknis

 **1. Proyeksi 3D ke 2D:**
Menggunakan **proyeksi perspektif** dengan handling pembagian nol:
```python
def project_3d_to_2d(self, point):
     ... transformasi kamera ...
    
     Proyeksi perspektif dengan safety check
    z_adjusted = z + self.focal_length
    
    if abs(z_adjusted) < 10:    Avoid division by zero
        factor = 1.0    Fallback to parallel projection
    else:
        factor = self.focal_length / z_adjusted
```

 **2. Backface Culling:**
Optimasi rendering dengan hanya menggambar permukaan yang menghadap kamera:
```python
 Hitung normal permukaan
normal = np.cross(v1, v2)

 Vektor dari permukaan ke kamera
view_vector = camera_pos - point_on_face

 Hanya gambar jika normal menghadap kamera (dot product > 0)
if np.dot(normal, view_vector) > 0:
    draw_face()
```

 **3. Urutan Transformasi:**
Transformasi diterapkan dalam urutan:
```
1. Scaling
2. Reflection
3. Rotation
4. Translation
```

**Matriks gabungan:**  
`T_total = T_translation × T_rotation × T_reflection × T_scaling`

 🎯 Pemenuhan Kriteria Mini Project

| Kriteria | Status | Implementasi |
|----------|--------|--------------|
| **Minimal 3 dari 4 transformasi** | ✅ **TERPENUH!** | **KEEMPAT** transformasi diimplementasikan |
| **Translasi 3D** | ✅ | Kontrol pergeseran di 3 sumbu |
| **Rotasi 3D** | ✅ | Rotasi terhadap X, Y, Z independen |
| **Skala 3D** | ✅ | Scaling proporsional dan non-proporsional |
| **Refleksi 3D** | ✅ | Refleksi terhadap 3 bidang koordinat |
| **Kreatif** | ✅ | 3 objek berbeda + animasi + interaksi |
| **Edukatif** | ✅ | Panel info + rumus + visualisasi real-time |

 📈 Pembelajaran yang Didapat

 **1. Konsep Matematika:**
- Matriks transformasi homogen 4×4
- Trigonometri untuk rotasi 3D
- Sistem koordinat kartesian 3D
- Proyeksi perspektif vs. paralel

 **2. Pemrograman Grafika:**
- Representasi objek 3D dengan vertices dan faces
- Rendering pipeline sederhana
- Optimasi dengan backface culling
- Interaksi user dengan objek 3D

 **3. Implementasi Praktis:**
- Handling edge cases (division by zero)
- State management untuk transformasi
- UI/UX untuk aplikasi edukatif
- Animasi dan feedback visual

   🧪 Testing dan Validasi

    **Test Case 1: Translasi**
```python
Input: Tombol T (mode translasi) → Q/W (gerak sumbu X)
Expected: Objek bergerak horizontal
Result: ✅ Berhasil
```

    **Test Case 2: Rotasi Kompleks**
```python
Input: Mode rotasi → rotasi X 90° → rotasi Y 45°
Expected: Objek berorientasi diagonal
Result: ✅ Berhasil
```

    **Test Case 3: Transformasi Bertingkat**
```python
Input: Scaling 2x → Translation → Reflection
Expected: Transformasi komposit terlihat natural
Result: ✅ Berhasil
```

    **Test Case 4: Boundary Conditions**
```python
Input: Scaling 0.1x (minimum) → kamera sangat dekat
Expected: Tidak crash, proyeksi fallback ke paralel
Result: ✅ Berhasil dengan exception handling
```

