from tkinter import *
import random
import time
from PIL import ImageTk

class Race:
	def __init__(self, Araba, Dubalar, canvas, Arkaplan):
		self.canvas 	= canvas
		self.Araba 		= Araba
		self.Dubalar 	= Dubalar
		self.ArkaPlan 	= Arkaplan

		self.idAraba	= canvas.create_image(85, 400, image = self.Araba)
		
		self.canvas.bind_all('<KeyPress-Right>', self.Sag)
		self.canvas.bind_all('<KeyPress-Left>', self.Sol)
		
		self.x = 0 # X eksenindeki baslangic hizimiz
		self.y = 0 # Y eksenindeki baslangic hizimiz
		
	def Ciz(self):
		self.canvas.move(self.idAraba, self.x, self.y) 
		Koordinat = self.canvas.coords(self.idAraba)
		#print(Koordinat)
		if Koordinat[0] == 280 or Koordinat[0] == 20:
			self.x = 0
		if self.Dubas(Koordinat) == True: 
			self.canvas.move(self.ArkaPlan,0,0)
	
	def Durum(self): # Aracımızın koordinatının herhangi bir dubanın koordinatı ile eşleşip eşleşmediğini kontrol ediyoruz.
		Koordinat = self.canvas.coords(self.idAraba)
		if self.Dubas(Koordinat) == True: # Eğer eşleşiyor ise 1 değerini döndürüyoruz.
			return 1
	
	def Fin(self):
		Koordinat = self.canvas.coords(self.ArkaPlan)
		return Koordinat
	
	def Sag(self, event): #Sağ yön tuşuna basınca X eksninde 1 pixel sağa doğru hareket ettiriyoruz.
		Koordinat = self.canvas.coords(self.idAraba)
		if Koordinat[0] != 280:#Penecereden taşmaması için x eksenindeki koordinatımız 280 olmadığı sürece bu işlemi yapmasını söylüyoruz.
			self.x = 1
		
	def Sol(self, event): #Sol yön tuşuna basınca X eksninde 1 pixel sola doğru hareket ettiriyoruz.
		Koordinat = self.canvas.coords(self.idAraba)
		if Koordinat[0] != 20:#Penecereden taşmaması için x eksenindeki koordinatımız 20 olmadığı sürece bu işlemi yapmasını söylüyoruz.
			self.x = -1
		
	def Dubas(self, pos):
		self.DubaKoor = {}
		for ai in range(0, 50):
			self.DubaKoor[ai] = self.canvas.coords(self.Dubalar.idDuba[ai])
			if pos[0] > self.DubaKoor[ai][0] - 10 and pos[0] < self.DubaKoor[ai][0] + 10:
				if pos[1] - 30 < self.DubaKoor[ai][1] + 10 and 400 > self.DubaKoor[ai][1] + 10:
					return True

class Duba:
	def __init__(self, canvas, BoruResim):
		self.idDuba = {} # Birden fazla duba oluşturacağımız için bir döngünün içinde dubalarımızı rastgele koordinatlarda oluşturuyoruz.
		for ai in range(0, 50):
			startsX = float(random.randint(20,280))
			startsY = float(random.randint(-5000,50))
			self.idDuba[ai] = canvas.create_image(startsX, startsY, image = BoruResim)
		
	def Ciz(self):
		for ai in range(0, 50):
			canvas.move(self.idDuba[ai],0, 1); #Dubalarımızı arkaplan ile beraber y ekseninde 1 pixel hareket ettiriyoruz.
			# Böylece arkaplanla beraber hareket ediyormuş gibi gözüküyor.


tk = Tk()
tk.title('wwPHP Race') # Oyun Pencere Başlığımız.
canvas = Canvas(tk, width=301, height=500, bd=0, highlightthickness=0) # Oyunumuzun pencere boyutu


ArabaResim 		= PhotoImage(file = 'car.png') #Araba Resmimiz
ArkaPlan 		= ImageTk.PhotoImage(file = "racemap.png") #Arkaplan resmimiz
idArkaPlan		= canvas.create_image(0, -4500, image = ArkaPlan, anchor = NW)  #Ekranimizin arkaplanini belirliyoruz
canvas.pack()
tk.update()
DubaResim		= PhotoImage(file = 'duba.png') #Duba Resmimiz
Duba			= Duba(canvas, DubaResim) # Duba sınıfımızı çağırıyoruz.
Race 			= Race(ArabaResim, Duba, canvas, idArkaPlan)#Ufo Nesnemize Gerekli Parametreleri Yolluyoruz.

OyunDurumu = 0; #0 Oyun Devam Ediyor, 1 Dubaya Çarptı, 2 Oyun Bitti
while 1: # Sonsuz Döngümüzü Başlatıyoruz.
	if OyunDurumu == 0: # OyunDurumu değişkeni 0 olduğu sürece gerçekleşecek eylemler.
		canvas.move(idArkaPlan,0, 1); # Arka Planımızı y ekseninde 1 pixel hareket ettiriyoruz. Sonsuz döngü içerisinde olduğu için bu işlem süreklilik olarak gözükecektir.
		Duba.Ciz(); # Dubalarımızı Çiziyoruz.
		Race.Ciz();
	if Race.Durum() == 1: # Eğer dönen değer 1 ise duba ile aracımızın koordinatının işleştiği anlamına geliyor.
		OyunDurumu = 1;
		canvas.create_text(150, 200, text="Kaybettin", font=("Arial", 20), fill="red")
	if Race.Fin()[1] > -250: # Eğer hareketli arkaplanımızın koordinatı -250 yi geçmiş ise oyunun bittiğini ifade ediyoruz.
		OyunDurumu = 2;
		canvas.create_text(150, 200, text="Oyunu Kazandın !", font=("Arial", 25), fill="green")
	tk.update_idletasks()
	tk.update()
	time.sleep(0.005)