import chromadb
from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Use default light-weight embedding model provided by ChromaDB
default_ef = embedding_functions.DefaultEmbeddingFunction()

def get_chroma_client(db_path: str = "./chroma_db"):
    """Initializes persistent ChromaDB client."""
    return chromadb.PersistentClient(path=db_path)

def chunk_documents(documents: list[dict], chunk_size: int = 500, chunk_overlap: int = 50) -> list[dict]:
    """Splits raw parsed document text into smaller overlapping chunks for better search accuracy."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunked_docs = []
    for doc in documents:
        chunks = text_splitter.split_text(doc["text"])
        for idx, chunk in enumerate(chunks):
            chunked_docs.append({
                "text": chunk,
                "metadata": {
                    "source": doc["source"],
                    "page_number": doc["page_number"],
                    "chunk_index": idx
                }
            })
    return chunked_docs

def store_chunks_in_chroma(chunked_docs: list[dict], collection_name: str = "exam_materials", db_path: str = "./chroma_db"):
    """Indexes text chunks into a ChromaDB collection."""
    client = get_chroma_client(db_path)
    collection = client.get_or_create_collection(
        name=collection_name, 
        embedding_function=default_ef
    )

    documents = [item["text"] for item in chunked_docs]
    metadatas = [item["metadata"] for item in chunked_docs]
    ids = [f"{item['metadata']['source']}_p{item['metadata']['page_number']}_c{item['metadata']['chunk_index']}" for item in chunked_docs]

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print(f"Stored {len(documents)} chunks in collection '{collection_name}'.")

def query_similar_context(query: str, n_results: int = 3, collection_name: str = "exam_materials", db_path: str = "./chroma_db"):
    """Retrieves top N relevant text chunks based on a semantic query."""
    client = get_chroma_client(db_path)
    collection = client.get_collection(name=collection_name, embedding_function=default_ef)
    
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results

def clear_vector_store(collection_name: str = "exam_materials", db_path: str = "./chroma_db"):
    """Deletes all indexed chunks and cleans up the collection."""
    client = get_chroma_client(db_path)
    try:
        client.delete_collection(name=collection_name)
        print(f"Collection '{collection_name}' deleted successfully.")
    except Exception as e:
        print(f"Failed to clear collection: {e}")