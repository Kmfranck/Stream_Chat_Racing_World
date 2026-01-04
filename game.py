import pygame
import threading
import time
import queue
import sys
import io
import random
import math
import os
import re
import statistics
import socket
import ssl

# --- CORRECTION ENCODAGE ---
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ================= CONFIGURATION =================
# Choisir la plateforme: "twitch", "youtube", ou "both"
PLATFORM = "both"  # 👈 MODIFIER ICI

# Configuration Twitch (si utilisé)
TWITCH_CHANNEL = "xxxxxxxxx"  # 👇 REMPLACE PAR LE NOM DE TA CHAINE
TWITCH_TOKEN = "oauth:xxxxxxxxxxxxxx"  # 👇 REMPLACE PAR TON TOKEN
TWITCH_CLIENT_ID = "xxxxxxxxxxxxxxxxxxxx"  # 👇 Optionnel

# Configuration YouTube (si utilisé)
YOUTUBE_VIDEO_ID = "xxxxxxxxxxxxx"  # 👇 REMPLACE PAR L'ID DE TON LIVE

# Import conditionnel pour YouTube
if PLATFORM in ["youtube", "both"]:
    try:
        import pytchat
        YOUTUBE_AVAILABLE = True
    except ImportError:
        print("⚠️ pytchat non installé. Pour YouTube: pip install pytchat")
        YOUTUBE_AVAILABLE = False
else:
    YOUTUBE_AVAILABLE = False

# ================= CONFIGURATION JEU =================
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
FULLSCREEN = False
FPS = 60
BOOST_AMOUNT = 35
MAX_SPEED = 10
SMOOTHING = 0.2

# Couleurs
C_BG = (15, 30, 60)
C_ROAD = (40, 40, 45)
C_ROAD_LINE = (200, 200, 100, 180)
C_WHITE = (255, 255, 255)
C_BLACK = (20, 20, 20)
C_ACCENT = (255, 215, 0)
C_ACCENT2 = (100, 200, 255)

# Dégradés pour les pays
COLOR_GRADIENTS = [
    [(60, 59, 110), (120, 120, 255)],    # USA
    [(255, 255, 255), (200, 230, 255)],   # Canada
    [(0, 156, 59), (255, 223, 0)],       # Brésil
    [(0, 85, 164), (100, 160, 255)],     # France
    [(0, 0, 0), (255, 206, 0)],          # Allemagne
    [(0, 135, 81), (255, 255, 255)],     # Nigeria
    [(193, 39, 45), (0, 98, 51)],        # Maroc
    [(255, 153, 51), (0, 153, 51)],      # Inde
    [(255, 0, 0), (255, 255, 0)],        # Chine
    [(255, 255, 255), (188, 0, 45)],     # Japon
    [(255, 255, 255), (0, 57, 166)],     # Russie
    [(128, 128, 128), (200, 200, 200)]   # Autre
]

# Liste des 12 pays principaux
MAIN_COUNTRIES = [
    {"id": "usa", "name": "USA", "color_idx": 0},
    {"id": "canada", "name": "CANADA", "color_idx": 1},
    {"id": "bresil", "name": "BAZIL", "color_idx": 2},
    {"id": "france", "name": "FRANCE", "color_idx": 3},
    {"id": "allemagne", "name": "GERMAN", "color_idx": 4},
    {"id": "nigeria", "name": "NIGERIA", "color_idx": 5},
    {"id": "maroc", "name": "MAROCCO", "color_idx": 6},
    {"id": "inde", "name": "INDIA", "color_idx": 7},
    {"id": "chine", "name": "CHINA", "color_idx": 8},
    {"id": "japon", "name": "JAPAN", "color_idx": 9},
    {"id": "russie", "name": "RUSSIA", "color_idx": 10},
]

# Liste complète des PARTICIPANTS (12 pays + Autre)
PARTICIPANTS = MAIN_COUNTRIES + [
    {"id": "autre", "name": "AUTRE", "color_idx": 11},
]

# File d'attente pour les messages
msg_queue = queue.Queue()

# Liste de TOUS les pays du monde
WORLD_COUNTRIES = [
    "algerie", "angola", "benin", "botswana", "burkina", "burundi", "cameroun", "cap vert",
    "centrafrique", "comores", "congo", "cote ivoire", "djibouti", "egypte", "erythree",
    "ethiopie", "gabon", "gambie", "ghana", "guinee", "guinee bissau", "guinee equatoriale",
    "kenya", "lesotho", "liberia", "libye", "madagascar", "malawi", "mali", "maroc", "maurice",
    "mauritanie", "mozambique", "namibie", "niger", "nigeria", "ouganda", "rwanda", "sao tome",
    "senegal", "seychelles", "sierra leone", "somalie", "soudan", "swaziland", "tanzanie",
    "tchad", "togo", "tunisie", "zambie", "zimbabwe",
    
    "argentine", "bahamas", "barbade", "belize", "bolivie", "bresil", "canada", "chili",
    "colombie", "costa rica", "cuba", "dominique", "equateur", "etats unis", "grenade",
    "guatemala", "guyana", "haiti", "honduras", "jamaique", "mexique", "nicaragua", "panama",
    "paraguay", "perou", "republique dominicaine", "salvador", "saint christophe",
    "sainte lucie", "saint vincent", "suriname", "trinite", "uruguay", "venezuela",
    
    "afghanistan", "arabie saoudite", "armenie", "azerbaidjan", "bahrein", "bangladesh",
    "bhoutan", "birmanie", "brunei", "cambodge", "chine", "coree du nord", "coree du sud",
    "emirats arabes unis", "georgie", "inde", "indonesie", "irak", "iran", "israel",
    "japon", "jordanie", "kazakhstan", "kirghizistan", "koweit", "laos", "liban",
    "malaisie", "maldives", "mongolie", "nepal", "oman", "ouzbekistan", "pakistan",
    "philippines", "qatar", "singapour", "sri lanka", "syrie", "tadjikistan", "taiwan",
    "thailande", "timor oriental", "turkménistan", "turquie", "vietnam", "yemen",
    
    "albanie", "allemagne", "andorre", "autriche", "belgique", "bielorussie", "bosnie",
    "bulgarie", "chypre", "croatie", "danemark", "espagne", "estonie", "finlande",
    "france", "grece", "hongrie", "irlande", "islande", "italie", "lettonie", "liechtenstein",
    "lituanie", "luxembourg", "macedoine", "malte", "moldavie", "monaco", "montenegro",
    "norvege", "pays bas", "pologne", "portugal", "roumanie", "royaume uni", "russie",
    "saint marin", "serbie", "slovaquie", "slovenie", "suede", "suisse", "republique tcheque",
    "ukraine", "vatican",
    
    "australie", "fidji", "iles marshall", "iles salomon", "kiribati", "micronesie",
    "nauru", "nouvelle zelande", "palaos", "papouasie nouvelle guinee", "samoa",
    "tonga", "tuvalu", "vanuatu"
]

# ================= GESTION DES JOUEURS =================
class PlayerTracker:
    def __init__(self):
        self.unique_players = set()
        self.session_votes = []
        self.session_players = []
        self.current_session_players = set()
    
    def add_vote(self, player_name):
        self.unique_players.add(player_name)
        self.current_session_players.add(player_name)
    
    def start_new_race(self):
        if self.current_session_players:
            self.session_players.append(len(self.current_session_players))
            self.current_session_players = set()
    
    def get_average_players_per_race(self):
        if not self.session_players:
            return 0
        return statistics.mean(self.session_players)
    
    def get_total_unique_players(self):
        return len(self.unique_players)
    
    def get_current_session_count(self):
        return len(self.current_session_players)

# ================= PARTICULES =================
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-2, 0)
        self.life = random.randint(20, 40)
        self.color = color
        self.size = random.randint(2, 5)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1
        self.life -= 1
        return self.life > 0
    
    def draw(self, surface):
        alpha = min(255, self.life * 8)
        pygame.draw.circle(surface, (*self.color, alpha), (int(self.x), int(self.y)), self.size)

# ================= DÉTECTION DES PAYS =================
COUNTRY_KEYWORDS = {
    "usa": ["usa", "us", "united states", "america", "états-unis", "états unis", "amérique", "states"],
    "canada": ["canada", "can", "ca"],
    "bresil": ["bresil", "brésil", "brazil", "br", "brasil"],
    "france": ["france", "fr", "français", "french", "francais"],
    "allemagne": ["allemagne", "germany", "deutschland", "de", "germagne"],
    "nigeria": ["nigeria", "ng"],
    "maroc": ["maroc", "morocco", "ma", "marocco"],
    "inde": ["inde", "india", "in", "ind"],
    "chine": ["chine", "china", "cn", "chinese"],
    "japon": ["japon", "japan", "jp", "jap"],
    "russie": ["russie", "russia", "ru", "russe"]
}

def detect_country_in_message(message):
    message_lower = message.lower()
    
    for country_id, keywords in COUNTRY_KEYWORDS.items():
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', message_lower):
                return country_id
    
    for country in WORLD_COUNTRIES:
        if re.search(r'\b' + re.escape(country) + r'\b', message_lower):
            return "autre"
    
    for country in MAIN_COUNTRIES:
        country_name_lower = country["name"].lower()
        if re.search(r'\b' + re.escape(country_name_lower) + r'\b', message_lower):
            return country["id"]
    
    return "autre"

# ================= CLASSE VOITURE =================
class Car:
    def __init__(self, config, y_pos, idx):
        self.id = config["id"]
        self.name = config["name"]
        self.color_idx = config["color_idx"]
        self.wins = 0
        self.idx = idx
        
        self.x = 250
        self.target_x = 250
        self.y = y_pos
        self.start_x = 250
        
        self.bounce = 0
        self.bounce_dir = 1
        self.particles = []
        
        self.last_voter = ""
        self.flash_timer = 0
        self.boost_effect = 0
        
        flag_path = f"flags/{self.id}.png"
        if os.path.exists(flag_path):
            try:
                raw_img = pygame.image.load(flag_path).convert_alpha()
                self.flag_image = pygame.transform.scale(raw_img, (40, 25))
                self.has_flag = True
            except:
                self.has_flag = False
        else:
            self.has_flag = False
    
    def boost(self, voter):
        self.target_x += BOOST_AMOUNT
        self.last_voter = voter
        self.flash_timer = 15
        self.boost_effect = 10
        
        for _ in range(8):
            color1, color2 = COLOR_GRADIENTS[self.color_idx]
            color = random.choice([color1, color2])
            self.particles.append(Particle(
                self.x + 40,
                self.y + 20,
                color
            ))

    def update(self):
        diff = self.target_x - self.x
        
        if abs(diff) > 0.5:
            step = diff * SMOOTHING
            if abs(step) > MAX_SPEED:
                step = MAX_SPEED if step > 0 else -MAX_SPEED
            self.x += step
        else:
            self.x = self.target_x
        
        self.bounce += 0.2 * self.bounce_dir
        if abs(self.bounce) > 3:
            self.bounce_dir *= -1
        
        self.particles = [p for p in self.particles if p.update()]
        
        if self.flash_timer > 0:
            self.flash_timer -= 1
        if self.boost_effect > 0:
            self.boost_effect -= 1

    def draw_shadow(self, surface, x, y):
        shadow = pygame.Surface((70, 15), pygame.SRCALPHA)
        shadow.fill((0, 0, 0, 80))
        pygame.draw.ellipse(shadow, (0, 0, 0, 60), (0, 0, 70, 15))
        surface.blit(shadow, (x + 5, y + 40))

    def draw_car_body(self, surface, x, y):
        color1, color2 = COLOR_GRADIENTS[self.color_idx]
        
        car_rect = pygame.Rect(x, y, 70, 40)
        
        for i in range(40):
            ratio = i / 40
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            pygame.draw.line(surface, (r, g, b), 
                           (x, y + i), (x + 70, y + i))
        
        pygame.draw.rect(surface, (255, 255, 255, 30), car_rect, 2, border_radius=6)
        pygame.draw.rect(surface, (100, 150, 255, 150), (x + 45, y + 10, 20, 10), border_radius=2)
        pygame.draw.circle(surface, (255, 255, 200), (x + 65, y + 10), 5)
        pygame.draw.circle(surface, (255, 255, 200), (x + 65, y + 30), 5)
        
        wheel_color = (30, 30, 30)
        pygame.draw.circle(surface, wheel_color, (x + 15, y + 45), 8)
        pygame.draw.circle(surface, wheel_color, (x + 55, y + 45), 8)
        pygame.draw.circle(surface, (100, 100, 100), (x + 15, y + 45), 5)
        pygame.draw.circle(surface, (100, 100, 100), (x + 55, y + 45), 5)
        
        if self.has_flag:
            flag_x = x + 5
            flag_y = y - 15
            pygame.draw.line(surface, (180, 180, 180), 
                           (flag_x, flag_y + 10), (flag_x, flag_y + 25), 2)
            surface.blit(self.flag_image, (flag_x + 2, flag_y + 5))
            flag_rect = pygame.Rect(flag_x + 2, flag_y + 5, 40, 25)
            pygame.draw.rect(surface, (0, 0, 0, 80), flag_rect, 1)
        else:
            flag_x = x + 5
            flag_y = y - 10
            color1, color2 = COLOR_GRADIENTS[self.color_idx]
            pygame.draw.rect(surface, color1, (flag_x, flag_y, 20, 12))
            pygame.draw.rect(surface, color2, (flag_x, flag_y, 20, 6))

    def draw(self, surface):
        draw_x = self.x
        draw_y = self.y + self.bounce
        
        self.draw_shadow(surface, draw_x, draw_y)
        self.draw_car_body(surface, draw_x, draw_y)
        
        if self.boost_effect > 0:
            trail_length = 15
            for i in range(trail_length):
                alpha = 100 - (i * 100 // trail_length)
                width = 30 - (i * 20 // trail_length)
                height = 20 - (i * 10 // trail_length)
                trail_rect = pygame.Rect(
                    draw_x - i * 3 - 10,
                    draw_y + (40 - height) // 2,
                    width,
                    height
                )
                color1, color2 = COLOR_GRADIENTS[self.color_idx]
                trail_color = (
                    (color1[0] + color2[0]) // 2,
                    (color1[1] + color2[1]) // 2,
                    (color1[2] + color2[2]) // 2,
                    alpha
                )
                s = pygame.Surface((width, height), pygame.SRCALPHA)
                pygame.draw.rect(s, trail_color, (0, 0, width, height), border_radius=4)
                surface.blit(s, trail_rect)
        
        if self.flash_timer > 0:
            s = pygame.Surface((75, 55), pygame.SRCALPHA)
            flash_alpha = min(150, self.flash_timer * 15)
            s.fill((255, 255, 255, flash_alpha))
            surface.blit(s, (draw_x - 2, draw_y - 17))
            
            if self.flash_timer > 5:
                v_txt = font_tiny.render(f"↑ {self.last_voter[:12]}", True, C_ACCENT)
                name_bg = pygame.Surface((v_txt.get_width() + 8, v_txt.get_height() + 4), pygame.SRCALPHA)
                name_bg.fill((0, 0, 0, 180))
                surface.blit(name_bg, (draw_x - 4, draw_y + 70))
                surface.blit(v_txt, (draw_x, draw_y + 72))
        
        n_txt = font_small.render(self.name, True, C_WHITE)
        name_bg = pygame.Surface((n_txt.get_width() + 8, n_txt.get_height() + 4), pygame.SRCALPHA)
        name_bg.fill((0, 0, 0, 180))
        surface.blit(name_bg, (draw_x - 4, draw_y + 55))
        surface.blit(n_txt, (draw_x, draw_y + 57))
        
        for particle in self.particles:
            particle.draw(surface)

    def reset(self):
        self.x = self.start_x
        self.target_x = self.start_x
        self.flash_timer = 0
        self.boost_effect = 0
        self.last_voter = ""
        self.particles = []

# ================= CONNEXION TWITCH =================
class TwitchChatReader:
    def __init__(self, queue, player_tracker, channel, token):
        self.msg_queue = queue
        self.player_tracker = player_tracker
        self.channel = channel.lower()
        self.token = token
        self.running = True
        self.sock = None
        
    def connect(self):
        print(f"🔌 Connexion à Twitch: #{self.channel}")
        
        try:
            context = ssl.create_default_context()
            self.sock = context.wrap_socket(
                socket.socket(socket.AF_INET, socket.SOCK_STREAM), 
                server_hostname='irc.chat.twitch.tv'
            )
            
            self.sock.connect(('irc.chat.twitch.tv', 6697))
            
            self.send_command(f"PASS {self.token}")
            self.send_command(f"NICK {self.channel}")
            self.send_command(f"JOIN #{self.channel}")
            self.send_command("CAP REQ :twitch.tv/commands")
            self.send_command("CAP REQ :twitch.tv/tags")
            
            print("✅ Connecté au chat Twitch!")
            return True
            
        except Exception as e:
            print(f"❌ Erreur connexion: {e}")
            return False
    
    def send_command(self, command):
        try:
            self.sock.send(f"{command}\r\n".encode('utf-8'))
        except:
            pass
    
    def read_messages(self):
        buffer = ""
        
        while self.running:
            try:
                data = self.sock.recv(2048)
                if not data:
                    print("❌ Connexion perdue")
                    break
                
                buffer += data.decode('utf-8', errors='ignore')
                
                while '\r\n' in buffer:
                    line, buffer = buffer.split('\r\n', 1)
                    self.process_line(line)
                    
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    print(f"⚠️ Erreur lecture: {e}")
                break
    
    def process_line(self, line):
        if line.startswith("PING"):
            self.send_command(f"PONG {line.split()[1]}")
            return
        
        if "Login authentication failed" in line:
            print("❌ ERREUR CRITIQUE : Le Token est invalide ou expiré !")
            return

        if "PRIVMSG" in line:
            try:
                parts = line.split("PRIVMSG", 1)
                
                meta_data = parts[0].split("!")[0]
                if meta_data.startswith(":"):
                    username = meta_data[1:]
                else:
                    username = meta_data
                
                message = parts[1].split(":", 1)[1].strip()
                
                # Ajout du tag [Twitch]
                self.msg_queue.put((f"[Twitch] {username}", message))
                print(f"📩 [Twitch/{username}]: {message}")
                
            except Exception as e:
                print(f"⚠️ Erreur parsing message: {e}")
    
    def start(self):
        if self.connect():
            self.sock.settimeout(0.5)
            self.read_messages()
    
    def stop(self):
        self.running = False
        if self.sock:
            try:
                self.sock.close()
            except:
                pass

def twitch_worker():
    print("👀 Démarrage lecteur Twitch...")
    
    token = TWITCH_TOKEN
    
    reader = TwitchChatReader(msg_queue, player_tracker, TWITCH_CHANNEL, token)
    
    max_retries = 3
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            print(f"📡 Tentative {attempt + 1}/{max_retries}...")
            reader.start()
            break
        except Exception as e:
            print(f"❌ Échec: {e}")
            if attempt < max_retries - 1:
                print(f"⏳ Nouvelle tentative dans {retry_delay}s...")
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                print("❌ Échec définitif")

# ================= CONNEXION YOUTUBE =================
# ================= CONNEXION YOUTUBE =================
def youtube_worker(live_chat): # 👈 On ajoute l'argument ici
    print("👀 Démarrage lecteur YouTube...")
    
    try:
        # On supprime la ligne "live_chat = pytchat.create..." car c'est fait avant
        
        if not live_chat.is_alive():
            print("❌ Impossible de se connecter au live YouTube")
            return
        
        print("✅ Connecté au chat YouTube!")
        
        while True:
            try:
                for chat_item in live_chat.get().sync_items():
                    author = chat_item.author.name
                    message = chat_item.message
                    
                    # Ajout du tag [YouTube]
                    msg_queue.put((f"[YouTube] {author}", message))
                    print(f"📩 [YouTube/{author}]: {message}")
                    
            except Exception as e:
                print(f"⚠️ Erreur lecture YouTube: {e}")
                time.sleep(2)
                
    except Exception as e:
        print(f"❌ Erreur connexion YouTube: {e}")

# ================= FONCTIONS DESSIN =================
def draw_background(surface):
    for y in range(surface.get_height()):
        ratio = y / surface.get_height()
        r = int(15 * (1 - ratio) + 5 * ratio)
        g = int(30 * (1 - ratio) + 15 * ratio)
        b = int(60 * (1 - ratio) + 30 * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (surface.get_width(), y))
    
    for i in range(30):
        x = (i * 47) % surface.get_width()
        y = (i * 31) % surface.get_height()
        size = 1 + (i % 2)
        brightness = 100 + (i % 155)
        pygame.draw.circle(surface, (brightness, brightness, brightness), (x, y), size)

def draw_road(surface, road_offset, cars, finish_line_x):
    pygame.draw.rect(surface, C_ROAD, (240, 0, surface.get_width() - 240, surface.get_height()))
    
    for car in cars:
        y_pos = car.y + 25
        for i in range(0, surface.get_width() - 240, 40):
            line_x = 240 + i + road_offset
            if line_x < surface.get_width():
                pygame.draw.rect(surface, C_ROAD_LINE, 
                               (line_x, y_pos, 20, 3))
    
    draw_finish_line(surface, finish_line_x)

def draw_finish_line(surface, finish_line_x):
    damier_offset = (pygame.time.get_ticks() // 100) % 40
    for y in range(0, surface.get_height(), 20):
        for x in range(0, 30, 20):
            color = C_WHITE if ((x+y+damier_offset)//20) % 2 == 0 else C_BLACK
            pygame.draw.rect(surface, color, 
                           (finish_line_x + x, y, 20, 20))
    
    glow = pygame.Surface((40, surface.get_height()), pygame.SRCALPHA)
    for i in range(40):
        alpha = abs(20 - i) * 4
        pygame.draw.line(glow, (255, 255, 200, alpha), 
                        (i, 0), (i, surface.get_height()))
    surface.blit(glow, (finish_line_x - 20, 0))
    
    finish_txt = font_small.render("The End", True, C_ACCENT)
    txt_shadow = font_small.render("The End", True, (0, 0, 0))
    surface.blit(txt_shadow, (finish_line_x - 65, 22))
    surface.blit(finish_txt, (finish_line_x - 65, 20))

def draw_sidebar(surface, cars, player_tracker):
    sidebar = pygame.Surface((240, surface.get_height()), pygame.SRCALPHA)
    for x in range(240):
        ratio = x / 240
        r = int(40 * (1 - ratio) + 60 * ratio)
        g = int(45 * (1 - ratio) + 65 * ratio)
        b = int(50 * (1 - ratio) + 70 * ratio)
        pygame.draw.line(sidebar, (r, g, b, 220), (x, 0), (x, surface.get_height()))
    
    pygame.draw.rect(sidebar, (100, 150, 255, 100), (0, 0, 240, surface.get_height()), 3)
    pygame.draw.rect(sidebar, (150, 200, 255, 50), (0, 0, 240, surface.get_height()), 1)
    
    surface.blit(sidebar, (0, 0))
    
    title = font_title.render("BOARD", True, C_ACCENT)
    surface.blit(title, (120 - title.get_width()//2, 15))
    
    avg_players = player_tracker.get_average_players_per_race()
    total_players = player_tracker.get_total_unique_players()
    current_players = player_tracker.get_current_session_count()
    
    stats_y = 55
    stats_texts = [
        f"🎮 PLAYERS: {current_players}",
        f"📊 AVERAGE/GAME: {avg_players:.1f}",
        f"👥 Total: {total_players}"
    ]
    
    for i, text in enumerate(stats_texts):
        stat_txt = font_tiny.render(text, True, C_ACCENT2)
        surface.blit(stat_txt, (20, stats_y + i * 20))
    
    pygame.draw.line(surface, (100, 150, 255, 150), (20, 115), (220, 115), 2)
    
    sorted_cars = sorted(cars, key=lambda c: c.wins, reverse=True)
    max_visible = min(10, len(sorted_cars))
    
    for i in range(max_visible):
        car = sorted_cars[i]
        y_pos = 130 + (i * 40)
        
        item_bg = pygame.Surface((200, 35), pygame.SRCALPHA)
        if i < 3:
            podium_colors = [(255, 215, 0, 80), (200, 200, 220, 80), (205, 127, 50, 80)]
            item_bg.fill(podium_colors[i])
        else:
            item_bg.fill((255, 255, 255, 30 if i % 2 == 0 else 10))
        
        surface.blit(item_bg, (20, y_pos))
        
        num_color = C_ACCENT if i < 3 else C_WHITE
        num_txt = font_country.render(f"{i+1}.", True, num_color)
        surface.blit(num_txt, (25, y_pos + 8))
        
        color1, color2 = COLOR_GRADIENTS[car.color_idx]
        
        if car.has_flag:
            try:
                flag_img = pygame.image.load(f"flags/{car.id}.png").convert_alpha()
                flag_img = pygame.transform.scale(flag_img, (25, 15))
                surface.blit(flag_img, (55, y_pos + 8))
            except:
                pygame.draw.rect(surface, color1, (55, y_pos + 7, 25, 15))
                pygame.draw.rect(surface, color2, (55, y_pos + 7, 25, 8))
        else:
            pygame.draw.rect(surface, color1, (55, y_pos + 7, 25, 15))
            pygame.draw.rect(surface, color2, (55, y_pos + 7, 25, 8))
        
        name_txt = font_small.render(car.name[:8], True, C_WHITE)
        surface.blit(name_txt, (90, y_pos + 8))
        
        score_txt = font_small.render(str(car.wins), True, C_ACCENT)
        surface.blit(score_txt, (200 - score_txt.get_width(), y_pos + 8))

def draw_chat_panel(surface, chat_log_visual):
    panel_w = 300
    panel_h = 180
    panel_x = surface.get_width() - panel_w - 10
    panel_y = surface.get_height() - panel_h - 10
    
    chat_bg = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    chat_bg.fill((0, 0, 0, 200))
    pygame.draw.rect(chat_bg, (100, 150, 255, 100), chat_bg.get_rect(), 2)
    pygame.draw.rect(chat_bg, (150, 200, 255, 50), chat_bg.get_rect(), 1)
    surface.blit(chat_bg, (panel_x, panel_y))
    
    chat_title = font_small.render("LIVE CHAT", True, C_ACCENT2)
    surface.blit(chat_title, (panel_x + 15, panel_y + 8))
    
    for i, line in enumerate(chat_log_visual[-5:]):
        if len(line) > 35:
            line = line[:32] + "..."
        
        msg_bg = pygame.Surface((panel_w - 30, 28), pygame.SRCALPHA)
        msg_bg.fill((255, 255, 255, 10 if i % 2 == 0 else 5))
        surface.blit(msg_bg, (panel_x + 15, panel_y + 35 + (i * 28)))
        
        t_msg = font_chat.render(line, True, (220, 220, 220))
        surface.blit(t_msg, (panel_x + 20, panel_y + 40 + (i * 28)))

def draw_winner_overlay(surface, winner_car, timer_reset):
    overlay = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (0, 0))
    
    crown_y = surface.get_height() // 2 - 120
    crown_points = [
        (surface.get_width()//2 - 50, crown_y + 30),
        (surface.get_width()//2 - 30, crown_y),
        (surface.get_width()//2 - 10, crown_y + 20),
        (surface.get_width()//2, crown_y),
        (surface.get_width()//2 + 10, crown_y + 20),
        (surface.get_width()//2 + 30, crown_y),
        (surface.get_width()//2 + 50, crown_y + 30)
    ]
    pygame.draw.polygon(surface, C_ACCENT, crown_points)
    
    win_text = font_title.render(f"{winner_car.name} WINS !", True, C_ACCENT)
    win_shadow = font_title.render(f"{winner_car.name} WINS !", True, (0, 0, 0))
    
    surface.blit(win_shadow, (surface.get_width()//2 - win_shadow.get_width()//2 + 3, 
                             surface.get_height()//2 - 30 + 3))
    surface.blit(win_text, (surface.get_width()//2 - win_text.get_width()//2, 
                           surface.get_height()//2 - 30))
    
    if winner_car.has_flag:
        try:
            flag_img = pygame.image.load(f"flags/{winner_car.id}.png").convert_alpha()
            flag_img = pygame.transform.scale(flag_img, (200, 100))
            surface.blit(flag_img, (surface.get_width()//2 - 100, surface.get_height()//2 + 50))
        except:
            pass
    
    time_left = 5 - (pygame.time.get_ticks() - timer_reset) // 1000
    if time_left > 0:
        count_txt = font_country.render(f"Next race: {time_left}s", True, C_ACCENT2)
        surface.blit(count_txt, (surface.get_width()//2 - count_txt.get_width()//2, 
                                surface.get_height()//2 + 180))

# ================= INITIALISATION =================
pygame.init()
pygame.mixer.init()

print("\n" + "="*50)
print("🎵 LOADING SOUNDS AND MUSIC")
print("="*50)

# Sons
snd_vroum = None
snd_win = None
music_loaded = False

try:
    music_path = "sounds/music.mp3"
    if os.path.exists(music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        music_loaded = True
        print(f"✅ Music loaded")
except Exception as e:
    print(f"❌ Music error: {e}")

try:
    vroum_path = "sounds/vroom.mp3"
    if os.path.exists(vroum_path):
        snd_vroum = pygame.mixer.Sound(vroum_path)
        snd_vroum.set_volume(0.5)
        print(f"✅ Car sound loaded")
    
    win_path = "sounds/win.mp3"
    if os.path.exists(win_path):
        snd_win = pygame.mixer.Sound(win_path)
        snd_win.set_volume(1)
        print(f"✅ Win sound loaded")
except Exception as e:
    print(f"❌ Sound error: {e}")

print("="*50)

# Fenêtre
if FULLSCREEN:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    print(f"Fullscreen mode: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
else:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("🏎️ Chat Racing - World Championship 🏁")

clock = pygame.time.Clock()

# Polices
try:
    font_title = pygame.font.Font(None, 32)
    font_small = pygame.font.Font(None, 18)
    font_tiny = pygame.font.Font(None, 14)
    font_chat = pygame.font.Font(None, 16)
    font_country = pygame.font.Font(None, 20)
except:
    font_title = pygame.font.SysFont("Arial", 32, bold=True)
    font_small = pygame.font.SysFont("Arial", 16, bold=True)
    font_tiny = pygame.font.SysFont("Arial", 12)
    font_chat = pygame.font.SysFont("Consolas", 14)
    font_country = pygame.font.SysFont("Arial", 18, bold=True)

# Création Voitures
cars = []
num_cars = len(PARTICIPANTS)
available_height = SCREEN_HEIGHT - 180
car_spacing = (available_height / num_cars)*1.2

for i, p in enumerate(PARTICIPANTS):
    y_pos = 40 + (i * car_spacing)
    cars.append(Car(p, y_pos, i))

print(f"\n📊 {num_cars} cars created")

# Vérification drapeaux
flags_available = 0
for country in MAIN_COUNTRIES:
    flag_path = f"flags/{country['id']}.png"
    if os.path.exists(flag_path):
        flags_available += 1

print(f"📁 {flags_available}/{len(MAIN_COUNTRIES)} flags available")

# Initialiser tracker
player_tracker = PlayerTracker()

# ================= CONNEXION PLATEFORMES =================
print("\n" + "="*50)
print("📡 PLATFORM CONNECTION")
print("="*50)

twitch_connected = False
youtube_connected = False

# Configuration Twitch
if PLATFORM in ["twitch", "both"]:
    if not TWITCH_TOKEN or "oauth:xxxxxxxx" in TWITCH_TOKEN:
        print("❌ ERROR: Twitch Token not configured!")
        print("  1. Go to: https://twitchapps.com/tmi/")
        print("  2. Click 'Connect'")
        print("  3. Authorize the application")
        print("  4. Copy the token starting with 'oauth:'")
        print("  5. Paste it in TWITCH_TOKEN")
    else:
        print(f"✅ Twitch token detected: {TWITCH_TOKEN[:10]}...")
        try:
            t_twitch = threading.Thread(target=twitch_worker, daemon=True)
            t_twitch.start()
            time.sleep(2)
            twitch_connected = True
            print("✅ Twitch reader started")
        except Exception as e:
            print(f"❌ Cannot start Twitch: {e}")

# Configuration YouTube
if PLATFORM in ["youtube", "both"]:
    if not YOUTUBE_AVAILABLE:
        print("❌ pytchat not installed for YouTube")
        print("  Install with: pip install pytchat")
    else:
        try:
            # 👇 CRÉATION DANS LE MAIN THREAD ICI 👇
            print("⏳ Initialisation Pytchat (Main Thread)...")
            live_chat = pytchat.create(video_id=YOUTUBE_VIDEO_ID)
            
            # On passe l'objet live_chat via "args"
            t_youtube = threading.Thread(target=youtube_worker, args=(live_chat,), daemon=True)
            t_youtube.start()
            
            time.sleep(2)
            youtube_connected = True
            print("✅ YouTube reader started")
        except Exception as e:
            print(f"❌ Cannot start YouTube: {e}")

# Mode démo si aucune connexion
if not twitch_connected and not youtube_connected:
    print("⚠️ Demo mode: use CTRL+SPACE to test")

# Afficher statut
print(f"\n📊 STATUS:")
print(f"  Twitch: {'✅ Connected' if twitch_connected else '❌ Disconnected'}")
print(f"  YouTube: {'✅ Connected' if youtube_connected else '❌ Disconnected'}")
if PLATFORM == "both":
    print(f"  Mode: Both platforms")
elif PLATFORM == "twitch":
    print(f"  Mode: Twitch only")
elif PLATFORM == "youtube":
    print(f"  Mode: YouTube only")

# ================= BOUCLE PRINCIPALE =================
running = True
race_active = True
finish_line_x = SCREEN_WIDTH - 50
winner = None
timer_reset = 0
chat_log_visual = []
road_offset = 0
fullscreen_mode = FULLSCREEN

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_F11:
                fullscreen_mode = not fullscreen_mode
                if fullscreen_mode:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
                else:
                    screen = pygame.display.set_mode((1024, 600))
                    SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 600
                finish_line_x = SCREEN_WIDTH - 50
            elif event.key == pygame.K_SPACE and pygame.key.get_mods() & pygame.KMOD_CTRL:
                for car in cars:
                    car.boost("DEBUG")
            elif event.key == pygame.K_m:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                    print("⏸️ Music paused")
                else:
                    pygame.mixer.music.unpause()
                    print("▶️ Music resumed")

    # Traitement messages
    processed = 0
    while not msg_queue.empty() and processed < 50:
        author, msg = msg_queue.get()
        processed += 1
        
        display_msg = f"{author[:18]}: {msg[:25]}"
        chat_log_visual.append(display_msg)
        if len(chat_log_visual) > 15:
            chat_log_visual.pop(0)

        if race_active:
            detected_country = detect_country_in_message(msg)
            
            if detected_country:
                for car in cars:
                    if car.id == detected_country:
                        car.boost(author)
                        player_tracker.add_vote(author)
                        
                        if snd_vroum: 
                            snd_vroum.play()
                        
                        print(f"🎯 Vote: {author} -> {car.name}")
                        break

    # Mises à jour
    if race_active:
        for car in cars:
            car.update()
            if car.x >= finish_line_x - 50:
                race_active = False
                car.wins += 1
                winner = car
                timer_reset = pygame.time.get_ticks()
                
                player_tracker.start_new_race()
                
                if snd_win: 
                    snd_win.play()
                
                print(f"🏆 VICTORY ! {car.name} wins !")
                break
    else:
        if pygame.time.get_ticks() - timer_reset > 5000:
            for car in cars: 
                car.reset()
            race_active = True
            winner = None

    # DESSIN
    draw_background(screen)
    
    road_offset = (road_offset + 2) % 40
    draw_road(screen, road_offset, cars, finish_line_x)
    
    draw_sidebar(screen, cars, player_tracker)
    
    for car in cars:
        car.draw(screen)
    
    draw_chat_panel(screen, chat_log_visual)
    
    if winner:
        draw_winner_overlay(screen, winner, timer_reset)
    
    # Instructions
    inst_txt = font_tiny.render("F11: Fullscreen • ESC: Quit • M: Music • CTRL+SPACE: Test", True, (200, 200, 200, 150))
    screen.blit(inst_txt, (15, SCREEN_HEIGHT - 25))
    
    # Info joueurs
    current_players = player_tracker.get_current_session_count()
    avg_players = player_tracker.get_average_players_per_race()
    
    players_info = font_tiny.render(f"🎮 {current_players} players • 📊 {avg_players:.1f} average/race", True, C_ACCENT2)
    screen.blit(players_info, (SCREEN_WIDTH - players_info.get_width() - 15, SCREEN_HEIGHT - 25))
    
    countries_info = font_tiny.render(f"🌍 {len(MAIN_COUNTRIES)} COUNTRIES + OTHERS", True, C_ACCENT)
    screen.blit(countries_info, (SCREEN_WIDTH//2 - countries_info.get_width()//2, 15))
    
    # Indicateur musique
    if music_loaded:
        if pygame.mixer.music.get_busy():
            music_indicator = font_tiny.render("🎵 Music ON", True, C_ACCENT2)
        else:
            music_indicator = font_tiny.render("🔇 Music OFF", True, (200, 100, 100))
        screen.blit(music_indicator, (SCREEN_WIDTH - music_indicator.get_width() - 15, 40))
    
    # Indicateur plateformes
    platform_text = ""
    if PLATFORM == "both":
        if twitch_connected and youtube_connected:
            platform_text = "🔴 Twitch + YouTube"
        elif twitch_connected:
            platform_text = "🔴 Twitch (YouTube disconnected)"
        elif youtube_connected:
            platform_text = "🔴 YouTube (Twitch disconnected)"
        else:
            platform_text = "⚠️ Demo mode (both disconnected)"
    elif PLATFORM == "twitch":
        platform_text = "🔴 Twitch" if twitch_connected else "⚠️ Twitch disconnected"
    elif PLATFORM == "youtube":
        platform_text = "🔴 YouTube" if youtube_connected else "⚠️ YouTube disconnected"
    
    platform_indicator = font_tiny.render(platform_text, True, (100, 65, 165) if twitch_connected or youtube_connected else (200, 100, 100))
    screen.blit(platform_indicator, (15, 40))
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()