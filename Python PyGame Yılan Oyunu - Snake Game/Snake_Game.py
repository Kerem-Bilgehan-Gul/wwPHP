"""
wwPHP.com Snake Game
"""
# Kullanılan Kütüphaneler.
import pygame;
import sys;
import time;
import random;

# Oyun Alanı Boyutu
Pencere_Genislik  = 500;
Pencere_Yukseklik = 500;

"""
Kolay      = 20
Orta       = 40
Zor        = 60
Çok Zor    = 80
İnsan Üstü = 100
"""
Zorluk = 20;

# Hata Kontrolü
Hata = pygame.init();

if Hata[1] > 0:
	print('Bir Hata Meydana Geldi !');
	sys.exit(-1);
else:
	print('Oyun Başlatılıyor.');
	
# Oyun penceresini oluşturuyoruz.
pygame.display.set_caption('wwPHP Snake Game'); # Oyun Başlığı
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
    Skor_Alan = Skor_Font.render('Skor : ' + str(Skor), True, renk);
    Skor_Rect = Skor_Alan.get_rect();
    if durum == 1:
        Skor_Rect.midtop = (Pencere_Genislik/10, 15);
    else:
        Skor_Rect.midtop = (Pencere_Genislik/2, Pencere_Yukseklik/1.25);
    Oyun_Penceresi.blit(Skor_Alan, Skor_Rect);

#Oyun Kaybedilme Durumunda Çalışacak Fonksiyon
def Oyun_Kaybedildi():
    Fontt = pygame.font.SysFont('Arial', 90);
    Oyun_Kaybedildi_Yuzey = Fontt.render('KAYBETTİN !', True, Kirmizi);
    Oyun_Kaybedildi_rect = Oyun_Kaybedildi_Yuzey.get_rect();
    Oyun_Kaybedildi_rect.midtop = (Pencere_Genislik/2, Pencere_Yukseklik/4);
    Oyun_Penceresi.fill(Siyah);
    Oyun_Penceresi.blit(Oyun_Kaybedildi_Yuzey, Oyun_Kaybedildi_rect);
    Skor_Goster(0, Kirmizi, 'times', 20);
    pygame.display.flip();
    time.sleep(3);
    pygame.quit();
    sys.exit();


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit();
            sys.exit();
        # Bir Tuşa Her Basıldığında :
        elif event.type == pygame.KEYDOWN:
            # W -> Yukarı; S -> Aşağı; A -> Sola; D -> Sağa
            if event.key == pygame.K_UP or event.key == ord('w'):
                Yilan_Yon_Degisiklik = 'YUKARI';
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                Yilan_Yon_Degisiklik = 'ASAGI';
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                Yilan_Yon_Degisiklik = 'SOL';
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                Yilan_Yon_Degisiklik = 'SAG';
            # Esc Tuşuna Basılırsa Oyun Bitiriliyor.
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT));

    # Eğer Yılan Yukarı Gidiyorsa, Aşağıya - Aşağıda Gidiyorsa, Yukarıya Gidemez !
	# Bu Durum Sağ ve Sol Hareket Yönleri İçerisinde Geçerli.
    if Yilan_Yon_Degisiklik == 'YUKARI' and Yilan_Hareket_Yon != 'ASAGI':
        Yilan_Hareket_Yon = 'YUKARI';
    if Yilan_Yon_Degisiklik == 'ASAGI' and Yilan_Hareket_Yon != 'YUKARI':
        Yilan_Hareket_Yon = 'ASAGI';
    if Yilan_Yon_Degisiklik == 'SOL' and Yilan_Hareket_Yon != 'SAG':
        Yilan_Hareket_Yon = 'SOL';
    if Yilan_Yon_Degisiklik == 'SAG' and Yilan_Hareket_Yon != 'SOL':
        Yilan_Hareket_Yon = 'SAG';

    # Yılanı Duruma Göre Hareket Ettiriyoruz.
    if Yilan_Hareket_Yon == 'YUKARI':
        Yilan_poz[1] -= 10;
    if Yilan_Hareket_Yon == 'ASAGI':
        Yilan_poz[1] += 10;
    if Yilan_Hareket_Yon == 'SOL':
        Yilan_poz[0] -= 10;
    if Yilan_Hareket_Yon == 'SAG':
        Yilan_poz[0] += 10;

    # Yılan Her Yem Yediğinde Sokoru 1 Artırıyoruz ve Yeni Bir yem Oluşması İçin Yem_durumu nu False yapıyoruz.
    Yilan_Govde.insert(0, list(Yilan_poz)); # Yilan_Govde List Nesnesinin 0. Parametresine Ekleme Yapılıyor.
    if Yilan_poz[0] == Yem_poz[0] and Yilan_poz[1] == Yem_poz[1]: # Eğer Yılan Yem İle Temas Etmişse Skor 1 Attırılıyor.
        Skor += 1;
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

    # Eğer Yılan Pencere Kenarına Temas Ederse Oyunu Kaybettiriyoruz.
    if Yilan_poz[0] < 0 or Yilan_poz[0] > Pencere_Genislik-10:
        Oyun_Kaybedildi();
    if Yilan_poz[1] < 0 or Yilan_poz[1] > Pencere_Yukseklik-10:
        Oyun_Kaybedildi();

    # Eğer Yılan Kendi Gövdesi İle Temas Ederse Oyunu Kaybettiriyoruz.
    for block in Yilan_Govde[1:]:
        if Yilan_poz[0] == block[0] and Yilan_poz[1] == block[1]:
            Oyun_Kaybedildi();

    Skor_Goster(1, Beyaz, 'consolas', 20);

    pygame.display.update();
    Fps_Kontrolcusu.tick(Zorluk);