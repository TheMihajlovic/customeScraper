import requests
from bs4 import BeautifulSoup
import csv

# URLs list that will be populated from CSV
urls = []

#import CSV file with URLs
with open('list_of_urls.csv', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        urls.append(row[0])

# Class for data export
class OnPage:
    def __init__(self, url, title, description, tags):
        self.url = url
        self.title = title
        self.description = description
        self.tags = tags

# Storing data to be exported
data = []

# Iterating URLs one by one and appending on data list as objects
for url in urls:
    response = requests.get(url)

    # checking soup and grabbing content of page
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract data from the webpage
        title = soup.title.text if soup.title else 'No title found'
        description = soup.find('div', class_="video-description").get_text().lstrip() if soup.find('div', class_="video-description") else 'No description found'
        tags = soup.find('meta', attrs={'name': 'keywords'}).get('content') if soup.find('meta', attrs={'name': 'keywords'}) else 'No keywords found'

        # Update this iteration object with extracted data
        iterationData = OnPage(url, title, description, tags)

        # Append data with current object
        data.append(iterationData)

    else:
        print(f"Failed to retrieve data from {url}")

# Specify the CSV file name
csv_file = "output.csv"

# Write the list of objects to the CSV file
with open(csv_file, "w", newline="") as file:
    writer = csv.writer(file)

    # Write the header row
    writer.writerow(["URL", "Title", "Description", "Tags"])

    # Write data for each person
    for onePage in data:
        writer.writerow([onePage.url, onePage.title, onePage.description, onePage.tags])

print(f"Data written to {csv_file}")
