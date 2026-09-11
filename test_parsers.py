import sys
from parsers import parse_document

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_parsers.py <path_to_file>")
        return

    file_path = sys.argv[1]
    print(f"Parsing document: {file_path}...\n")
    
    results = parse_document(file_path)
    print(f"Successfully extracted {len(results)} sections/pages.\n")
    
    # Display the first extracted block as a sample
    if results:
        first_block = results[0]
        print(f"--- Sample Output (Source: {first_block['source']}, Page/Slide: {first_block['page_number']}) ---")
        print(first_block['text'][:300] + "..." if len(first_block['text']) > 300 else first_block['text'])
        print("------------------------------------------------------------------")

if __name__ == "__main__":
    main()