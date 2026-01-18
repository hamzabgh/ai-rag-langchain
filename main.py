
from core import constants
from database.vector_store import retriever
from models.llm_chain import invoke_chain


def main():
    """Main application loop."""
    print("Pizza Restaurant RAG System")
    print("=" * 30)
    
    while True:
        print(constants.UI_SEPARATOR)
        question = input(constants.PROMPT_MESSAGE)
        
        if question.lower() == constants.EXIT_COMMAND:
            print("\nGoodbye!")
            break
        
        print("\n\n")
        
        try:
            reviews = retriever.invoke(question)
            
            result = invoke_chain(
                reviews=reviews,
                question=question
            )
            
            print(result)
            
        except Exception as e:
            print(f"Error: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main()