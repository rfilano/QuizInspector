import openai
from PIL import Image
import argparse
import pytesseract
import fitz

with open('secrets.txt') as f:
    openai.api_key = f.read()

openai.organization = "org-mTI7Tu5c0oKv0R9vhYmzhSS5"


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
    pdf_text = ""
    for page in pages:
        pdf_text = pdf_text + pytesseract.image_to_string(Image.open(page))
    return pdf_text


def gpt_call(audience, pdf_text):
    prompt = "Here's a test for " + audience + \
        " students. Please provide sample answers for a great student, an average student, and a poor student. Evaluate the difficulty and divergence of each question.\n" + pdf_text
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return (response["choices"][0]["message"]["content"])


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("pdf_name")
    args = parser.parse_args()
    pngs = pdf_to_image(args.pdf_name)
    pdf_text = images_to_text(pngs)
    print("Please format your response as 'Grade Level Subject'\n For example: 3rd grade math.")
    audience = input("What is the target audience? ")
    print(gpt_call(audience, pdf_text))
