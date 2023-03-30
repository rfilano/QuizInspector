# Quiz Inspector - Under Construction

QuizInspector is an AI-based quiz analyzer for educators.
This program scans a PDF and sends the PDF contents to OpenAI. The program will provide sample answers for a great student, an average student, a poor student, as well as the difficulty and divergence of each question.

# Sample PDFS
The sample PDFs include:\
SampleMath.pdf - 2 Page, 2nd Grade Math\
SampleHistory.pdf - 1 Page, 11th Grade US History

# Requirements
The requirements are listed in requirements.txt

# How to Use
run program:\
python main.py [pdf_name.pdf]

Enter the target audience in response to the following prompt:\
Please format your response as 'Grade Level Subject'. For example: 3rd grade math.\
What is the target audience?

Program will print out response containing sample answers and question difficulty analysis.

