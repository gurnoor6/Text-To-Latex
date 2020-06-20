from PIL import Image
import pytesseract
import argparse
import cv2
import os

from .makeRectangle import makeRectangle

def getImageText(image_name):
	print("image_name= ",image_name)
	images_list = makeRectangle(image_name)
	full_text=""
	for image in images_list:
		gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
		gray = cv2.medianBlur(gray,3)

		#save the grayscale blurred image temporarily in the disk so that we can apply ocr to it
		filename = "temp.png".format(os.getpid())
		cv2.imwrite(filename,gray)

		text = pytesseract.image_to_string(Image.open(filename))
		os.remove(filename)
		full_text+=text
	return full_text

if __name__=='__main__':
	# images_list = makeRectangle('im.png')
	# for image in images_list:
	# 	cv2.imshow("image",image)
	# 	cv2.waitKey(0)
	# 	print(getText(image))

	image_name = "../media/images/im.png"
	t = getImageText(image_name)
	print(t)
