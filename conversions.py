import openai
from PIL import Image
import pytesseract
import fitz
import io

#with open('secrets.txt') as f:
#    openai.api_key = f.read()


def pdf_to_image(file_bits):
    doc = fitz.open("pdf", file_bits)
    i = 0
    output_pages = []
    for page in doc:
        i += 1
        pix = page.get_pixmap()
        output_pages.append(pix.tobytes(output="png"))
    doc.close()
    return output_pages


def images_to_text(pages):
    pdf_text = ""
    for page in pages:
        pdf_text = pdf_text + pytesseract.image_to_string(Image.open(io.BytesIO(page)))
    return pdf_text


def gpt_call(audience, pdf_text):
    prompt = (f"Here's a test for {audience} students."
              f" Please provide sample answers for a great student, an average student, and a poor student."
              f" Evaluate the difficulty and discrimination of each question and provide suggestions.\n{pdf_text}")
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return (response["choices"][0]["message"]["content"])

def ai_call(pdf_path, audience,api_key):
    openai.api_key = api_key
    pngs = pdf_to_image(pdf_path)
    pdf_text = images_to_text(pngs)
    return(gpt_call(audience, pdf_text))
