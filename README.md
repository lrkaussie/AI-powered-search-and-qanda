# AI-Powered Document Search & Q&A System

An open-source, self-hosted system that enables natural language querying of documents using state-of-the-art AI technology and RAG (Retrieval-Augmented Generation).

## 🌟 Features

- **Document Upload & Processing**: Support for PDF, DOCX, and TXT files
- **Natural Language Querying**: Ask questions about your documents in plain English
- **RAG-Based Answers**: Get accurate, context-aware responses using advanced AI
- **Vector Search**: Efficient document retrieval using FAISS/ChromaDB
- **User-Friendly Interface**: Built with Streamlit for easy interaction
- **Self-Hosted**: Complete control over your data and privacy
- **Scalable Architecture**: Built with FastAPI and modern AI frameworks

## 🛠️ Tech Stack

- **Backend Framework**: FastAPI
- **Frontend**: Streamlit
- **Document Processing**: PyMuPDF, python-docx, pdfplumber
- **Vector Database**: FAISS/ChromaDB
- **AI/ML**: 
  - LangChain & LlamaIndex for RAG
  - Hugging Face Transformers
  - Open-source LLMs (Mistral, LLaMA 2, Falcon, or GPT-J)
- **Embeddings**: Sentence Transformers

## 🔧 Technical Details

### System Architecture

The system is built with a modular architecture consisting of several key layers:

1. **User Interaction Layer**
   - Streamlit-based frontend for document uploads and query interface
   - Real-time response display with source attribution
   - Asynchronous document processing feedback

2. **API & Backend Layer**
   - FastAPI-based RESTful API endpoints
   - Async request handling for improved performance
   - Request validation and error handling
   - Response caching for frequently asked questions

3. **Document Processing Pipeline**
   - Text extraction from multiple file formats
   - Content chunking with configurable overlap
   - Metadata extraction and preservation
   - Document structure preservation

4. **Vector Storage & Retrieval**
   - Efficient document embedding using Sentence Transformers
   - Vector similarity search with FAISS/ChromaDB
   - Configurable similarity thresholds
   - Metadata-enhanced retrieval

5. **RAG Implementation**
   - Context window optimization
   - Dynamic prompt engineering
   - Source document citation
   - Response quality scoring

### Key Technical Features

#### Document Processing
- Chunk size optimization for context preservation
- Sliding window approach with configurable overlap
- Automatic table and image handling
- OCR integration for scanned documents

#### Embedding & Retrieval
- Bi-encoder architecture for efficient embedding
- Cross-encoder reranking for improved accuracy
- Hybrid search combining sparse and dense retrievers
- Configurable retrieval parameters

#### LLM Integration
- Modular LLM backend supporting multiple models
- Prompt template management
- Context length optimization
- Response filtering and post-processing

#### Performance Optimizations
- Batch processing for document indexing
- Caching at multiple layers
- Async operations for improved throughput
- Resource usage monitoring

#### Security Features
- Input sanitization and validation
- Rate limiting and request throttling
- Document access control
- Secure file handling

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-document-search.git
cd ai-document-search
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

### Running the Application

1. Start the backend server:
```bash
uvicorn app.main:app --reload
```

2. In a new terminal, start the Streamlit frontend:
```bash
streamlit run frontend/app.py
```

3. Open your browser and navigate to `http://localhost:8501`

## 📚 Usage

1. **Upload Documents**:
   - Click the "Upload" button in the interface
   - Select your PDF, DOCX, or TXT files
   - Wait for processing to complete

2. **Ask Questions**:
   - Type your question in natural language
   - The system will retrieve relevant information and generate an answer
   - View source context alongside the answers

## 🎯 Use Cases

- **Medical Research**: Quick analysis of clinical studies and medical papers
- **Legal Document Analysis**: Extract key information from contracts and legal documents
- **Financial Analysis**: Parse and query financial reports and statements
- **Academic Research**: Efficient literature review and textbook querying
- **Policy Research**: Analysis of government documents and policies

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with open-source AI tools and frameworks
- Inspired by the need for efficient document analysis
- Thanks to all contributors and the open-source community

## 📞 Support

For support, please open an issue in the GitHub repository or contact the maintainers. 