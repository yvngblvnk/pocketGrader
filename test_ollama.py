import ollama

def test_ollama_connection():
    # Adjust model_name if you are using a different local model (e.g., 'gemma3:4b', 'mistral')
    model_name = "gemma3:4b"
    
    print(f"Testing connection to Ollama using model: {model_name}...")
    
    try:
        response = ollama.chat(
            model=model_name,
            messages=[
                {"role": "user", "content": "Respond with 'Ollama is connected successfully!' if you can read this."}
            ]
        )
        print("\n--- Response ---")
        print(response["message"]["content"])
        print("----------------")
        print("Phase 0 sanity check passed!")
        
    except Exception as e:
        print(f"\nFailed to connect to Ollama. Error details: {e}")
        print("\nTroubleshooting Steps:")
        print("1. Ensure Ollama app/service is running in the background.")
        print(f"2. Make sure you pulled the model via terminal: `ollama pull {model_name}`")

if __name__ == "__main__":
    test_ollama_connection()