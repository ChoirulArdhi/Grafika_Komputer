 Praktikum Transformasi 2D - Game Platformer

 🎮 Deskripsi Proyek

Proyek ini adalah implementasi sistem transformasi geometri 2D dalam konteks pengembangan game platformer. Implementasi mencakup empat transformasi dasar: **translasi**, **rotasi**, **scaling**, dan **refleksi**, yang diterapkan pada karakter pemain dalam skenario game interaktif.

 🎯 Tujuan Praktikum

1. Memahami dan mengimplementasikan empat transformasi geometri 2D dasar
2. Menerapkan transformasi dalam konteks game development yang interaktif
3. Menganalisis efek urutan transformasi pada objek grafis
4. Memvisualisasikan transformasi secara real-time dengan feedback matematis

 📚 Transformasi yang Diimplementasikan

 1. **TRANSLASI (Dash Movement)**
**Scenario:** Karakter bergerak cepat saat menekan tombol "Dash"
```
Rumus: (x', y') = (x + dx, y + dy)
Implementasi: dx = 20, dy = 0
```

 2. **ROTASI (Hand Rotation)**
**Scenario:** Animasi memutar tangan saat memukul musuh
```
Rumus: x' = x·cosθ - y·sinθ
        y' = x·sinθ + y·cosθ
Implementasi: θ = 30° per rotasi
```

 3. **SCALING (Power Up)**
**Scenario:** Karakter membesar saat mengambil item kekuatan
```
Rumus: (x', y') = (sx·x, sy·y)
Implementasi: sx = sy = 1.5
```

 4. **REFLECTION (Mirror World)**
**Scenario:** Scene ter-refleksi secara horizontal di dunia cermin
```
Rumus: (x', y') = (-x, y)
Implementasi: Refleksi terhadap sumbu-Y
```

 🛠️ Teknologi yang Digunakan

- **Bahasa Pemrograman:** Python 3.x
- **Library:** Turtle Graphics (standar Python)
- **Konsep Matematika:** Trigonometri, Geometri Analitik, Matriks Transformasi
- **Platform:** Cross-platform (Windows, macOS, Linux)

 🎮 Fitur Game

 **Karakter dan Objek:**
1. **Pemain (Player)** - Karakter utama berbentuk segitiga
2. **Tangan (Hand)** - Untuk animasi pukulan
3. **Musuh (Enemy)** - Target yang bisa dipukul
4. **Item Kekuatan (Power Item)** - Item untuk scaling

 **Mekanika Game:**
- **Collision Detection** antara karakter dan musuh
- **State Management** untuk tracking game progress
- **Visual Feedback** melalui perubahan warna dan ukuran
- **Real-time Transformation** dengan update dinamis

 **Kontrol Permainan:**
| Tombol | Aksi | Transformasi |
|--------|------|--------------|
| **D** | Dash Movement | Translasi |
| **R** | Rotate Hand | Rotasi |
| **S** | Scale Up | Scaling |
| **M** | Mirror World | Refleksi |
| **SPACE** | Reset Game | - |

 📁 Struktur Kode

 **Kelas Utama: `Transformasi2D`**

 **Atribut:**
- `player`, `hand`, `enemy`, `power_item` - Objek game
- `player_x`, `player_y` - Posisi karakter
- `scale_factor` - Faktor scaling
- `rotation_angle` - Sudut rotasi tangan
- `mirror_world` - Status mirror world
- `game_state` - Status permainan

 **Metode Utama:**

1. **`__init__()`** - Inisialisasi game environment
2. **`dash_transform()`** - Implementasi translasi
3. **`rotate_hand()`** - Implementasi rotasi
4. **`scale_character()`** - Implementasi scaling
5. **`toggle_mirror_world()`** - Implementasi refleksi
6. **`update_player_position()`** - Update posisi dengan transformasi
7. **`check_collision()`** - Deteksi tabrakan
8. **`update_info()`** - Display informasi status
9. **`reset_game()`** - Reset ke kondisi awal

 🚀 Cara Menjalankan Program

 **Prerequisites:**
- Python 3.x terinstal
- Library Turtle (sudah termasuk dalam Python standard library)

 **Langkah-langkah:**

1. **Clone/Download kode:**
   ```bash
   git clone <repository-url>
   cd praktikum-transformasi-2d
   ```

2. **Jalankan program:**
   ```bash
   python transformasi_2d_game.py
   ```

3. **Atau jalankan di IDE:**
   - Buka file `transformasi_2d_game.py` di IDE Python
   - Run program dari menu Run/Execute

 📊 Output Program

 **1. Console Output:**
```
==============================================================
PRAKTIKUM TRANSFORMASI 2D - GRAFIKA KOMPUTER
Program Studi Ilmu Komputer
Universitas Nahdlatul Ulama Blitar
==============================================================

TRANSFORMASI 1: TRANSLASI (DASH)
Posisi sebelum: (10.0, 5.0)
Translasi: (20, 0)
Posisi setelah: (30.0, 5.0)
--------------------------------------------------
```

 **2. Visual Display:**
- **Game Window** dengan background hitam
- **Karakter pemain** (segitiga cyan)
- **Tangan** (lingkaran kuning)
- **Musuh** (kotak merah)
- **Item kekuatan** (lingkaran orange)

 **3. Information Panel:**
- Status semua transformasi
- Posisi dan rotasi terkini
- Status game (power collected, enemy hit)
- Petunjuk kontrol
- Rumus matematika transformasi

 🔬 Analisis Matematika

 **Matriks Transformasi:**

1. **Translasi:**
   ```
   [ 1  0  dx ]
   [ 0  1  dy ]
   [ 0  0  1  ]
   ```

2. **Rotasi:**
   ```
   [ cosθ  -sinθ  0 ]
   [ sinθ   cosθ  0 ]
   [  0      0    1 ]
   ```

3. **Scaling:**
   ```
   [ sx   0   0 ]
   [ 0   sy   0 ]
   [ 0    0   1 ]
   ```

4. **Refleksi (sumbu-Y):**
   ```
   [ -1  0  0 ]
   [  0  1  0 ]
   [  0  0  1 ]
   ```

 **Urutan Transformasi:**
Urutan aplikasi transformasi mempengaruhi hasil akhir:
```
Final_Position = Reflection × Scaling × Rotation × Translation × Original_Position
```

 📈 Hasil dan Pembelajaran

 **Observasi:**
1. **Translasi** adalah transformasi yang paling intuitif
2. **Rotasi** memerlukan handling sudut dan trigonometri
3. **Scaling** mempengaruhi ukuran tanpa mengubah posisi pusat
4. **Refleksi** mengubah orientasi seluruh coordinate system
5. **Urutan transformasi** sangat kritis dalam hasil akhir

 **Challenge yang Diatasi:**
1. **Koordinat relatif** untuk posisi tangan
2. **State management** untuk multiple transformations
3. **Visual feedback** yang konsisten
4. **Collision detection** dalam coordinate system yang berubah

 🧪 Test Scenario

 **Sequence Testing:**
```python
1. Start at (10, 5)
2. Press D (Dash) → Move to (30, 5)
3. Press R (Rotate) → Hand rotates 30°
4. Press S (Scale) → Character scales 1.5x
5. Press M (Mirror) → World flips horizontally
6. Press SPACE → Reset to initial state
```

 **Edge Cases:**
1. Multiple rotations beyond 360°
2. Scaling multiple times
3. Mirror world toggle while transformed
4. Collision in mirrored coordinates
