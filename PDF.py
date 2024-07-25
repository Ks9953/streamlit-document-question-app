import streamlit as st
import openai
from PyPDF2 import PdfReader
import docx
import os

# Set your OpenAI API key
openai.api_key = 'sk-None-BzE8MAcGklCQOcQyxx4VT3BlbkFJJWa2iOLRwqKxqU3fqO1m'

# Function to read PDF file
def read_pdf(file):
    pdf = PdfReader(file)
    text = ""
    for page_num in range(len(pdf.pages)):
        page = pdf.pages[page_num]
        text += page.extract_text()
    return text

# Function to read DOCX file
def read_docx(file):
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text
    return text

# Function to extract text from the file
def extract_text_from_file(file):
    file_extension = os.path.splitext(file.name)[1].lower()
    if file_extension == '.pdf':
        return read_pdf(file)
    elif file_extension == '.docx':
        return read_docx(file)
    else:
        st.error('Unsupported file format')
        return None

# Streamlit App
st.title("Document Question Answering Application")

uploaded_files = st.file_uploader("Upload PDF or DOCX files", accept_multiple_files=True, type=["pdf", "docx"])

if uploaded_files:
    document_texts = []
    for file in uploaded_files:
        text = extract_text_from_file(file)
        if text:
            document_texts.append(text)

    st.write("Documents uploaded successfully!")

    user_question = st.text_input("Enter your question")

    if st.button("Get Answer") and user_question:
        combined_text = "\n".join(document_texts)
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Updated parameter
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Answer the following question based on the provided documents:\n\n{combined_text}\n\nQuestion: {user_question}\nAnswer:"}
            ],
            max_tokens=150
        )
        answer = response.choices[0].message['content'].strip()  # Updated parameter
        st.write(f"Answer: {answer}")

        # Save the conversation
        if 'history' not in st.session_state:
            st.session_state.history = []
        st.session_state.history.append(f"Q: {user_question}\nA: {answer}")

# To save conversations
st.sidebar.title("Conversation History")
if 'history' in st.session_state:
    conversation_history = "\n\n".join(st.session_state.history)
else:
    conversation_history = ""
st.sidebar.text_area("History", value=conversation_history, height=300)

