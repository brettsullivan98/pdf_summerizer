from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from PyPDF2 import PdfReader
from transformers import pipeline
import os

app = Flask(__name__)
api = Api(app)

# Initialize the summarization model
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", framework="pt")

class PDFSummarizer(Resource):
    def post(self):
        # Check if a file was uploaded
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        
        # Check if the file is a PDF
        if not file.filename.endswith('.pdf'):
            return jsonify({"error": "File is not a PDF"}), 400

        # Save the file to a temporary location
        filepath = os.path.join("uploads", file.filename)
        file.save(filepath)

        # Extract text from the PDF
        text = extract_text_from_pdf(filepath)
        
        # Summarize the extracted text
        summary = summarizer(text, max_length=130, min_length=30, do_sample=False)[0]['summary_text']

        # Clean up the temporary file
        os.remove(filepath)

        return jsonify({"summary": summary})

def extract_text_from_pdf(filepath):
    """Extracts text from a PDF file."""
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""  # Extract text from each page
    return text

api.add_resource(PDFSummarizer, '/summarize')

if __name__ == '__main__':
    # Create the uploads directory if it doesn't exist
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    app.run(debug=True)