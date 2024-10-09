import requests
import json
import base64

# Load an image file and encode it to base64
with open("/Users/chris/Documents/vscode_trashcode/processed_image_final.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

url = "http://localhost:11434/api/generate"
data = {
  "model": "llava",
  "prompt":"What text is in the image after KOD:?",
  "images": [encoded_string]
}

response = requests.post(url, data=json.dumps(data))

# Split the response text into lines
lines = response.text.splitlines()

# Initialize an empty list to store the responses
responses = []

# Process each line individually
for line in lines:
    # Parse the line as JSON
    response = json.loads(line)
    # Add the 'response' part to the list
    responses.append(response['response'])

# Join the responses together into a single string, with a space between each one
output = ' '.join(responses)

# Remove leading and trailing spaces and replace multiple spaces with a single space
output = ' '.join(output.split())

# Print the output
print(output)