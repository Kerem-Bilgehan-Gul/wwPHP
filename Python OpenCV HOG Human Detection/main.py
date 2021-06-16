# Gerekli Kutuphanelerimizi Ekliyoruz
import cv2
import numpy as np
import imutils
from imutils.object_detection import non_max_suppression


# Histogram of Oriented Gradients Dedektorumuzu Tanimliyoruz
HOGCV = cv2.HOGDescriptor()
HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Insan Tanimlamasi Yapacagimiz Resmimiz
Resim = cv2.imread("fr.jpg");

ResimGenislik = Resim.shape[1]
EnYuksekGenislik = 800

# Eger Resim Genisligi En Yuksek Genislikten Fazla Ise,
# Resim Boyutumuzu En Yuksek Genislige Gore Boyutlandiriyoruz.
if ResimGenislik > EnYuksekGenislik:
    Resim = imutils.resize(Resim, width=EnYuksekGenislik)

# Resimde Bulunan Insanlar veya Yayalarin Koordinatlarini Belirliyoruz.
Insan, weights = HOGCV.detectMultiScale(Resim, winStride=(4, 4), padding=(8, 8), scale=1.2)
# Belirledigimiz Koordinatlari Numpy Array'a Ceviriyoruz.
Insan = np.array([[x, y, x + w, y + h] for (x, y, w, h) in Insan])

# Ust uste binen kutucuklari tek bir genel kutucuk haline getirmek icin,
# non_max_suppression fonksiyonunu kullaniyoruz.
Insan = non_max_suppression(Insan, probs=None, overlapThresh=0.6)

print(Insan) # Resim uzerinde tespit edilen her insanin koordinatlarini konsol ekranina yazdiriyoruz.

Say = 0

#  Belirlenen koordinatlari isaretliyoruz.
for x, y, w, h in Insan:
    cv2.rectangle(Resim, (x, y), (w, h), (0, 0, 100), 2)
    cv2.rectangle(Resim, (x, y - 20), (w,y), (0, 0, 255), -1)
    cv2.putText(Resim, f'Zombi{Say}', (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    Say += 1

cv2.imshow('wwPHP.com Human Detection', Resim)
cv2.waitKey(0)
cv2.destroyAllWindows()
