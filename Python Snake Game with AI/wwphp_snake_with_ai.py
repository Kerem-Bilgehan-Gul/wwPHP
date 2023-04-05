"""
wwPHP.com Snake Game with AI
"""
# Kullanılan Kütüphaneler.
import pygame;
import sys;
import time;
import random;
import torch;
import numpy as np;
from collections import deque;
from model import Linear_QNet, QTrainer;
from enum import Enum;
from collections import namedtuple;
import os;

MAX_MEMORY = 500_000;
BATCH_SIZE = 100000;
LR = 0.001;
model = Linear_QNet(11, 256, 3);
n_games = 0;
epsilon = 0;
gamma = 0.9;
Bellek = deque(maxlen=MAX_MEMORY);
model.load_state_dict(torch.load('./model/model.pth'));

trainer = QTrainer(model, lr=LR, gamma=gamma);
Point = namedtuple('Point', 'x, y');

frame_iteration = 0;
# Oyun Alanı Boyutu
Pencere_Genislik  = 350;
Pencere_Yukseklik = 350;

"""
Kolay      = 20
Orta       = 40
Zor        = 60
Çok Zor    = 80
İnsan Üstü = 100
"""
Zorluk = 60;

# Hata Kontrolü
Hata = pygame.init();

if Hata[1] > 0:
	print('Bir Hata Meydana Geldi !');
	sys.exit(-1);
else:
	print('Oyun Başlatılıyor.');
	
# Oyun penceresini oluşturuyoruz.
pygame.display.set_caption('wwPHP.com Snake Game with AI'); # Oyun Başlığı
Oyun_Penceresi = pygame.display.set_mode((Pencere_Genislik, Pencere_Yukseklik));

# Renkler (R-G-B)
Siyah   = pygame.Color(0, 0, 0);
Beyaz   = pygame.Color(255, 255, 255);
Kirmizi = pygame.Color(255, 0, 0);
Yesil   = pygame.Color(0, 255, 0);
Mavi    = pygame.Color(0, 0, 255);

# FPS (saniyede gösterilen kare) kontrolcüsü
Fps_Kontrolcusu = pygame.time.Clock();

#Oyun Değişkenleri
Yilan_poz 	= [100, 50]; # Yılanın başlangıç pozisyonu
Yilan_Govde = [[100, 50], [100-10, 50], [100-(2*10), 50]];
#Yem pozisyonu için çerçeve sınırlarında rastgele bir değer oluşturuyoruz.
Yem_poz = [random.randrange(1, (Pencere_Genislik//10)) * 10, random.randrange(1, (Pencere_Yukseklik//10)) * 10]; 
Yem_durumu = True; #Yemin oluşturulma durumu

Yilan_Hareket_Yon = 'SAG';
Yilan_Yon_Degisiklik = Yilan_Hareket_Yon;

Skor = 0;

# Skor
def Skor_Goster(durum, renk, font, boyut):
    Skor_Font = pygame.font.SysFont(font, boyut);
    Skor_Alan = Skor_Font.render('Score : ' + str(Skor), True, renk);
    Skor_Rect = Skor_Alan.get_rect();
    if durum == 1:
        Skor_Rect.midtop = (Pencere_Genislik-200, 120);
    else:
        Skor_Rect.midtop = (Pencere_Genislik/10, Pencere_Yukseklik/1.25);
    Oyun_Penceresi.blit(Skor_Alan, Skor_Rect);
	
def Yazi_Goster(durum, renk, font, boyut):
    Skor_Font = pygame.font.SysFont(font, boyut);
    Skor_Alan = Skor_Font.render('wwPHP.com Snake Game with AI.', True, renk);
    Skor_Rect = Skor_Alan.get_rect();
    if durum == 1:
        Skor_Rect.midtop = (Pencere_Genislik-200, 100);
    else:
        Skor_Rect.midtop = (Pencere_Genislik/10, Pencere_Yukseklik/1.25);
    Oyun_Penceresi.blit(Skor_Alan, Skor_Rect);

#Oyun Kaybedilme Durumunda Çalışacak Fonksiyon
def Oyun_Kaybedildi():
    Fontt = pyfont.SysFont('Arial', 90);
    Oyun_Kaybedildi_Yuzey = Fontt.render('KAYBETTİN !', True, Kirmizi);
    Oyun_Kaybedildi_rect = Oyun_Kaybedildi_Yuzey.get_rect();
    Oyun_Kaybedildi_rect.midtop = (Pencere_Genislik/2, Pencere_Yukseklik/4);
    Oyun_Penceresi.fill(Siyah);
    Oyun_Penceresi.blit(Oyun_Kaybedildi_Yuzey, Oyun_Kaybedildi_rect);
    Skor_Goster(0, Kirmizi, 'times', 20);
    pydisplay.flip();
    time.sleep(3);
    pyquit();
    sys.exit();

def Carpisma_Tespiti(pt=None):
    global Yilan_poz;
    global Yilan_Govde;
    if pt is None:
        pt = Yilan_poz;
    # Eğer Yılan Pencere Kenarına Temas Ederse Oyunu Kaybettiriyoruz.
    if pt[0] < 0 or pt[0] > Pencere_Genislik-10:
        return True;
    if pt[1] < 0 or pt[1] > Pencere_Yukseklik-10:
        return True;

    # Eğer Yılan Kendi Gövdesi İle Temas Ederse Oyunu Kaybettiriyoruz.
    if pt in Yilan_Govde[1:]:
        return True;

    return False;

def Hareket_Et(action):
    global Yilan_Hareket_Yon;
    YON_DIR = ['SAG', 'ASAGI', 'SOL', 'YUKARI'];
    idx = YON_DIR.index(Yilan_Hareket_Yon);

    if np.array_equal(action, [1, 0, 0]):
        new_dir = YON_DIR[idx];
    elif np.array_equal(action, [0, 1, 0]):
        next_idx = (idx + 1) % 4;
        new_dir = YON_DIR[next_idx];
    else:
        next_idx = (idx - 1) % 4;
        new_dir = YON_DIR[next_idx];

    Yilan_Hareket_Yon = new_dir
    # Yılanı Duruma Göre Hareket Ettiriyoruz.
    if Yilan_Hareket_Yon == 'YUKARI':
        Yilan_poz[1] -= 10;
    if Yilan_Hareket_Yon == 'ASAGI':
        Yilan_poz[1] += 10;
    if Yilan_Hareket_Yon == 'SOL':
        Yilan_poz[0] -= 10;
    if Yilan_Hareket_Yon == 'SAG':
        Yilan_poz[0] += 10;

def Hareket_Adimi(action):
    global Yilan_poz;
    global Yem_poz;
    global Yilan_Govde;
    global Yem_durumu;
    global Skor;
    global frame_iteration;
    frame_iteration += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit();
            quit();
        
    Hareket_Et(action);
    Yilan_Govde.insert(0, list(Yilan_poz));
        
    Odul = 0;
    Oyun_Durumu = False;
    if Carpisma_Tespiti(Yilan_poz) or frame_iteration > 100*len(Yilan_Govde):
        Oyun_Durumu = True;
        Odul = -10;
        return Odul, Oyun_Durumu, Skor;
    
    if Yilan_poz[0] == Yem_poz[0] and Yilan_poz[1] == Yem_poz[1]: # Eğer Yılan Yem İle Temas Etmişse Skor 1 Attırılıyor.
        Skor += 1;
        Odul = 10;
        Yem_durumu = False;
    else:# Eğer Yılan Yem İle Temas Etmemişse Yilan_Govde List Nesnesinin En Son Parametresi Çıkarılarak Hareket Etmesi Sağlanıyor.
        Yilan_Govde.pop();

    # Yem_durumu Eğer False İse Yeni Bir Yem Oluşturuyoruz.
    if not Yem_durumu:
        Yem_poz = [random.randrange(1, (Pencere_Genislik//10)) * 10, random.randrange(1, (Pencere_Yukseklik//10)) * 10];
    Yem_durumu = True;
	
	# Yılanın Gövdesini Çiziyoruz
    Oyun_Penceresi.fill(Siyah);
    for pos in Yilan_Govde: # Yilan_Gove List Nesnesinde Bulunan Koordinatlara Göre Yılan Çiziliyor.
        pygame.draw.rect(Oyun_Penceresi, Mavi, pygame.Rect(pos[0], pos[1], 10, 10));

    # Yılanın Yemini Çiziyoruz
    pygame.draw.rect(Oyun_Penceresi, Yesil, pygame.Rect(Yem_poz[0], Yem_poz[1], 10, 10));
	
    Skor_Goster(1, Beyaz, 'consolas', 10);
    Yazi_Goster(1, Beyaz, 'consolas', 15);
    pygame.display.update();
	
    Fps_Kontrolcusu.tick(Zorluk);

    return Odul, Oyun_Durumu, Skor;
	
def Oyun_Verilerini_Al():
    Yilan = Yilan_Govde[0];
    point_l = Point(Yilan[0] - 20, Yilan[1])
    point_r = Point(Yilan[0] + 20, Yilan[1])
    point_u = Point(Yilan[0], Yilan[1] - 10)
    point_d = Point(Yilan[0], Yilan[1] + 10)
        
    dir_l = Yilan_Hareket_Yon == 'SOL'
    dir_r = Yilan_Hareket_Yon == 'SAG'
    dir_u = Yilan_Hareket_Yon == 'YUKARI'
    dir_d = Yilan_Hareket_Yon == 'ASAGI'

    state = [
        # Riskler
        (dir_r and Carpisma_Tespiti(point_r)) or 
        (dir_l and Carpisma_Tespiti(point_l)) or 
        (dir_u and Carpisma_Tespiti(point_u)) or 
        (dir_d and Carpisma_Tespiti(point_d)),

        # Sag Taraftaki Riskler
        (dir_u and Carpisma_Tespiti(point_r)) or 
        (dir_d and Carpisma_Tespiti(point_l)) or 
        (dir_l and Carpisma_Tespiti(point_u)) or 
        (dir_r and Carpisma_Tespiti(point_d)),

        # Sol Taraftaki Riskler
        (dir_d and Carpisma_Tespiti(point_r)) or 
        (dir_u and Carpisma_Tespiti(point_l)) or 
        (dir_r and Carpisma_Tespiti(point_u)) or 
        (dir_l and Carpisma_Tespiti(point_d)),
        
        # Hareket Emirleri
        dir_l,
        dir_r,
        dir_u,
        dir_d,
            
        # Yem Konumu
        Yem_poz[0] < Yilan[0],
        Yem_poz[0] > Yilan[0],
        Yem_poz[1] < Yilan[1],
        Yem_poz[1] > Yilan[1]
    ];

    return np.array(state, dtype=int);

def Bellege_Kayit_Et(state, action, reward, next_state, done):
    Bellek.append((state, action, reward, next_state, done));

def train_long_memory():
    if len(Bellek) > BATCH_SIZE:
        mini_sample = random.sample(Bellek, BATCH_SIZE);
    else:
        mini_sample = Bellek;

    states, actions, rewards, next_states, dones = zip(*mini_sample);
    trainer.train_step(states, actions, rewards, next_states, dones);

def train_short_memory(state, action, reward, next_state, done):
    trainer.train_step(state, action, reward, next_state, done);

def get_action(state):
    epsilon = 80 - n_games;
    Son_Hareket = [0,0,0];
    if random.randint(0, 200) < epsilon:
        move = random.randint(0, 2);
        Son_Hareket[move] = 1;
    else:
        state0 = torch.tensor(state, dtype=torch.float);
        prediction = model(state0);
        move = torch.argmax(prediction).item();
    Son_Hareket[move] = 1;

    return Son_Hareket;

def Yeniden_Baslat():
    global Yilan_poz;
    global Yilan_Govde;
    global Yem_poz;
    global Yem_durumu;
    global Yilan_Hareket_Yon;
    global Yilan_Yon_Degisiklik;
    global frame_iteration;
    #Oyun Değişkenleri
    Yilan_poz 	= [100, 50]; # Yılanın başlangıç pozisyonu
    Yilan_Govde = [[100, 50], [100-10, 50], [100-(2*10), 50]];
    #Yem pozisyonu için çerçeve sınırlarında rastgele bir değer oluşturuyoruz.
    Yem_poz = [random.randrange(1, (Pencere_Genislik//10)) * 10, random.randrange(1, (Pencere_Yukseklik//10)) * 10]; 
    Yem_durumu = False; #Yemin oluşturulma durumu
    frame_iteration = 0
    Yilan_Hareket_Yon = 'SAG';
    Yilan_Yon_Degisiklik = Yilan_Hareket_Yon;

total_score = 0;
record = 0;
file_exists = os.path.exists('last_rec.txt');
if file_exists:
    with open("last_rec.txt", "r+") as f:
        record = int(f.read());

while True:
    Eski_Hareket = Oyun_Verilerini_Al();
    Son_Hareket = get_action(Eski_Hareket);
    reward, done, score = Hareket_Adimi(Son_Hareket);
    state_new = Oyun_Verilerini_Al();
    train_short_memory(Eski_Hareket, Son_Hareket, reward, state_new, done)
    Bellege_Kayit_Et(Eski_Hareket, Son_Hareket, reward, state_new, done)
    if done:
        Yeniden_Baslat();
        Skor = 0;
        n_games += 1;
        train_long_memory();
    if score > record:
        print('Save:', score, 'Rec:', record);
        record = score;
        model.save();
        with open("last_rec.txt", "r+") as f:
            f.write(str(record));

	