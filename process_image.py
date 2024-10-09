import pytesseract
from PIL import Image, ImageEnhance
import cv2

def process_image(image_path, output_path='processed_image.png', scale_factor=None, new_dimensions=None):
    # Enhance the image using PIL
    image = Image.open(image_path)
    brightener = ImageEnhance.Brightness(image)
    image = brightener.enhance(1.2)
    contraster = ImageEnhance.Contrast(image)
    image = contraster.enhance(1.85)
    sharpener = ImageEnhance.Sharpness(image)
    image = sharpener.enhance(1.7)
    image.save(output_path)

    # Read the image using cv2
    image = cv2.imread(output_path)

    # Resize the image to twice its original size using cubic interpolation
    #image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    #  Rescale the image if scale_factor or new_dimensions are provided
    if scale_factor:
        image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)
    elif new_dimensions:
        image = cv2.resize(image, new_dimensions, interpolation=cv2.INTER_LINEAR)

    # Rotate the image 90 degrees to the right
    #image_rotated = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

    # Convert the image to grayscale using cv2
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian Blur to reduce noise
    image_blur = cv2.GaussianBlur(image_gray, (3, 3), 0)

    # Apply Thresholding to binarize the image
    _, image_thresh = cv2.threshold(image_blur, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Apply Morphological Operations to clean up the image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    image_morph = cv2.morphologyEx(image_thresh, cv2.MORPH_CLOSE, kernel)

    cv2.imwrite('processed_image_final.png', image_blur)

    return image_morph

# Example usage
processed_image = process_image('test10.png')