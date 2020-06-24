import cv2
import xmlparse

images_data = xmlparse.getRectLocation()

for img_data in images_data:
	location = img_data[0]
	x1 = (img_data[1])
	y1 = img_data[2]
	x2 =(img_data[3])
	y2 =img_data[4]
	img = cv2.imread(location,1)
	print(x1,y1,x2,y2)
	cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,0),2)
	# cv2.imwrite("myimg.jpg",img)
	cv2.imshow("lalala",img)
	cv2.waitKey(0)