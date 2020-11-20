from PIL import Image
import cv2

# using Image.open and Image.save from PIL to directly convert .jpg to .ppm
image = Image.open('./greens.jpg').convert('L')
image.save('./greens.pgm')

# cv2 could not support to directly convert .jpg to .pgm 