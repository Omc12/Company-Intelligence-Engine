from core.engine import analyze_company
from rag.evaluation import compute_precision_at_k

def main():
    company_name = "OpenAI"

    try:
        intel, features, docs = analyze_company(company_name)

        print("\n--- Structured Intelligence ---\n")
        print(intel)

        print("\n--- Engineered Features ---\n")
        print(features)  

        precision = compute_precision_at_k(company_name, docs, k=3)
        print(f"\nPrecision@3: {precision}")

    except Exception as e:
        print("Validation failed:", e)

if __name__ == "__main__":
    main()