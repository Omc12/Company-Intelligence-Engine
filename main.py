from core.engine import analyze_company

def main():
    company_name = "OpenAI"

    try:
        intel, features = analyze_company(company_name)

        print("\n--- Structured Intelligence ---\n")
        print(intel)

        print("\n--- Engineered Features ---\n")
        print(features)  

    except Exception as e:
        print("Validation failed:", e)


if __name__ == "__main__":
    main()