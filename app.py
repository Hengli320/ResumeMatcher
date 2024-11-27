from dotenv import load_dotenv; load_dotenv()
from flask import Flask, request, jsonify, render_template
from flask_restful import Api, Resource
from flask_cors import CORS

import fitz 
from database import get_job_requirements
from ai_generator import generate_fit_paragraph
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)

api = Api(app)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
system_content = ( "Please extract skills from the user resume, skills include programming languages like 'python', 'C++', etc"
                    ", technologies such as 'Git' and 'Docker', etc, services like 'GCP', 'AWS', and finally libraries like 'PyTorch', 'TensorFlow'."
                    "Return a list in json format containing all these skills")

@app.route('/')
def home():
    return render_template('index.html')

class UploadResume(Resource):
    def post(self):
        # Retrieve job title and file from the request
        job_title = request.form.get("job_title")
        file = request.files.get("resume")

        # Validate inputs
        if not job_title or not file:
            return {"error": "Job title and resume are required."}, 400

        if not file.filename.lower().endswith('.pdf'):
            return {"error": "Invalid file type. Only PDF files are allowed."}, 400

        try:
            # Process the PDF file in-memory
            pdf_text = extract_text_from_pdf(file)
            keywords = extract_keywords(pdf_text)
            # print(keywords)

            # Retrieve job requirements from the database
            job_requirements = get_job_requirements(job_title)
            if not job_requirements:
                return {"error": f"No job requirements found for the job title: {job_title}"}, 404

            # Match requirements and generate feedback
            # matched_requirements = get_matched_requirements(keywords, job_requirements)
            fit_paragraph = generate_fit_paragraph(keywords, job_requirements)
            
            # Return the feedback
            return jsonify({
                "fit_paragraph": fit_paragraph
            })

        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}, 500


def extract_text_from_pdf(file):
    """Extract text from an uploaded PDF file."""
    doc = fitz.open("pdf", file.read())
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_keywords(text):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": text}
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error occured: {e}")


# Add resource endpoint
api.add_resource(UploadResume, '/upload_resume')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

