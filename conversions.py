import openai
from PIL import Image
import pytesseract
import fitz
import io

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


def gpt_call(audience, pdf_text, flags):
    sample_students = []
    sample_student_prompt = ""
    prompt = "Here's a test for" + audience + "students."
    for flag in flags:
        if flag == "g":
            sample_students.append("a good student")
        if flag == "a":
            sample_students.append("an average student")
        if flag == "p":
            sample_students.append("a poor student")
        if flag == "d":
            prompt = prompt + "Evalute the divergence of each question."
        if flag == "r":
            prompt = prompt + "Rate the relevancy of the questions to the target audience."
    if len(sample_students) > 0:
        sample_student_prompt = "Please provide sample answers for "
        if len(sample_students) == 1:
            sample_student_prompt = sample_student_prompt + sample_students[0] + "."
        if len(sample_students) == 2:
                sample_student_prompt = sample_student_prompt + sample_students[0] + ", " + sample_students[1] + "."
        if len(sample_students) == 3:
                sample_student_prompt = sample_student_prompt + sample_students[0] + ", " + sample_students[1] + ",and " + sample_students[2] + "."
    prompt = prompt + sample_student_prompt + " Evaluate the difficulty each question and provide suggestions.\n" + pdf_text
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return (response["choices"][0]["message"]["content"])

def ai_call(pdf_path, audience,api_key, flags):
    openai.api_key = api_key
    pngs = pdf_to_image(pdf_path)
    pdf_text = images_to_text(pngs)
    return(gpt_call(audience, pdf_text, flags))
