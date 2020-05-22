import cv2
import numpy as np

image ="img.jpg"

img = cv2.imread(image,0)
# img = cv2.GaussianBlur(img, (5,5),0)
# img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,11,2)
# kernel = np.ones((5,5),np.uint8)

kernel = [[-1,-1,-1],[2,2,2],[-1,-1,-1]]
print(kernel)
kernel = np.asarray(kernel,np.int8)
print(kernel)
# kernel = np.ones((5,5),np.uint8)
kernel = kernel.astype('float32')
kernel*=4
# print(kernel)
img = cv2.filter2D(img,0,kernel=kernel)

kernel = [[-1,2,-1],[-1,2,-1],[-1,2,-1]]
kernel = np.asarray(kernel,np.int8)
kernel*=1
img = cv2.filter2D(img,0,kernel=kernel)

# for i in range(4):
img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,3,5)
# kernel = np.ones((3,3),np.uint8)
# img = cv2.erode(img,kernel,iterations=1)

# img = cv2.dilate(img,kernel,iterations=200)
cv2.imshow("img",img)
cv2.waitKey(0)