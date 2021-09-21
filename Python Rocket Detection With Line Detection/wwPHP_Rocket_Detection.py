# wwPHP.com Rocket Detection with Line Detection.
import cv2;
import numpy as np;
import math;
import time;

cap = cv2.VideoCapture('wwPHPRocketDetection.mp4'); # Read Video File.

while(cap.isOpened()):
	# Capture Frame
	ret, frame = cap.read();
	if ret == True:
		img = frame;
		# Convert the frame to gray scale.
		gray 			= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY);
		# Convert the gray frame to blur 
		kernel_size 	= 5;
		blur_gray 		= cv2.GaussianBlur(gray,(kernel_size, kernel_size),0);
		low_threshold 	= 50;
		high_threshold 	= 150;
		edges 			= cv2.Canny(blur_gray, low_threshold, high_threshold);
		line_image = np.copy(img) * 0;  # Creating a blank to draw lines on
		# Detect Lines.
		lines = cv2.HoughLinesP(edges, 1, (np.pi / 180), 15, np.array([]),	50, 20);

		RocketLineCount = 0;  #Detected Line Counts.
		RocketInfoArray = []; #This array in detected rocket lines information.
		RocketSpeed 	= 0;  #Rocket Speed varible.
		yCoorArray 		= []; #Y Coordinates Array.
		RocketDegree 	= 1;  #Rockets Degrees Varible.
		PixelsOneMeter 	= 50; #How much pixel in one meter ?
		
		for line in lines:
			for x1,y1,x2,y2 in line:
			#I give space around the edges.
			#Because my video has bad lines.
				if x1 > 80 and x2 < 1000:
					if y1 < 400 and y2 < 400:
						RocketInfoArray.append([RocketLineCount]);
						Radians = math.atan2(y2-y1, x2-x1);
						Degress = math.degrees(Radians); #I calculate rocket degree with this parameters.
						#I'm adding the rocket information to the array.
						RocketInfoArray[RocketLineCount].append(str(y1)+"-"+str(y2)+"-"+str(x1)+"-"+str(x2)+"-"+str(Degress)+"-"+str(time.time()));
						#I increase by 1 for each line.
						RocketLineCount = RocketLineCount + 1;
						yCoorArray.append(y1);
						RocketDegree = RocketDegree + Degress;
						cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),4);
						MaxTime = float(RocketInfoArray[yCoorArray.index(max(yCoorArray))][1].split("-")[5]);
						MinTime = float(RocketInfoArray[yCoorArray.index(min(yCoorArray))][1].split("-")[5]);
						# I Calculate Rocket Speed :
						if MaxTime != 0.0 and MinTime != 0.0 and (MaxTime-MinTime) != 0.0:
							RocketTime = MaxTime-MinTime;
							Speed = ((max(yCoorArray)-min(yCoorArray))/PixelsOneMeter)*(1.0/RocketTime);
							if Speed > 0.0 :
								RocketSpeed = RocketSpeed + Speed;
		# I Calculate Rocket Speed and Degree Average.						
		RocketsAverageSpeed = int(RocketSpeed/(RocketLineCount+1));
		RocketsAverageDegree = int(RocketDegree/(RocketLineCount+1));
		if RocketsAverageSpeed > 50 and RocketsAverageDegree > 10:
			print("Rockets Average Speed : " + str(RocketsAverageSpeed)+" km");
			print("Rockets Average Degree : " + str(RocketsAverageDegree));
			cv2.putText(img, "Rocket Detected !", (150, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (139,35,3), 2);
			
		lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0);
		cv2.imshow("mask",lines_edges);

	if cv2.waitKey(25) & 0xFF == ord('q'):
		break;