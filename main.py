from engine import analyze_company

def main():
    company_name = "OpenAI"

    try:
        result = analyze_company(company_name)

        print("\n--- Structured Output ---\n")
        print(result)

        print("\n--- Accessing Individual Fields ---\n")
        print("Summary:", result.summary)
        print("Outlook:", result.outlook)
        print("Confidence:", result.confidence)    

    except Exception as e:
        print("Validation failed:", e)


if __name__ == "__main__":
    main()