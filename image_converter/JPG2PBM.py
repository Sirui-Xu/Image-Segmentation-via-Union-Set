from PIL import Image
import cv2

# using Image.open and Image.save from PIL to directly convert .jpg to .ppm
image = Image.open('./greens.jpg').convert('1', dither=NONE)
image.save('./greens.pbm')

# cv2 could not support to directly convert .jpg to .pbm 

