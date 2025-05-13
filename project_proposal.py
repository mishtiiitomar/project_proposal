# AI-Powered Proposal Generator Microservice (Streamlit MVP - Polished UI)

import streamlit as st
import PyPDF2
import google.generativeai as genai
from streamlit.components.v1 import html

# --- AUTHENTICATION ---
genai.configure(api_key="AIzaSyDBn8pxrRt8VWKeZ1Apd3M3u4n9gLFg4ZY")
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

# --- PROMPT TEMPLATE ---
PROMPT_TEMPLATE = """
You are a business proposal assistant. Given the new customer requirements and examples of past proposals,
you will generate a professional, 1-page proposal draft. Be clear, persuasive, and structured.
Include a short summary, scope of work, and closing paragraph.

Customer Requirements:
{requirements}

Relevant Proposal Reference Text:
{reference_text}
"""

# --- HELPER FUNCTIONS ---
def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    return text[:3000]  # Reduced for quota efficiency

def generate_proposal(requirements, reference_text):
    prompt = PROMPT_TEMPLATE.format(requirements=requirements, reference_text=reference_text)
    response = model.generate_content(prompt)
    return response.text

# --- CUSTOM STYLES ---
st.markdown("""
    <style>
    .main {background-color: #f9f9f9; font-family: 'Segoe UI', sans-serif;}
    .block-container {padding-top: 2rem;}
    .stButton>button {background-color: #2c3e50; color: white; border-radius: 6px; padding: 0.5rem 1.5rem; font-size: 16px;}
    .stTextArea textarea {font-family: 'Courier New', monospace; font-size: 14px;}
    .stDownloadButton button {background-color: #1abc9c; color: white; border-radius: 4px;}
    </style>
""", unsafe_allow_html=True)

# --- STREAMLIT UI ---
st.markdown("""
    <h1 style='text-align: center; color: #2c3e50;'>📄 AI Proposal Generator</h1>
    <p style='text-align: center; color: #5d6d7e;'>Upload requirements and a reference proposal to generate a polished, client-ready document.</p>
""", unsafe_allow_html=True)

with st.container():
    st.subheader("📌 Step 1: Paste Customer Requirements")
    requirements_input = st.text_area("Describe what the client needs:", height=150)

    st.subheader("📎 Step 2: Upload a Reference Proposal (PDF)")
    reference_file = st.file_uploader("Upload a Past Proposal", type="pdf")

    if st.button("🚀 Generate Proposal") and requirements_input:
        with st.spinner("Creating your proposal with Gemini..."):
            reference_text = extract_text_from_pdf(reference_file) if reference_file else ""
            result = generate_proposal(requirements_input, reference_text)

        st.success("✅ Proposal Generated Successfully!")

        st.markdown("### ✍️ Final Proposal Output")
        st.text_area("Generated Proposal:", result, height=400)
        st.download_button("📥 Download as Text", result, file_name="draft_proposal.txt")


