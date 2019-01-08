import thread
import cv2 
import sys

def denoise_image(image):
    return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)



input_dir_path = sys.argv[1]
output_path = sys.argv[2]

image = cv2.imread(input_dir_path)
new_image = denoise_image( image )
print(new_image)
cv2.imwrite(output_path, new_image)

