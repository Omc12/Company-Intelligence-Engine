from core.engine import analyze_company

def main():
    try:
        intel, features = analyze_company(
            "Microsoft",
            "0000789019"
        )

        print("\n--- Structured Intelligence ---\n")
        print(intel)

        print("\n--- Engineered Features ---\n")
        print(features)

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()