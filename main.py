"""
Entry point — interactive CLI loop.

Usage:
python main.py

Type your question and press Enter.
Type  'exit' to quit.
"""

from src.assistant import chat

def main() ->None:
    print("Welcome to the assistant! Type your question or 'exit' to quit.")
    print("=" * 50)
    print("Example questions:")
    print(" - What is 128 times 46?")
    print(" - Who was Albert Einstein?")
    print(" - How is the weather in São Paulo?")
    print(" - What is the UV index in Rio de Janeiro?")
    print(" - What is the air quality in Beijing?")
    print(" - What is the square root of 1024?")
    print("Type 'exit' to quit.\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        
        if not user_input:
            continue
        
        if user_input.lower() in ['exit']:
            print("Goodbye!")
            break
        try:           
            response = chat(user_input)
            print(f"Assistant: {response}")
        
        except Exception as e:
            print(f"Error: Something went wrong: {e}")
            print("Please try again.")
        

if __name__ == "__main__":
    main()