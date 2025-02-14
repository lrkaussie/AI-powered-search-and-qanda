import streamlit as st
import requests
import json
from pathlib import Path
import time

# API Configuration
API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="AI Document Search & Q&A",
    page_icon="🔍",
    layout="wide"
)

def upload_document(file):
    """Upload a document to the API"""
    files = {"file": (file.name, file, "application/octet-stream")}
    response = requests.post(f"{API_URL}/documents/upload", files=files)
    return response.json()

def query_documents(question: str, stream: bool = False):
    """Query the documents using the RAG system"""
    if stream:
        response = requests.post(
            f"{API_URL}/rag/ask/stream",
            params={"query": question},
            stream=True
        )
        return response
    else:
        response = requests.post(
            f"{API_URL}/rag/ask",
            params={"query": question}
        )
        return response.json()

# App title and description
st.title("📚 AI Document Search & Q&A")
st.markdown("""
Upload documents and ask questions about their content. 
The system will use AI to find relevant information and generate accurate answers.
""")

# Sidebar for document upload
with st.sidebar:
    st.header("📄 Document Upload")
    uploaded_file = st.file_uploader(
        "Choose a document to upload (PDF, DOCX, TXT)",
        type=["pdf", "docx", "txt"]
    )
    
    if uploaded_file:
        if st.button("Upload Document"):
            with st.spinner("Uploading and processing document..."):
                try:
                    result = upload_document(uploaded_file)
                    st.success(f"Document uploaded successfully: {result['title']}")
                except Exception as e:
                    st.error(f"Error uploading document: {str(e)}")

    st.divider()
    st.markdown("### Settings")
    use_streaming = st.checkbox("Enable streaming responses", value=True)

# Main content area
st.header("❓ Ask Questions")

# Question input
question = st.text_input("Enter your question about the documents:")

if question:
    if st.button("Ask"):
        try:
            if use_streaming:
                # Create placeholder for streaming response
                response_placeholder = st.empty()
                context_placeholder = st.empty()
                
                response = query_documents(question, stream=True)
                
                # Initialize response text
                full_response = ""
                
                # Stream the response
                for line in response.iter_lines():
                    if line:
                        data = json.loads(line)
                        if not data.get("finished", False):
                            full_response += data.get("token", "")
                            response_placeholder.markdown(f"**Answer:** {full_response}")
                        else:
                            # Display context when streaming is finished
                            context = data.get("context", [])
                            if context:
                                with context_placeholder.expander("View Source Context", expanded=False):
                                    for i, chunk in enumerate(context, 1):
                                        st.markdown(f"**Source {i}:**")
                                        st.markdown(chunk["chunk"])
                                        st.markdown(f"*From document: {chunk['metadata']['title']}*")
                                        st.divider()
            else:
                with st.spinner("Generating answer..."):
                    response = query_documents(question)
                    
                    # Display the answer
                    st.markdown(f"**Answer:** {response['answer']}")
                    
                    # Display context
                    with st.expander("View Source Context", expanded=False):
                        for i, chunk in enumerate(response['context'], 1):
                            st.markdown(f"**Source {i}:**")
                            st.markdown(chunk["chunk"])
                            st.markdown(f"*From document: {chunk['metadata']['title']}*")
                            st.divider()
                    
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center'>
    <p>Built with FastAPI, ChromaDB, and Mistral-7B</p>
</div>
""", unsafe_allow_html=True) 