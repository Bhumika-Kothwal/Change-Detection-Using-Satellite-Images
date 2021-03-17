# Change-Detection-Using-Satellite-Images 

## 1. Program file name : DetectChange.py 

### Description of program 
The program detects the change between two images and shows it as an output image.

First, the images are read and resized, and their difference image is found.  
 
```python
diff_image = abs(image1 - image2)
cv2.imwrite(out_dir+'difference.jpg', diff_image)
```

Then Principal Components Analysis (PCA) has been performed. For this, the vector set is found. EVS represents the principal axes in feature space, representing the directions of maximum variance in the data.

```python
pca = PCA()
vector_set, mean_vec=find_vector_set(diff_image, new_size)
pca.fit(vector_set)
EVS = pca.components_
```

Now we need to find the Feature Vector Space.

```python
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
```

To find the change map, K-Means clustering is done on the feature vector set.

```python
def clustering(FVS, components, new):
    kmeans = KMeans(components, verbose = 0)
    kmeans.fit(FVS)
    output = kmeans.predict(FVS)
    count  = Counter(output)
    least_index = min(count, key = count.get)
    change_map  = np.reshape(output,(new[1] - 4, new[0] - 4))
    return least_index, change_map
```

The change map is then written into the output.


### Outputs
#### Example 1
Original Image|  Final Image
:-------------------------:|:-------------------------:
![Initial Image of Ayakkum Lake](/Images/AyakkumLake1.jpg)  |  ![Final Image of Ayakkum Lake](/Images/AyakkumLake2.jpg)

##### Change Map
![Change Map of Ayakkum Lake](/Output/output_ChangeMap_AyakkumLake.jpg)

#### Example 2
Original Image|  Final Image
:-------------------------:|:-------------------------:
![Initial Image of Circle](/Images/circle1.jpg)  |  ![Final Image of Circle](/Images/circle2.jpg)

##### Change Map
![Change Map of Circle](/Output/output_ChangeMap_circle.jpg)

### Conclusion    
Thus, the change map has been created based on the difference between the two images.
  

## 2. Program file name : DetectChange_h4.py , DetectChange_h5.py

### Description of program    
The program file DetectChange_h4.py contains the code with hxh non-overlapping box value as 4x4 (even value of h) and program file DetectChange_h5.py contains the code with hxh non-overlapping box value as 5x5 (even value of h) to create eigen vector space for finding PCA components.

### Outputs
Both the programs with value of hxh non-overlapping box as 4x4 and 5x5 give expected change detection output.

### Conclusion
* hxh non-overlapping box set to create eigen vector space takes both odd and even values of h (concluded by practically experimenting)
