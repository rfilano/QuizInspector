from PIL import Image

import pytesseract
import fitz

pdffile = "Sample6.pdf"
doc = fitz.open(pdffile)
page = doc.load_page(0)  # number of page
pix = page.get_pixmap()
output = "outfile.png"
pix.save(output)
doc.close()

print(pytesseract.image_to_string(Image.open('outfile.png')))

#reader = PdfReader("Sample6.pdf")
#page = reader.pages[0]
#print(page.extract_text())
#f = open("ConversionFiles\sample6.txt", "w")
#f.write(page.extract_text())