import cv2
import numpy as np
import xml.etree.ElementTree as ET


tree = ET.parse('file.xml')
root = tree.getroot()
print(root.tag)

x=[]
y=[]
w=[]
h=[]
for tgdrct in root.iter('taggedRectangle'):
	x.append(tgdrct.get('x'))
	y.append(tgdrct.get('y'))
	w.append(tgdrct.get('width'))
	h.append(tgdrct.get('height'))

x = np.asarray(x).astype(float).astype(int)
y = np.asarray(y).astype(float).astype(int)
w = np.asarray(w).astype(float).astype(int)
h = np.asarray(h).astype(float).astype(int)

xl = x
yl = y
xr = x+w
yr = y+h





img = cv2.imread("IMG_1261.JPG")
for i in range(11):
	cv2.rectangle(img,(xl[i],yl[i]),(xr[i],yr[i]),(255,0,0),3)	#(311,294),(37,488)
print(img.shape)
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()