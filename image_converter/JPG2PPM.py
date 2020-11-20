from PIL import Image
import cv2

# using Image.open and Image.save from PIL to directly convert .jpg to .ppm
image = Image.open('./greens.jpg')
image.save('./greens.ppm')

# using cv2.imread and cv2.imwrite from cv2, which is much similar to matlab
# image = cv2.imread('./greens.jpg')
# cv2.imwrite('./greens.ppm', image)