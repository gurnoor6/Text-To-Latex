#Crops out the rego=ions of text in the picture and returns them as a list
#Return type -List

import numpy as np
import cv2
import argparse
import time
from imutils.object_detection import non_max_suppression

def makeRectangle(image_path,east ='frozen_east_text_detection.pb',min_confidence=0.5,width=320,height=320):

	image = cv2.imread(image_path)
	orig = image.copy()		#copy the original image because we need to resize as well
	(H,W) = image.shape[:2]

	(newH,newW)= (width,height)
	rW = W/float(newW)
	rH = H/float(newH)

	image = cv2.resize(image,(newW,newH))
	(H,W) = image.shape[:2]

	layerNames = ["feature_fusion/Conv_7/Sigmoid","feature_fusion/concat_3"]		#These layers give us geometry and scores array as explained next

	#Loads the cv2 Neural Network
	net = cv2.dnn.readNet(east)

	#Blob is basically the same image but sort of normalised. In some cases, it is also divided by sigma. that is taken care in scale factor which is 1/sigma.
	#We subtract the (123.68,...) values from the RGB clour channels of our image. 
	# By default, open cv swaps the RB channels compared to what is required by tf. So we swap RB
	# crop crops our image to give the center portion. generally kept to false
	blob = cv2.dnn.blobFromImage(image,1.0,(W,H),(123.68,116.78,103.94),swapRB=True,crop=False)
	net.setInput(blob)

	#Scores has a shape (1,1,width/4=80,height/4=80) The image is sort of squished basically. For each pixel then, we have a value associated
	# That value is called the score for that pixel (it represents the probability to find text (don't know where))
	#Geometry has shape (1,5,80,80). 5 refers to the 5 data values present here and 80,80 refers that there are 5 parameters assoociated with each pixel
	(scores,geometry) = net.forward(layerNames)

	#we can think it of as number of pixels in the image (dimensions of image basically)
	(numRows,numCols) = scores.shape[2:4]

	#rects stores the coordinates of bounding boxes of rectangles and confidences stores the corresponsing probability of being a bounding box
	rects=[]
	confidences =[]


	#We iterate over each column
	for y in range(0,numRows):
		#ScoresData refers to the probability of finding text
		scoresData = scores[0,0,y]

		#Don't really know what the other terms represnt
		xData0 = geometry[0,0,y]
		xData1 = geometry[0,1,y]
		xData2 = geometry[0,2,y]
		xData3 = geometry[0,3,y]
		anglesData = geometry[0,4,y]

		#x is basicallu the height pixel value. 
		for x in range(0,numCols):
			if scoresData[x]<min_confidence:
				continue

			#multiplying by 4 because our original image has been resized by factor of 4 due ti input i =n neral network
			(offsetX,offsetY) = (x*4.0,y*4.0)

			angle = anglesData[x]
			cos = np.cos(angle)
			sin = np.sin(angle)

			#self explanatory terms ahead. How these relations arrived- I don't know
			h = xData0[x]+xData2[x]
			w = xData1[x]+ xData3[x]
			endX = int(offsetX + (cos*xData1[x]) + (sin*xData2[x]))
			endY = int(offsetY - (sin*xData1[x]) + (cos*xData2[x]))
			startX = int(endX-w)
			startY = int(endY-h)
			rects.append((startX,startY,endX,endY))
			confidences.append(scoresData[x])

	#non max suppression basically takes the rectangles, figures out if they all are pointing to the same region and then use the next parameter to chose only one rectang;e
	# As a substitute for a lot of them.
	boxes = non_max_suppression(np.array(rects),probs = confidences)

	cropped_imgs = []
	for (startX, startY, endX, endY) in boxes:
		startX = int(startX*rW)
		startY = int(startY*rH)
		endX = int(endX*rW)
		endY = int(endY*rH)
		#We do not make the rectangle here because it interferes with the text detection in c=ocr.py
		# cv2.rectangle(orig, (startX,startY),(endX,endY),(0,255,0),2)
		to_be_cropped = orig.copy()
		cropped = to_be_cropped[startY-20:endY+20,startX+10:endX-10]
		cropped_imgs.append(cropped)

	return cropped_imgs


if __name__=='__main__':
	cv2.imshow("iamge",makeRectangle('abc.jpg')[0])
	cv2.waitKey(0)

