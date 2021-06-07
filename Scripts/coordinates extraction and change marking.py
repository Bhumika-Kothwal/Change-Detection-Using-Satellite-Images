image1_path = "/home/tejal/Change-Detection-Using-Satellite-Images/Images/AyakkumLake1.jpg"
image2_path = "/home/tejal/Change-Detection-Using-Satellite-Images/Images/AyakkumLake2.jpg"
out_dir = "/home/tejal/Change-Detection-Using-Satellite-Images/Output"


print('[INFO] Start Change Detection ...')
print('[INFO] Importing Librairies ...')
import cv2 
import sklearn
from sklearn.cluster import KMeans
from collections import Counter
from sklearn.decomposition import PCA
import skimage.morphology
import numpy as np
import matplotlib.pyplot as plt 
import time


def find_vector_set(diff_image, new_size):
 
    i = 0
    j = 0
    vector_set = np.zeros((int(new_size[0] * new_size[1] / 25),25))
    while i < vector_set.shape[0]:
        while j < new_size[1]:
            k = 0
            while k < new_size[0]:
                block   = diff_image[j:j+5, k:k+5]
                feature = block.ravel()
                vector_set[i, :] = feature
                k = k + 5
            j = j + 5
        i = i + 1

    mean_vec   = np.mean(vector_set, axis = 0)
    # Mean normalization
    vector_set = vector_set - mean_vec   
    return vector_set, mean_vec

def find_FVS(EVS, diff_image, mean_vec, new):
 
    i = 2
    feature_vector_set = []
 
    while i < new[1] - 2:
        j = 2
        while j < new[0] - 2:
            block = diff_image[i-2:i+3, j-2:j+3]
            feature = block.flatten()
            feature_vector_set.append(feature)
            j = j+1
        i = i+1
 
    FVS = np.dot(feature_vector_set, EVS)
    FVS = FVS - mean_vec
    print ("[INFO] Feature vector space size", FVS.shape)
    return FVS

def clustering(FVS, components, new):
    kmeans = KMeans(components, verbose = 0)
    kmeans.fit(FVS)
    output = kmeans.predict(FVS)
    count  = Counter(output)
 
    least_index = min(count, key = count.get)
    change_map  = np.reshape(output,(new[1] - 4, new[0] - 4))
    return least_index, change_map
# edge detectionusing canny filter and ploting it 
def edge_detection(CloseMap):
    edges = cv2.Canny(CloseMap, 100, 200)
    plt.subplot(121), plt.imshow(CloseMap, cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(edges,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    plt.savefig('Edge Image.png')
    plt.show()
    #cv2.imwrite(out_dir+'Edges.jpg', edges)
    return edges
# extracting coordinates of the changed area by dividing the changed image into sections of size 5x5
def printFinal(image, edge):
    #dividing the white section of the edge detected image into 5x5 sections 
    edge[:5,:5] = 255
    #finding the white section of the image and storing the coordinates in the variable indices
    indices = np.where(edge == 255)
    print ("coordinates of changed places" ,indices)
    coordinates = zip(indices[0], indices[1])
    #forming a numpy array of x and y coordinates
    arr1 = np.asarray(list(map(np.int, indices[0])))
    arr2 = np.asarray(list(map(np.int, indices[1])))
    #copying the original input image in variable impcopy
    imcopy = image.copy()
    #changing the colour of the coordinates in the original image wherever a change is seen 
    for i in range(len(indices[0])):
        imcopy[indices[0][i]][indices[1][i]] = [255, 0, 0]
    #plotting the changes
    plt.subplot(121), plt.imshow(image)
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(imcopy)
    plt.title('Final Image'), plt.xticks([]), plt.yticks([])
    plt.savefig('Final Image.png')
    plt.show()
    

# Read Images
print('[INFO] Reading Images ...')
start = time.time()
image1 = cv2.imread(image1_path)
image2 = cv2.imread(image2_path)
end = time.time()
print('[INFO] Reading Images took {} seconds'.format(end-start))


# Resize Images
print('[INFO] Resizing Images ...')
start = time.time()
new_size = np.asarray(image1.shape) /5
new_size = new_size.astype(int) *5
image1 = cv2.resize(image1, (new_size[0],new_size[1])).astype(int)
image2 = cv2.resize(image2, (new_size[0],new_size[1])).astype(int)
end = time.time()
print('[INFO] Resizing Images took {} seconds'.format(end-start))

# Difference Image
print('[INFO] Computing Difference Image ...')
start = time.time()
diff_image = abs(image1 - image2)

#cv2.imwrite(out_dir+'difference.jpg', diff_image)
end = time.time()
print('[INFO] Computing Difference Image took {} seconds'.format(end-start))
diff_image=diff_image[:,:,1]
print("diff image shape : " + str(diff_image.shape))


print('[INFO] Performing PCA ...')
start = time.time()
pca = PCA()
vector_set, mean_vec=find_vector_set(diff_image, new_size)
pca.fit(vector_set)
EVS = pca.components_
end = time.time()
print('[INFO] Performing PCA took {} seconds'.format(end-start))

print('[INFO] Building Feature Vector Space ...')
start = time.time()
FVS = find_FVS(EVS, diff_image, mean_vec, new_size)
components = 3
end = time.time()
print('[INFO] Building Feature Vector Space took {} seconds'.format(end-start))

print('[INFO] Clustering ...')
start = time.time()
least_index, change_map = clustering(FVS, components, new_size)
end = time.time()
print('[INFO] Clustering took {} seconds'.format(end-start))

change_map[change_map == least_index] = 255
change_map[change_map != 255] = 0
change_map = change_map.astype(np.uint8)

print('[INFO] Save Change Map ...')
cv2.imwrite(out_dir+'ChangeMap.jpg', change_map)

print('[INFO] Performing Closing ...')
print('[WARNING] Kernel is fixed depending on image topology')
print('[WARNING] Closing with disk-shaped structuring element with radius equal to 6')
kernel = skimage.morphology.disk(6)
CloseMap = cv2.morphologyEx(change_map, cv2.MORPH_CLOSE, kernel)
#cv2.imwrite(out_dir+'CloseMap.jpg', CloseMap)

print('[INFO] Performing Opening ...')
OpenMap = cv2.morphologyEx(CloseMap, cv2.MORPH_OPEN, kernel)
#cv2.imwrite(out_dir+'OpenMap.jpg', OpenMap)

print('[INFO] Performing Edge Detection ...')
edges = edge_detection(CloseMap)

print('[INFO] Getting Final Image ...')
printFinal(image1, edges)
