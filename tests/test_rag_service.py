
from backend.app.services.rag_service import answer_question


def main():
    question = "How many public holidays does the company observe?"

    result = answer_question(question)

    print("\nQuestion:", result["question"])
    print("\nAnswer:", result["answer"])
    print("\nSources:")

    for source in result["sources"]:
        print("-", source["text"])


if __name__ == "__main__":
    main()
