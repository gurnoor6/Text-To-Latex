from skimage.io import imread
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
img = rgb2gray(imread("handwritten1.jpg"))

from skimage.filters import sobel
sobel_image = sobel(img)
# plt.figure(figsize=(8,8))
# plt.axis("off")
# plt.imshow(sobel_image, cmap="gray")
# plt.show()

from skimage.filters import sobel
import numpy as np
def horizontal_projections(sobel_image):
    #threshold the image.
    sum_of_rows = []
    for row in range(sobel_image.shape[0]-1):
        sum_of_rows.append(np.sum(sobel_image[row,:]))
    
    return sum_of_rows
sobel_image = sobel(img)
hpp = horizontal_projections(sobel_image)
plt.plot(hpp)
plt.show()

def find_peak_regions(hpp, divider=2):
    threshold = (np.max(hpp)-np.min(hpp))/divider
    peaks = []
    peaks_index = []
    for i, hppv in enumerate(hpp):
        if hppv < threshold:
            peaks.append([i, hppv])
    return peaks

peaks = find_peak_regions(hpp)

peaks_index = np.array(peaks)[:,0].astype(int)

segmented_img = np.copy(img)
r,c = segmented_img.shape
for ri in range(r):
    if ri in peaks_index:
        segmented_img[ri, :] = 0
        
plt.figure(figsize=(20,20))
plt.imshow(segmented_img, cmap="gray")
plt.show()

# def get_road_block_regions(nmap):
#     road_blocks = []
#     needtobreak = False
    
#     for col in range(nmap.shape[1]):
#         start = col
#         end = col+20
#         if end > nmap.shape[1]-1:
#             end = nmap.shape[1]-1
#             needtobreak = True
#         if path_exists(nmap[:, start:end]) == False:
#             road_blocks.append(col)
#         if needtobreak == True:
#             break
            
#     return road_blocks