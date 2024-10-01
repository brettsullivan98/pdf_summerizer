import streamlit as st
import requests

# Define the URL of your Flask backend API
FLASK_API_URL = "http://127.0.0.1:5000/summarize"

# Title and Description
st.title("AI-Powered PDF Summarizer")
st.write("Upload a PDF file to get a summarized version of its content.")

# Upload File
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# Check if a file has been uploaded
if uploaded_file is not None:
    # Display the name of the uploaded file
    st.write(f"Uploaded file: {uploaded_file.name}")

    # Send the PDF file to the Flask backend
    with st.spinner('Processing...'):
        # Convert the uploaded file to bytes
        files = {'file': uploaded_file.getvalue()}
        response = requests.post(FLASK_API_URL, files={'file': uploaded_file})

    # Check if the response from Flask was successful
    if response.status_code == 200:
        summary = response.json().get("summary", "No summary available.")
        
        # Display the summary
        st.subheader("Summary of the PDF:")
        st.write(summary)
    else:
        st.error("Failed to summarize the PDF. Please try again.")
