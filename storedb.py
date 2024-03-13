import requests
from lxml import html
import pymongo

# Function to extract and store information based on XPath
def extract_store(header, xpath):
    elements = tree.xpath(xpath)
    data = []
    for element in elements:
        data.append(element.text_content())
    document = {"header": header, "data": data}
    collection.insert_one(document)

headers_xpaths = {
    'Pre-1600 NEWS': "/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/ul[1]/*",
    'Pre-1600 BIRTHS': "/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/ul[4]/*",
    '1601-1900 NEWS': "/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/ul[2]/*",
    '1601-1900 BIRTHS': "/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/ul[5]//li",
    '1901-PRESENT NEWS': "/html/body/div[2]/div/div[3]/main/div[3]/div/div[1]/ul[3]/*",
    '1901-PRESENT BIRTHS': "/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/ul[6]/*"
}

# Connection
con = "mongodb://127.0.0.1:27017"
client = pymongo.MongoClient(con)
# Database name
db = client["INTERNSHIP"]


months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
days_in_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

for month in months:
    for day in range(1, days_in_month[months.index(month)] + 1):
        date = f"{month} {day}"  
        # We're scraping from Wikipedia
        url = f"https://en.wikipedia.org/wiki/{date}"
        # Creating a collection with the date
        collection = db[date]
        # Send a GET request to the URL
        response = requests.get(url)
        # Parse the HTML content of the page with the 'lxml' parser
        tree = html.fromstring(response.content)
        if response.status_code == 200:
            # Iterate through headers and XPaths
            for header, xpath in headers_xpaths.items():
                extract_store(header, xpath)
            print(f"SUCCESS for {date}")
        else:
            print(f"FAILURE for {date}")


client.close()
