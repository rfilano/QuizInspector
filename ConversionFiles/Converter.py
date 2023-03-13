# Tutorial and code from James Villemarette
# https://gist.github.com/jvillemare/81887e9c53253c16e7ce0f9c60250779
# https://www.youtube.com/watch?v=62JZImLe6Qw
import os			    # for magick and tesseract commands
import time			  # for epoch time
from pdf2image import convert_from_path
from PyPDF2 import PdfMerger
from pdfminer.high_level import extract_text

dir_files = [f for f in os.listdir(
    ".") if os.path.isfile(os.path.join(".", f))]
epoch_time = int(time.time())
formatted_time = time.strftime('%m_%d_%Y', time.localtime(epoch_time))
print(dir_files)
all_combined = []

for file in dir_files:  # look at every file in the current directory
    if file.endswith('.pdf'):  # if it is a PDF, use it
        print('Working on converting: ' + file)
        # setup
        # get just the filepath without the extension
        file = file.replace('.pdf', '')
        # generate a folder name for temporary images
        folder = "Output/" + file + '_' + formatted_time
        combined = folder + '/' + file  # come up with temporary export path
        # create folder
        if not os.path.exists(folder):  # make the temporary folder
            os.makedirs(folder)
        # convert PDF to PNG(s)
        #add pdf to image stuff here
        # convert PNG(s) to PDF(s) with OCR data
        pngs = [f for f in os.listdir(
            folder) if os.path.isfile(os.path.join(folder, f))]
        for pic in pngs:
            if pic.endswith('.png'):
                combined_pic = folder + '/' + pic
                print(combined_pic)
                tesseract = 'tesseract "' + combined_pic + '" "' + combined_pic + '-ocr" PDF'
                print(tesseract)
                os.system(tesseract)
        # combine OCR'd PDFs into one
        ocr_pdfs = [f for f in os.listdir(
            folder) if os.path.isfile(os.path.join(folder, f))]

        merger = PdfMerger()
        for pdf in ocr_pdfs:
            if pdf.endswith('.pdf'):
                merger.append(folder + '/' + pdf)

        merger.write(folder + '-ocr-combined.pdf')
        all_combined.append(folder + '-ocr-combined.pdf')
        merger.close()

        for f in all_combined:
            name = f[:-17] + ".txt"
            file_object = open(name, "w+")
            file_object.write(extract_text(f))