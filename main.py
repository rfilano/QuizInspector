import os
from PIL import Image

import pytesseract
import fitz

pdf_files = [f for f in os.listdir(
    ".") if os.path.isfile(os.path.join(".", f))]
for file in pdf_files:  # look at every file in the current directory
    if file.endswith('.pdf'):  # if it is a PDF, use it
        doc = fitz.open(file)
        i = 0
        for page in doc:
            i += 1
            pix = page.get_pixmap()
            output = file[:-4] + "_page_" + i.__str__() + ".png"
            pix.save(output)
        doc.close()

png_files = [f for f in os.listdir(
    ".") if os.path.isfile(os.path.join(".", f))]
for file in png_files:
    if file.endswith('.png'):  # if it is a PDF, use it
        print(file[:-4] + " as string: ")
        print(pytesseract.image_to_string(Image.open(file[:-4] + '.png')))
        open(file[:-4] + ".txt",
             "w").write(pytesseract.image_to_string(Image.open(file[:-4] + '.png')))
