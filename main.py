from core.engine import analyze_company

def main():

    company="Microsoft"
    cik="0000789019"

    query="What competitive risks affect Microsoft's AI business?"

    intel,features=analyze_company(company,cik,query)

    print("\n--- Structured Intelligence ---\n")
    print(intel)

    print("\n--- Engineered Features ---\n")
    print(features)


if __name__=="__main__":
    main()