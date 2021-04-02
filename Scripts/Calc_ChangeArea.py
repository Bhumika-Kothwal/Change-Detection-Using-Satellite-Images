import cv2 as cv
import argparse
#Parse argument
ap = argparse.ArgumentParser()
ap.add_argument("-cm", "--change_map_image", required = True,
	help = "Path to the directory that contains the change map image")

args = vars(ap.parse_args())

image_path = args["change_map_image"]
c_map = cv.imread(image_path)

total_size = c_map.shape[0] * c_map.shape[1] * c_map.shape[2]

change_size = 0
for r in range(0, c_map.shape[0]):
    for w in range(0,c_map.shape[1]):
        for c in range(0, c_map.shape[2]):
            if(c_map[r][w][c] == 255):
                change_size += 1

per_change = (change_size/total_size) * 100

print("The percentage of area changed = " + str(round(per_change, 3)) + "%")