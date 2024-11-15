import re
import json
import uuid
import requests
import spacy
from bs4 import BeautifulSoup
import httpx
import pandas as pd

# Clean the extracted text
def clean(txt):
    s = ""
    v = set('QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890,.-()/ ')
    for i in txt:
        if i not in v or i == '\n':
            continue
        else:
            s += i
    s = s.replace('\n', ' ')
    return s

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

import httpx

url = "https://lnadbg4.adb.org/oga0009p.nsf/sancALL1P?OpenView&count=999"

try:
    response = httpx.get(url, verify=False)  # Disable SSL verification
    response.raise_for_status()
except httpx.RequestError as e:
    print(f"Error fetching data: {e}")
    exit(1)


# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')
view_container = soup.find('div', {'id': 'viewcontainer'})
table = view_container.find('table')

data = []

# Iterate over table rows
for row in table.find_all('tr')[1:]:  # Skip header row
    columns = row.find_all('td')
    if len(columns) == 8:
        name = columns[1].text.strip()
        address = columns[2].text.strip()
        add = clean(address)
        sanction_type = columns[3].text.strip()
        nationality = columns[5].text.strip()
        date = columns[6].text.strip()

        # Split date into effect and lapse
        try:
            effect, lapse = date.split('|')
            effect, lapse = effect.strip(), lapse.strip()
        except ValueError:
            effect, lapse = "", ""  # In case the date is missing or malformed

        grounds = columns[7].text.strip()

        # Perform Named Entity Recognition (NER) using spaCy on the 'Name' column
        doc = nlp(name)
        entity_type = None
        for ent in doc.ents:
            if ent.label_ in ['PERSON', 'ORG']:
                entity_type = ent.label_
                break

        # Generate a unique identifier (UUID)
        uuid_val = str(uuid.uuid4())

        # Append extracted data to the list
        data.append({
            'uuid': uuid_val,
            'Name': name,
            'Address': add,
            'Sanction Type': sanction_type,
            'Nationality': nationality,
            'Effect Date': effect,
            'Lapse Date': lapse,
            'Grounds': grounds,
            'Entity Type': entity_type if entity_type else 'UNKNOWN'  # Set to 'UNKNOWN' if no entity is found
        })
    else:
        print(f"Skipping row with unexpected number of columns: {row}")

# Save the data to a JSON file
output_file = 'results.json'
try:
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=2)
    print(f"Data saved to {output_file}")
except IOError as e:
    print(f"Error writing to {output_file}: {e}")


## now converting the json into csv

df = pd.DataFrame(data)

# Save to CSV
df.to_csv('results.csv', index=False)

print("Data successfully saved to 'results.csv'.")

