import csv
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow.keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Dropout,Flatten
import cv2



##### Above part constitutes importing libraries stuff #####

f = open('words.csv')
csv_f = csv.reader(f)
file = open('newfile.csv','w',newline='')
writer = csv.writer(file)

#1161 rows
rows = []
for row in csv_f:
	rows.append(row)

for i in range(1160):
	if(rows[i+1][0]==''):
		rows[i+1][0]=rows[i][0]
		rows[i+1][1]=rows[i][1]
		rows[i+1][2]=rows[i][2]

writer.writerows(rows)

##### We are done till making of a clean file ######
r_n = open('newfile.csv')
r_newfile = csv.reader(r_n)

imgs = []
details = []
indices = [1,2,4,5,6,7,8,9,11]
for row in r_newfile:
	imgs.append(row[0])
	temp_row = []
	for i in indices:
		temp_row.append(row[i])
	details.append(temp_row)

imgs = imgs[1:]
#1144 images
details = details[1:]

##### x and y are ready to be set #####
x=[]
for item in imgs:
	img = cv2.imread(item,0)
	x.append(img)
y = details
##### now we turn them into arrays #####

x = np.asarray(x)
y = np.asarray(y)

##### x and y are now our arrays #####

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2)
labels_train = y_train[:,-1]
labels_test = y_test[:,-1]
#x_train- 915, x_test-229
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /=255
x_test/=255
print(x_test[0])
# cv2.imshow("img",x_train[0])
# cv2.waitKey(0)
# cv2.destroyAllWindows()





































