import cv2
import numpy as np
from PIL import ImageGrab
import pyautogui
import time

while(True):
	try:
		#Anlik olarak ekran goruntumuzu sagdan 40 pixel iceride ve ustten 40 pixel 
		# asagida olmak uzere 600x600 boyutunda aliyoruz.
		EkranGoruntusu 	=  np.array(ImageGrab.grab(bbox=(40,40,640,640)));
		#Yakalancak Nesne olarak ordek gorselimizi belirtiyoruz.
		DuckDataSet 	= cv2.imread('duck.png');
		# SIFT Dedektorumuzu Baslatiyoruz
		sift = cv2.xfeatures2d.SIFT_create();
		# SIFT uzerinde Ekrangroruntumuz ve ordek resmimizdeki karsilastirilabilecek kilit noktalari buluyoruz.
		kp1, des1 = sift.detectAndCompute(EkranGoruntusu,None);
		kp2, des2 = sift.detectAndCompute(DuckDataSet,None);
		# FLANN parametrelerimizi tanimliyoruz.
		FLANN_INDEX_KDTREE 	= 1;
		index_params 		= dict(algorithm = FLANN_INDEX_KDTREE, trees = 5);
		search_params 		= dict(checks=50);
		flann				= cv2.FlannBasedMatcher(index_params,search_params);
		matches 			= flann.knnMatch(np.float32(des1),np.float32(des2),k=2);
		# Iyi olan eslesmeler icin maske olusturuyoruz.
		matchesMask = [[0,0] for i in range(len(matches))]
		# Tespit edilen nesneleri vurmak icin degiskenlerimizi olusturuyoruz.
		Y_Koor 		= 0;
		X_Koor 		= 0;
		olasilik 	= 0;
		for i,(m,n) in enumerate(matches):
			if m.distance < 0.5*n.distance:
				matchesMask[i]=[1,0];
				point = kp1[m.queryIdx].pt;
				X_Koor 			= int(point[0]); # X koordinatindaki noktamiz.
				Y_Koor 			= int(point[1]); # Y koordinatindaki noktamiz.
				olasilik 		= olasilik + 1; # Her eslesen nokta icin olasiligimizi 1 arttiriyoruz.
				if(olasilik > 3): # Eger 1 nesne icin 3 adet esleme varsa nesnenin bulundugu koordinata islem uyguluyoruz.
					pyautogui.click(x=X_Koor, y=Y_Koor); # Nesnenin bulundugu kooardinata mousemizi tiklatiyoruz.
					olasilik = 0; # Olasiligi sifirliyoruz.
		draw_params = dict(
				singlePointColor = (255,0,0),
				matchesMask = matchesMask,
				flags = cv2.DrawMatchesFlags_DEFAULT);
		# KNN eslesmelerimizi ekranda gosteriyoruz.
		KNNCiz = cv2.drawMatchesKnn(EkranGoruntusu,kp1,DuckDataSet,kp2,matches,None,**draw_params);
		cv2.imshow('KNN Duck Shot wwphp',KNNCiz);
		# Klavye uzerinde q tusuna basinca KNN pencerimizin kapatilmasini sagliyoruz.
		if cv2.waitKey(27) & 0xFF == ord('q'): 
			cv2.destroyAllWindows();
			break;
	except Exception as e:
		print(e);
		pass;