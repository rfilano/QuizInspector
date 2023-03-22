import os
from PIL import Image

import pytesseract
import fitz

def pdf_to_image(file):
        doc = fitz.open(file)
        i = 0
        output_pages = []
        for page in doc:
            i += 1
            pix = page.get_pixmap()
            output = file[:-4] + "_page_" + i.__str__() + ".png"
            pix.save(output)
            output_pages.append(output)
        doc.close()
        return output_pages

def images_to_text(pages):
        for page in pages:
            print(pytesseract.image_to_string(Image.open(page)))

def gpt_call(audience, pdf_text):
      return ("Here's a test for " + audience + ". Please provide sample answers for a great student, an average student, and a poor student. Evaluate the difficulty and divergence of each question.\n" + pdf_text)

if __name__ == "__main__":
      pngs = pdf_to_image("Sample2.pdf")
      pdf_text = images_to_text(pngs)

#python quizinspector.py quiz.pdf
#print("Who is the audience for this quiz?")
#audience = user input
#"Here is a quiz for {audience}. Provide sample answers and a difficulty level for each question"