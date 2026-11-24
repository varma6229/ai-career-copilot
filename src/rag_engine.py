from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def chunk_text(text: str) -> List[Document]:
    """
    Splits the raw resume text into small, context-preserving chunks.
    Uses RecursiveCharacterTextSplitter with size 500 and overlap 100
    to suit short, high-density CV formats.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True
    )
    # Wrap text in a list of Documents
    docs = [Document(page_content=text, metadata={"source": "resume"})]
    chunks = text_splitter.split_documents(docs)
    return chunks

def create_vector_store(text: str, api_key: str) -> FAISS:
    """
    Chunks the input text, generates Google Gemini embeddings, and
    builds an in-memory FAISS vector database.
    """
    chunks = chunk_text(text)
    
    # Initialize Google GenAI Embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=api_key
    )
    
    # Create the FAISS vector database in memory
    vector_store = FAISS.from_documents(chunks, embeddings)
    return vector_store

def retrieve_context(vector_store: FAISS, query: str, k: int = 3) -> List[Document]:
    """
    Performs similarity search on the FAISS index to retrieve the
    top k relevant resume chunks.
    """
    # Retrieve the top k matches
    docs = vector_store.similarity_search(query, k=k)
    return docs
