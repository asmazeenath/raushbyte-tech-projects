import cv2
import easyocr
import os
import pandas as pd

# OCR model
reader = easyocr.Reader(['en'])

def extract_text(image_path):

    image = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Improve image
    gray = cv2.resize(gray, None, fx=1.5, fy=1.5)

    # OCR
    result = reader.readtext(gray)

    text = []

    for detection in result:
        text.append(detection[1])

    return text


# Dataset folders
folders = ["dataset/birth", "dataset/death"]

data = []

for folder in folders:

    certificate_type = "Birth" if "birth" in folder else "Death"

    for file in os.listdir(folder):

        if file.lower().endswith((".jpg", ".jpeg", ".png")):

            path = os.path.join(folder, file)

            print("Processing:", file)

            text = extract_text(path)

            full_text = " ".join(text)

            data.append({
                "Certificate Type": certificate_type,
                "File Name": file,
                "Extracted Text": full_text
            })


# Create Excel
df = pd.DataFrame(data)

df.to_excel(
    "certificate_data.xlsx",
    index=False
)

print("\nExtraction completed!")
print("Excel file created: certificate_data.xlsx")