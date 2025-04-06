"""This script loads the scraped data from a JSONL file, analyzes the text content to find barriers (such as political, economic, technical, and social barriers), 
and saves the results in a new JSONL file. It uses a set of predefined keywords to identify the barriers in the content.
The processed data is saved in the 'data/cooked/processed_data.jsonl' file.
"""
import json
import os

                                                                    # Path to the raw data (scraped_data.jsonl) and cooked data (processed_data.jsonl)
RAW_DATA_PATH = "C:/Users/aseda/Documents/GitHub/SEI_case1/data/raw/scraped_data.jsonl"
COOKED_DATA_PATH = "C:/Users/aseda/Documents/GitHub/SEI_case1/data/cooked/processed_data.jsonl"

                                                                    # Dictionary of barrier categories with related keywords
barrier_keywords = {
    "political": ["policy", "governance", "political will", "corruption", "regulations"],
    "economic": ["funding", "cost", "investment", "resources", "financial"],
    "technical": ["capacity", "infrastructure", "technology", "data", "tools"],
    "social": ["community", "education", "awareness", "inequality", "participation"],
}

                                                                    # Function to load the raw data from the JSONL file
def load_data(path):
                                                                    # Open the file and read each line as JSON
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

                                                                    # Function to find barriers in the given text based on predefined keywords
def find_barriers(text):
    found = []
                                                                    # Loop through each category and its keywords
    for category, keywords in barrier_keywords.items():
        for kw in keywords:
                                                                    # Check if the keyword is present in the text
            if kw.lower() in text.lower():
                found.append({"category": category, "barrier": kw})
    return found

                                                                    # Main function to analyze the data
def analyze():
    print("Loading data...")                                        # Notify user that the data is being loaded
    data = load_data(RAW_DATA_PATH)                                 # Load the raw data
    output = []                                                     # Initialize an empty list to store processed results

                                                                    # Loop through each item in the loaded data
    for item in data:
        print(f"\n Analyzing: {item['url']}")                       # Display URL of the current item
        content = item.get("content", [])                           # Get the content of the item
        text = " ".join(content).strip()                            # Join the content into one string

                                                                    # If no content is found, skip this item
        if not text:
            print("No content found.")
            continue

                                                                    # Show a preview of the content
        print("Content preview:")
        print(text[:300] + "..." if len(text) > 300 else text)

                                                                    # Find barriers in the content
        barriers = find_barriers(text)

                                                                    # Print the barriers found
        print(" Found barriers:", barriers)

                                                                    # Store the result with URL and found barriers
        output.append({
            "url": item["url"],
            "barriers": barriers
        })

                                                                    # Create the directory for the processed data if it doesn't exist
    os.makedirs(os.path.dirname(COOKED_DATA_PATH), exist_ok=True)
    
                                                                    # Save the processed data to the new JSONL file
    with open(COOKED_DATA_PATH, "w", encoding="utf-8") as f:
        for item in output:
            f.write(json.dumps(item) + "\n")

                                                                    # Notify user that the processing is done
    print(f"\n Done! Processed data saved to: {COOKED_DATA_PATH}")

                                                                    # Run the analysis when the script is executed
if __name__ == "__main__":
    analyze()
