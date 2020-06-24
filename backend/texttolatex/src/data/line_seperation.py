from skimage.io import imread
from skimage.color import rgb2gray
from skimage.filters import sobel
from skimage.filters import threshold_otsu
import matplotlib.pyplot as plt
import numpy as np
from heapq import *
import cv2

# img = rgb2gray(imread("handwritten2.jpg"))

# sobel_image = sobel(img)
# plt.figure(figsize=(8,8))
# plt.axis("off")
# plt.imshow(sobel_image, cmap="gray")
# plt.show()

# sobel_image = sobel(img)
# hpp = horizontal_projections(sobel_image)
# plt.plot(hpp)
# plt.show()

def find_peak_indices(image, divider=2):
    '''
        Input: image (as numpy array)
        Output: Peak indices horizontal projections 
    '''
    sobel_image = sobel(image)
    hpp = np.sum(sobel_image, axis = 1)

    threshold = (np.max(hpp)-np.min(hpp))/divider
    peaks = []
    for i, hppv in enumerate(hpp):
        if hppv < threshold:
            peaks.append(i)

    return np.array(peaks).astype(int)


def get_hpp_clusters(peaks_index, min_cluster_size):
    hpp_clusters = []
    cluster = []
    for index, value in enumerate(peaks_index):
        cluster.append(value)

        if index < len(peaks_index)-1 and peaks_index[index+1] - value > 1:
            hpp_clusters.append(cluster)
            cluster = []

        #get the last cluster
        if index == len(peaks_index)-1:
            hpp_clusters.append(cluster)
            cluster = []
    
    hpp_clusters = [cluster for cluster in hpp_clusters if len(cluster)>=min_cluster_size]

    return hpp_clusters


def get_binary(img):
    mean = np.mean(img)
    if mean == 0.0 or mean == 1.0:
        return img

    thresh = threshold_otsu(img)
    binary = img <= thresh
    binary = binary*1

    return binary


def heuristic(a, b):
    return (b[0] - a[0])**2 + (b[1] - a[1])**2

def astar(array, start, goal):

    neighbors = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
    close_set = set()
    came_from = {}
    gscore = {start:0}
    fscore = {start:heuristic(start, goal)}
    oheap = []

    heappush(oheap, (fscore[start], start))
    
    while oheap:

        current = heappop(oheap)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j            
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:                
                    if array[neighbor[0]][neighbor[1]] == 1:
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue
                
            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue
                
            if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heappush(oheap, (fscore[neighbor], neighbor))
                
    return []


def find_line_segments(binary_image, hpp_clusters):
    line_segments = []

    for i, cluster_of_interest in enumerate(hpp_clusters):
        nmap = binary_image[cluster_of_interest[0]:cluster_of_interest[len(cluster_of_interest)-1],:]

        path = np.array(astar(nmap, (int(nmap.shape[0]/2), 0), (int(nmap.shape[0]/2),nmap.shape[1]-1)))
        offset_from_top = cluster_of_interest[0]
        path[:,0] += offset_from_top

        if path.shape != (0,):
            line_segments.append(path)

    return line_segments


def extract_line_images(image, lines):
    line_images = []

    for line_index in range(len(lines) - 1):
        img_copy = np.copy(image)
        lower_line = lines[line_index]
        upper_line = lines[line_index+1]

        lower_boundary = np.min(lower_line[:, 0])
        upper_boundary = np.min(upper_line[:, 0])
        r, c = img_copy.shape

        # for index in range(c-1):
        #     img_copy[0:lower_line[index, 0], index] = 255
        #     img_copy[upper_line[index, 0]:r, index] = 255

        line_images.append(img_copy[lower_boundary:upper_boundary, :])

    return line_images


def get_lines(img_path):
    img_org = rgb2gray(imread(img_path))
    img = np.copy(img_org)
    peaks_index = find_peak_indices(img)
    hpp_clusters = get_hpp_clusters(peaks_index, int(img.shape[0]/20)) # after removing irrelevant clusters

    binary_image = get_binary(img_org)
    # binary_image = remove_roadblocks(binary_image)

    lines = find_line_segments(binary_image, hpp_clusters)

    # for a, b in lines[1]:
    #     print(a, b)
    line_images = extract_line_images(cv2.imread(img_path, 0), lines)
    print('Text Lines found:', len(line_images))
    
    return line_images


# img_path = "handwritten1.jpg"
# line_images = get_lines(img_path)

# print('Size:', len(line_images))
# fig, ax = plt.subplots(figsize=(10,10), nrows=len(line_images))
# for i, line in enumerate(line_images):
#     ax[i].imshow(line, cmap='gray')

# plt.show()
# segmented_img = np.copy(img)
# r,c = segmented_img.shape
# for ri in range(r):
#     if ri in peaks_index:
#         segmented_img[ri, :] = 0
        
# plt.figure(figsize=(20,20))
# plt.imshow(segmented_img, cmap="gray")
# plt.show()

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

