import pytesseract
from PIL import Image, ImageEnhance
import cv2

image = Image.open('test1.png')
# image = Image.open('test3.jpeg')
brightener = ImageEnhance. Brightness (image)
image = brightener. enhance (1.5)
contraster = ImageEnhance. Contrast (image)
image = contraster. enhance (1.5)
sharpener = ImageEnhance. Sharpness (image)
image = sharpener.enhance (1.5)
image.save('dupa.png')

# Read the image using cv2
#image = cv2.imread('test1.png')
#image = cv2.imread('test6.jpeg')
image = cv2.imread('dupa.png')

# Rotate the image 90 degrees to the right
image_rotated = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

# Convert the image to grayscale using cv2
image_gray = cv2.cvtColor(image_rotated, cv2.COLOR_BGR2GRAY)

# Apply Gaussian Blur to reduce noise
image_blur = cv2.GaussianBlur(image_gray, (5, 5), 0)

# Apply Thresholding to binarize the image
_, image_thresh = cv2.threshold(image_blur, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Apply Morphological Operations to clean up the image
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
image_morph = cv2.morphologyEx(image_thresh, cv2.MORPH_CLOSE, kernel)



custom_config = r'--oem 3 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNPQRSTUVWXYZ-'
# Perform OCR
print(pytesseract.image_to_data(image_morph,config=custom_config))
