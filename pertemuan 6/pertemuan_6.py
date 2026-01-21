import turtle
import math
import time

class Transformasi2D:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("Transformasi 2D - Game Platformer")
        self.screen.bgcolor("black")
        self.screen.setup(width=1200, height=700)
        
        # Karakter pemain
        self.player = turtle.Turtle()
        self.player.shape("triangle")
        self.player.color("cyan")
        self.player.shapesize(2, 1.5, 1)
        self.player.penup()
        
        # Tangan karakter
        self.hand = turtle.Turtle()
        self.hand.shape("circle")
        self.hand.color("yellow")
        self.hand.shapesize(0.5)
        self.hand.penup()
        
        # Musuh
        self.enemy = turtle.Turtle()
        self.enemy.shape("square")
        self.enemy.color("red")
        self.enemy.shapesize(1.5)
        self.enemy.penup()
        
        # Item kekuatan
        self.power_item = turtle.Turtle()
        self.power_item.shape("circle")
        self.power_item.color("orange")
        self.power_item.shapesize(1)
        self.power_item.penup()
        
        # Dunia cermin (aktif/tidak)
        self.mirror_world = False
        self.original_positions = {}
        
        # Status game
        self.game_state = "Ready"
        self.power_collected = False
        self.enemy_hit = False
        
        # Posisi awal
        self.player_x = 10
        self.player_y = 5
        self.scale_factor = 1.0
        self.rotation_angle = 0
        self.hand_distance = 30
        
        # Setup posisi awal
        self.setup_scene()
        
        # Binding keyboard
        self.screen.listen()
        self.screen.onkey(self.dash_transform, "d")  # Tombol D untuk Dash
        self.screen.onkey(self.rotate_hand, "r")     # Tombol R untuk Rotate
        self.screen.onkey(self.scale_character, "s") # Tombol S untuk Scale
        self.screen.onkey(self.toggle_mirror_world, "m") # Tombol M untuk Mirror World
        self.screen.onkey(self.reset_game, "space")  # Spasi untuk Reset
        
        # Info display
        self.info_display = turtle.Turtle()
        self.info_display.hideturtle()
        self.info_display.penup()
        self.info_display.color("white")
        
        self.update_info()
    
    def setup_scene(self):
        """Setup posisi awal semua objek"""
        # Reset semua transformasi
        self.mirror_world = False
        self.power_collected = False
        self.enemy_hit = False
        self.scale_factor = 1.0
        self.rotation_angle = 0
        
        # Set posisi pemain
        self.player_x = 10
        self.player_y = 5
        self.update_player_position()
        
        # Set posisi tangan relatif terhadap pemain
        self.update_hand_position()
        
        # Set posisi musuh
        self.enemy.goto(100, 5)
        
        # Set posisi item kekuatan
        self.power_item.goto(-100, 5)
        
        # Simpan posisi original untuk mirror world
        self.original_positions = {
            'player': (self.player_x, self.player_y),
            'enemy': (100, 5),
            'power_item': (-100, 5),
            'hand': (self.hand.xcor(), self.hand.ycor())
        }
        
        # Reset visual
        self.player.color("cyan")
        self.hand.color("yellow")
        self.enemy.color("red")
        self.power_item.color("orange")
        self.power_item.showturtle()
    
    def update_player_position(self):
        """Update posisi pemain dengan transformasi yang ada"""
        x = self.player_x
        y = self.player_y
        
        # Apply mirror transformation jika aktif
        if self.mirror_world:
            x = -x
        
        # Apply scaling
        self.player.shapesize(2 * self.scale_factor, 1.5 * self.scale_factor, 1)
        
        # Move player
        self.player.goto(x, y)
        
        # Apply rotation (untuk tangan, bukan seluruh karakter)
        # Karakter tetap menghadap kanan/kiri tergantung mirror world
    
    def update_hand_position(self):
        """Update posisi tangan relatif terhadap pemain"""
        # Hitung posisi tangan berdasarkan rotasi
        angle_rad = math.radians(self.rotation_angle)
        hand_x = self.player_x + self.hand_distance * math.cos(angle_rad)
        hand_y = self.player_y + self.hand_distance * math.sin(angle_rad)
        
        # Apply mirror transformation jika aktif
        if self.mirror_world:
            hand_x = -hand_x
        
        # Update posisi tangan
        self.hand.goto(hand_x, hand_y)
    
    def dash_transform(self):
        """Transformasi Translasi: Dash (bergerak cepat ke kanan)"""
        if self.game_state != "Game Over":
            print("TRANSFORMASI 1: TRANSLASI (DASH)")
            print(f"Posisi sebelum: ({self.player_x}, {self.player_y})")
            
            # Translasi: tambahkan dx=20, dy=0
            dx = 20
            dy = 0
            
            # Jika di mirror world, gerak ke kiri
            if self.mirror_world:
                dx = -dx
            
            self.player_x += dx
            self.player_y += dy
            
            print(f"Translasi: ({dx}, {dy})")
            print(f"Posisi setelah: ({self.player_x}, {self.player_y})")
            print("-" * 50)
            
            # Update posisi
            self.update_player_position()
            self.update_hand_position()
            
            # Check collision dengan musuh
            self.check_collision()
            
            self.game_state = "Dashing"
            self.update_info()
    
    def rotate_hand(self):
        """Transformasi Rotasi: Memutar tangan karakter 30 derajat"""
        if self.game_state != "Game Over":
            print("TRANSFORMASI 2: ROTASI")
            print(f"Sudut sebelum: {self.rotation_angle}°")
            
            # Rotasi: tambahkan 30 derajat
            self.rotation_angle += 30
            
            # Normalisasi sudut ke 0-360
            self.rotation_angle %= 360
            
            print(f"Rotasi: +30°")
            print(f"Sudut setelah: {self.rotation_angle}°")
            print("-" * 50)
            
            # Update posisi tangan
            self.update_hand_position()
            
            # Animasi pukulan
            self.animate_punch()
            
            self.game_state = "Rotating"
            self.update_info()
    
    def scale_character(self):
        """Transformasi Scaling: Membesar 1.5x"""
        if self.game_state != "Game Over" and not self.power_collected:
            print("TRANSFORMASI 3: SCALING")
            print(f"Scale sebelum: {self.scale_factor}x")
            
            # Scaling: kalikan dengan 1.5
            self.scale_factor *= 1.5
            
            print(f"Scaling: ×1.5")
            print(f"Scale setelah: {self.scale_factor:.2f}x")
            print("-" * 50)
            
            # Update ukuran karakter
            self.update_player_position()
            
            # Tandai item telah diambil
            self.power_collected = True
            self.power_item.hideturtle()
            self.player.color("gold")  # Ubah warna saat power up
            
            self.game_state = "Scaling"
            self.update_info()
    
    def toggle_mirror_world(self):
        """Transformasi Refleksi: Mirror World (refleksi terhadap sumbu-Y)"""
        print("TRANSFORMASI 4: REFLEKSI (Mirror World)")
        print(f"Mirror World sebelum: {self.mirror_world}")
        
        # Toggle mirror world
        self.mirror_world = not self.mirror_world
        
        print(f"Refleksi terhadap sumbu-Y: {'AKTIF' if self.mirror_world else 'NON-AKTIF'}")
        print("-" * 50)
        
        # Apply mirror transformation ke semua objek
        self.apply_mirror_transformation()
        
        # Update karakter menghadap arah yang benar
        if self.mirror_world:
            self.player.tiltangle(180)  # Hadap kiri
        else:
            self.player.tiltangle(0)    # Hadap kanan
        
        self.game_state = "Mirror World"
        self.update_info()
    
    def apply_mirror_transformation(self):
        """Terapkan transformasi mirror ke semua objek"""
        # Simpan posisi asli jika masuk mirror world pertama kali
        if self.mirror_world and len(self.original_positions) > 0:
            # Untuk semua objek, kalikan x dengan -1
            self.player_x = -self.player_x
            self.update_player_position()
            self.update_hand_position()
            
            # Mirror posisi musuh
            enemy_x, enemy_y = self.original_positions['enemy']
            self.enemy.goto(-enemy_x, enemy_y)
            
            # Mirror posisi item
            item_x, item_y = self.original_positions['power_item']
            self.power_item.goto(-item_x, item_y)
        elif not self.mirror_world:
            # Kembalikan ke posisi original
            self.player_x, self.player_y = self.original_positions['player']
            self.update_player_position()
            self.update_hand_position()
            
            enemy_x, enemy_y = self.original_positions['enemy']
            self.enemy.goto(enemy_x, enemy_y)
            
            item_x, item_y = self.original_positions['power_item']
            self.power_item.goto(item_x, item_y)
    
    def check_collision(self):
        """Cek tabrakan dengan musuh"""
        distance = math.sqrt((self.player_x - 100)**2 + (self.player_y - 5)**2)
        
        # Jika di mirror world, gunakan posisi mirrored musuh
        if self.mirror_world:
            distance = math.sqrt((self.player_x - (-100))**2 + (self.player_y - 5)**2)
        
        if distance < 40:  # Threshold collision
            print("COLLISION DETECTED! Karakter menabrak musuh!")
            self.enemy_hit = True
            self.enemy.color("gray")  # Musuh mati
    
    def animate_punch(self):
        """Animasi pukulan tangan"""
        if self.enemy_hit:
            original_color = self.hand.color()
            self.hand.color("white")
            self.screen.update()
            time.sleep(0.1)
            self.hand.color(original_color)
            self.screen.update()
    
    def update_info(self):
        """Update informasi status game di layar"""
        self.info_display.clear()
        
        # Title
        self.info_display.goto(0, 300)
        self.info_display.write("TRANSFORMASI 2D - GAME PLATFORMER", 
                               align="center", font=("Arial", 16, "bold"))
        
        # Subtitle
        self.info_display.goto(0, 275)
        self.info_display.write("Program Studi Ilmu Komputer - Universitas Nahdlatul Ulama Blitar", 
                               align="center", font=("Arial", 10, "normal"))
        
        # Status transformasi
        self.info_display.goto(-550, 250)
        self.info_display.write("STATUS TRANSFORMASI:", 
                               align="left", font=("Arial", 12, "bold"))
        
        self.info_display.goto(-550, 220)
        self.info_display.write(f"1. Posisi Karakter: ({self.player_x:.1f}, {self.player_y:.1f})", 
                               align="left", font=("Arial", 10, "normal"))
        
        self.info_display.goto(-550, 200)
        self.info_display.write(f"2. Rotasi Tangan: {self.rotation_angle}°", 
                               align="left", font=("Arial", 10, "normal"))
        
        self.info_display.goto(-550, 180)
        self.info_display.write(f"3. Scale Karakter: {self.scale_factor:.2f}x", 
                               align="left", font=("Arial", 10, "normal"))
        
        self.info_display.goto(-550, 160)
        mirror_status = "AKTIF" if self.mirror_world else "NON-AKTIF"
        self.info_display.write(f"4. Mirror World: {mirror_status}", 
                               align="left", font=("Arial", 10, "normal"))
        
        # Status game
        self.info_display.goto(-550, 120)
        self.info_display.write("STATUS GAME:", 
                               align="left", font=("Arial", 12, "bold"))
        
        power_status = "SUDAH" if self.power_collected else "BELUM"
        self.info_display.goto(-550, 90)
        self.info_display.write(f"• Power Item: {power_status} diambil", 
                               align="left", font=("Arial", 10, "normal"))
        
        enemy_status = "TERKENA" if self.enemy_hit else "SEHAT"
        self.info_display.goto(-550, 70)
        self.info_display.write(f"• Musuh: {enemy_status}", 
                               align="left", font=("Arial", 10, "normal"))
        
        # Kontrol
        self.info_display.goto(200, 250)
        self.info_display.write("KONTROL PERMAINAN:", 
                               align="left", font=("Arial", 12, "bold"))
        
        self.info_display.goto(200, 220)
        self.info_display.write("D : Dash (Translasi)", 
                               align="left", font=("Arial", 10, "normal"))
        
        self.info_display.goto(200, 200)
        self.info_display.write("R : Rotate Hand (Rotasi)", 
                               align="left", font=("Arial", 10, "normal"))
        
        self.info_display.goto(200, 180)
        self.info_display.write("S : Scale Up (Scaling)", 
                               align="left", font=("Arial", 10, "normal"))
        
        self.info_display.goto(200, 160)
        self.info_display.write("M : Mirror World (Refleksi)", 
                               align="left", font=("Arial", 10, "normal"))
        
        self.info_display.goto(200, 140)
        self.info_display.write("SPACE : Reset Game", 
                               align="left", font=("Arial", 10, "normal"))
        
        # Rumus Transformasi
        self.info_display.goto(200, 80)
        self.info_display.write("RUMUS TRANSFORMASI:", 
                               align="left", font=("Arial", 12, "bold"))
        
        self.info_display.goto(200, 50)
        self.info_display.write("1. Translasi: (x', y') = (x+dx, y+dy)", 
                               align="left", font=("Courier", 9, "normal"))
        
        self.info_display.goto(200, 30)
        self.info_display.write("2. Rotasi: x' = x·cosθ - y·sinθ", 
                               align="left", font=("Courier", 9, "normal"))
        self.info_display.goto(200, 10)
        self.info_display.write("   y' = x·sinθ + y·cosθ", 
                               align="left", font=("Courier", 9, "normal"))
        
        self.info_display.goto(200, -10)
        self.info_display.write("3. Scaling: (x', y') = (sx·x, sy·y)", 
                               align="left", font=("Courier", 9, "normal"))
        
        self.info_display.goto(200, -30)
        self.info_display.write("4. Refleksi Y: (x', y') = (-x, y)", 
                               align="left", font=("Courier", 9, "normal"))
    
    def reset_game(self):
        """Reset game ke kondisi awal"""
        print("\n" + "="*50)
        print("RESET GAME")
        print("="*50)
        
        self.setup_scene()
        self.game_state = "Ready"
        self.update_info()
        
        print("Game telah direset ke kondisi awal!")
        print("-"*50)
    
    def run(self):
        """Jalankan game"""
        print("="*70)
        print("PRAKTIKUM TRANSFORMASI 2D - GRAFIKA KOMPUTER")
        print("Program Studi Ilmu Komputer")
        print("Universitas Nahdlatul Ulama Blitar")
        print("="*70)
        
        print("\nSCENARIO GAME:")
        print("1. Karakter mulai di posisi (10, 5)")
        print("2. Tekan D untuk DASH (Translasi: dx=20, dy=0)")
        print("3. Tekan R untuk ROTATE HAND (Rotasi: +30°)")
        print("4. Tekan S untuk SCALE UP (Scaling: ×1.5)")
        print("5. Tekan M untuk MIRROR WORLD (Refleksi sumbu-Y)")
        print("6. Tekan SPACE untuk RESET")
        
        print("\nTransformasi akan ditampilkan di console dan layar!")
        print("-"*70)
        
        turtle.mainloop()

# Jalankan game
if __name__ == "__main__":
    game = Transformasi2D()
    game.run()