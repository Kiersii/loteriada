import os
import re
import pytesseract
from PIL import Image

# Directory containing the images
image_directory = 'data_to_extract'

# List all files in the directory
image_files = os.listdir(image_directory)
pattern = r'\w\w\w\w\-\w\w\w\-\w\w\w\w'
# Open a file to save the OCR results
with open('ocr_results.txt', 'w') as result_file:
    # Perform OCR on each image
    for image_file in image_files:
        image_path = os.path.join(image_directory, image_file)
        ocr_result = pytesseract.image_to_data(Image.open(image_path))
        #result_file.write(f"OCR result for {image_file}:\n")
        matches = re.search(pattern, ocr_result)
        result_file.write(matches.group())
        result_file.write("\n")

 