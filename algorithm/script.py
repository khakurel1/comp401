import pandas as pd



tickers = ["AEP", "DFSVX", "DFLVX", "FSAGX"]

for t in tickers:
    # Step 1: Read the CSV file
    df = pd.read_csv(f"./algorithm/data/{t}.csv")

    # Step 2: Convert the DataFrame to JSON
    json_data = df.to_json(orient='records')

    # Step 3: Save the JSON to a file
    with open(f"./algorithm/data/{t}.json", 'w') as json_file:
        json_file.write(json_data)

    print("CSV file has been converted to JSON.")