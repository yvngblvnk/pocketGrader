import sys
from parsers import parse_document
from vector_store import chunk_documents, store_chunks_in_chroma, query_similar_context

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_vector_store.py <path_to_file>")
        return

    file_path = sys.argv[1]
    print("1. Parsing document...")
    docs = parse_document(file_path)

    print("2. Chunking text...")
    chunks = chunk_documents(docs)
    print(f"Generated {len(chunks)} text chunks.")

    print("3. Storing chunks in ChromaDB...")
    store_chunks_in_chroma(chunks)

    print("\n4. Testing semantic retrieval...")
    test_query = "What are internal controls?"
    results = query_similar_context(query=test_query, n_results=2)

    print(f"\n--- Top Retrieval Results for query: '{test_query}' ---")
    for idx, doc in enumerate(results["documents"][0]):
        meta = results["metadatas"][0][idx]
        print(f"\n[Result {idx + 1}] Source: {meta['source']} (Page {meta['page_number']})")
        print(f"Content: {doc}")
        print("-" * 50)

if __name__ == "__main__":
    main()