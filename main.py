import os
import re
import pytesseract
from PIL import Image, ImageEnhance
import cv2

def list_image_files(directory):
    image_files = os.listdir(directory)
    return sorted(image_files)

def enhance_image(image_path, output_path, brightness=1.2, contrast=1.85, sharpness=1.7):
    image = Image.open(image_path)
    brightener = ImageEnhance.Brightness(image)
    image = brightener.enhance(brightness)
    contraster = ImageEnhance.Contrast(image)
    image = contraster.enhance(contrast)
    sharpener = ImageEnhance.Sharpness(image)
    image = sharpener.enhance(sharpness)
    image.save(output_path)
    return output_path

def resize_image(image, scale_factor=None, new_dimensions=None):
    if scale_factor:
        return cv2.resize(image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)
    elif new_dimensions:
        return cv2.resize(image, new_dimensions, interpolation=cv2.INTER_LINEAR)
    return image

def process_cv2_image(image, blur_kernel_size=(3, 3), morph_kernel_size=(3, 3)):
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_blur = cv2.GaussianBlur(image_gray, blur_kernel_size, 0)
    _, image_thresh = cv2.threshold(image_blur, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, morph_kernel_size)
    image_morph = cv2.morphologyEx(image_thresh, cv2.MORPH_CLOSE, kernel)
    return image_morph

def process_image(image_path, output_path='processed_image.png', scale_factor=None, new_dimensions=None,
                  brightness=1.2, contrast=1.85, sharpness=1.7, blur_kernel_size=(3, 3), morph_kernel_size=(3, 3)):
    enhanced_image_path = enhance_image(image_path, output_path, brightness, contrast, sharpness)
    image = cv2.imread(enhanced_image_path)
    image = resize_image(image, scale_factor, new_dimensions)
    processed_image = process_cv2_image(image, blur_kernel_size, morph_kernel_size)
    cv2.imwrite('processed_image_final.png', processed_image)
    return processed_image

def process_image_and_ocr(image_path, custom_config, pattern, output_path='processed_image.png', scale_factor=None, new_dimensions=None,
                          brightness=1.2, contrast=1.85, sharpness=1.7, blur_kernel_size=(3, 3), morph_kernel_size=(3, 3)):
    processed_image = process_image(image_path, output_path, scale_factor, new_dimensions, brightness, contrast, sharpness, blur_kernel_size, morph_kernel_size)
    ocr_result = pytesseract.image_to_data(processed_image, config=custom_config)
    matches = re.search(pattern, ocr_result)
    return matches.group() if matches else os.path.basename(image_path)

def process_images(image_directory, output_file, custom_config, pattern, output_path='processed_image.png', scale_factor=None, new_dimensions=None,
                   brightness=1.2, contrast=1.85, sharpness=1.7, blur_kernel_size=(3, 3), morph_kernel_size=(3, 3)):
    image_files = list_image_files(image_directory)
    with open(output_file, 'w') as result_file:
        for counter, image_file in enumerate(image_files, start=1):
            image_path = os.path.join(image_directory, image_file)
            ocr_result = process_image_and_ocr(image_path, custom_config, pattern, output_path, scale_factor, new_dimensions, brightness, contrast, sharpness, blur_kernel_size, morph_kernel_size)
            #result_file.write(f"{counter}. {ocr_result}\n")
            result_file.write(f"{ocr_result}\n")

# Example usage with all parameters
if __name__ == "__main__":
    image_directory = 'ilovepdf_pages-to-jpg-7/'
    custom_config = r'--oem 3 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNPQRSTUVWXYZ-'
    pattern = r'\w\w\w\w\-\w\w\w\-\w\w\w\w'
    output_file = 'ocr_results.txt'
    output_path = 'processed_image.png'
    scale_factor = None
    new_dimensions = None
    brightness = 1.2
    contrast = 1.85
    sharpness = 1.7
    blur_kernel_size = (3, 3)
    morph_kernel_size = (3, 3)

    process_images(image_directory, output_file, custom_config, pattern, output_path, scale_factor, new_dimensions, brightness, contrast, sharpness, blur_kernel_size, morph_kernel_size)