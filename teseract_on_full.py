import os
import re
import pytesseract
from PIL import Image
from process_image import process_image

# Directory containing the images
image_directory = 'pdftojpg/'

# List all files in the directory
image_files = os.listdir(image_directory)
image_files = sorted(image_files)
pattern = r'\w\w\w\w\-\w\w\w\-\w\w\w\w'
custom_config = r'--oem 3 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNPQRSTUVWXYZ-'
# Open a file to save the OCR results
with open('ocr_results.txt', 'w') as result_file:
    counter = 1
    # Perform OCR on each image
    for image_file in image_files:
        image_path = os.path.join(image_directory, image_file)
        processed_image = process_image(image_path)
        ocr_result = pytesseract.image_to_data(processed_image,config=custom_config)
        #result_file.write(f"OCR result for {image_file}:\n")
        matches = re.search(pattern, ocr_result)
        if matches:
            result_file.write(f"{counter}" + ". " + matches.group())
        else:
            result_file.write(f"{counter}" + ". " + f"{image_file}")
        result_file.write("\n")
        counter += 1
def compare_files(file1_path, file2_path):
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        file1_lines = file1.readlines()
        file2_lines = file2.readlines()

    # Ensure both files have the same number of lines
    max_lines = max(len(file1_lines), len(file2_lines))

    for i in range(max_lines):
        line1 = file1_lines[i].strip() if i < len(file1_lines) else ''
        line2 = file2_lines[i].strip() if i < len(file2_lines) else ''
        
        if line1 != line2:
            print(f"Line {i + 1} differs:")
            print(f"File 1: {line1}")
            print(f"File 2: {line2}")

# Example usage
compare_files('ocr_results.txt', 'ocr_results_test.txt') 