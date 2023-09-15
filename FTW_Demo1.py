# Author: Mehrdad Jalali
# Date: [15.09.2023]
# Version: 1.0

import os
import PyPDF2
import openai
import gradio as gr

# Set your OpenAI API key
openai.api_key = "API-Key"

# Define the PDF files directory
pdfs_directory = "Datasets"

# Function to extract text from a PDF file using PyPDF2
def extract_text_from_pdf(pdf_file_path):
    text = ""
    with open(pdf_file_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Function to generate response using OpenAI API
def generate_response(question):
    # Iterate through PDF files in the directory
    responses = []
    for filename in os.listdir(pdfs_directory):
        if filename.endswith(".pdf"):
            pdf_file_path = os.path.join(pdfs_directory, filename)
            
            # Extract text from the PDF file
            context = extract_text_from_pdf(pdf_file_path)
            
            # Generate response using OpenAI API
            response = openai.Completion.create(
                engine="text-davinci-003",  # Choose the engine you prefer
                prompt=question + "\nContext: " + context,
                max_tokens=100  # Adjust as needed
            )
            
            # Append the generated response to the list
            generated_response = response.choices[0].text.strip()
            responses.append(f"Generated Response for {filename}: {generated_response}")
    
    # Return the list of generated responses
    return "\n".join(responses)

# Define the Gradio interface
title_html = '<div style="display: flex; align-items: center; justify-content: center; text-align: center;">' \
             '<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Logo_KIT.svg/800px-Logo_KIT.svg.png?20200302125831" style="max-width: 250px; margin-right: 10px;">' \
             '<span style="color: #2EA28A; font-size: 36px;">LLN-ELN: Revolutionizing Experiments with Large Language Models!</span>' \
             '<img src="https://i.ibb.co/8XMKP9k/My-project-1.png" style="max-width: 200px; margin-left: 10px;">' \
             '</div>'



iface = gr.Interface(
    fn=generate_response,
    inputs=gr.inputs.Textbox(placeholder="Enter your question..."),
    outputs="text",
    title=title_html,
    description="Enter a question and get AI-generated responses from ELN documents.",
    live=True,
    examples=[
    ["What is the value of the Detector in Opus?"],
    ["what is the unit of Aperture?"],
    ["what are the preparation steps for HKUST-1 in the ordered list?"],
    ["What is the purpose of cleaning the sample chamber in the context of the HKUST-1 experiment?"]],
    allow_screenshot=True,
    layout="wide"
)

# Run the Gradio interface
iface.launch()
