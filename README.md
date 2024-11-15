# Assessment-IntelleWings
Debarred Entities Data Scraper
This project scrapes a webpage containing a table of debarred persons and organisations After scraping the data is stored in a JSON file, and performs simple classification to predict whether the entity is a person or organisation based on the name.
After storing the data, it can be loaded into a csv file for exploratory data analysis(EDA).


## Installations

1. Clone the repository
    git clone <repository-url>
    cd <repository-folder>

2. Install the required  packages
    pip install -r requirements.txt

## Usage
1. Run the scraper
    python main.py
This will open a headless Chrome browser, navigate to the specified URL, and scrape the data from the table.

2. Load JSON to CSV for further analysis
    Use the following script to load 'results.json' into csv format for EDA.
     # Load JSON data 
     df=pd.read_json("results.json")
     # Save JSON data
     df.to_csv("results.json", index=False)             

## File Structure

1. main.py: Main scripts that performs web scraping and stores data in the respective files.
2. requirements.py: List of the dependencies for the project so that they can be respectively installed.
3. README.MD: Documentation for the project.
4. eda.ipynb: The exploratory data analysis implementation.
5. app.py: This file contains a Flask application in which an API has been created with GET method so that a specific ID's details can be fetched in JSON format.