"""This script saves the scraped data into a JSON Lines file.
It creates a directory called 'data/raw' (if it doesn't exist) to store the data.
Each scraped item is converted into a JSON format and saved to the 'scraped_data.jsonl' file.
The file is opened at the start of the spider and closed when the spider finishes.
"""

import json
from pathlib import Path

                                                                # This class handles saving scraped data into a JSON file
class SaveToJSONPipeline:
    
                                                                # This method is called when the spider starts scraping
    def open_spider(self, spider):
                                                                # Define the path where the data will be saved (parent directory + 'data/raw')
        data_dir = Path(__file__).resolve().parents[1] / 'data' / 'raw'
        
                                                                # Create the directory if it doesn't exist
        data_dir.mkdir(parents=True, exist_ok=True)
        
                                                                # Open the 'scraped_data.jsonl' file in write mode
        self.file = open(data_dir / 'scraped_data.jsonl', 'w', encoding='utf-8')

                                                                # This method is called when the spider finishes scraping
    def close_spider(self, spider):
                                                                # Close the file after finishing the scraping
        self.file.close()

                                                                # This method processes each item scraped by the spider
    def process_item(self, item, spider):
                                                                # Convert the item dictionary into a JSON string and add a newline
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        
                                                                # Write the JSON string to the file
        self.file.write(line)
        
                                                                # Return the item (so it can be further processed if needed)
        return item
