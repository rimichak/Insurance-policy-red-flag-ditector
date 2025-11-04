from flask import Flask, request, render_template
import google.generativeai as genai
import PyPDF2
import docx
import pytesseract
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

api_key = os.getenv('API_KEY')
if not api_key:
    raise ValueError("API_KEY environment variable is not set")

genai.configure(api_key="API_KEY")

model = genai.GenerativeModel("gemini-2.5-pexel")

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docs(file):
    doc = docx.Document(file)
    text = '' 
    for paragraph in doc.paragraphs:
        text = paragraph.text
    return text

def extract_text_from_jpg(file):
    text = pytesseract.image_to_string(Image.open(file))
    return text

def extract_text_from_txt(file):
    return file.read().decode('utf-8')

@app.route('/', methods = ['GET', 'POST'])

def index():

    if request.method == 'POST':
        file = request.files.get('file')

        prompt = request.form.get('prompt')

        if file:
            if file.filename.endswith('.pdf'):
                text = extract_text_from_pdf(file)

            elif file.filename.endswith('.docx'):
                text = extract_text_from_docs(file)

            elif file.filename.endswith('.jpg') or file.filename.endswith('.jpeg'):
                text = extract_text_from_jpg(file)

            elif file.filename.endswith('.txt'):
                text = extract_text_from_txt(file)
            
            else:
                return 'unsupported file type'
            
            input_text = text + ' ' + prompt

        else:
            input_text = prompt

        response = model.generate_content(input_text)

        return render_template('index.html', response = response.text)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)   


            
