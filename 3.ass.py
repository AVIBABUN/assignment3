import requests
from bs4 import BeautifulSoup
import csv

# Function to perform web scraping
def web_crawler(params):
    primary_category = params.get("Primary Category", "")
    secondary_category = params.get("Secondary Category", "")
    geography = params.get("Geography", "")
    date_range = params.get("Date Range", "")

    # Construct the search query based on parameters
    search_query = f"site:example.com {primary_category} {secondary_category} {geography} {date_range}"

    # Perform a Google search to find URLs matching the query
    google_url = f"https://www.google.com/search?q={search_query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(google_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('a')

        # Extract URLs from search results
        urls = [a['href'] for a in results if a.has_attr('href')]

        # Filter out non-relevant URLs
        relevant_urls = [url for url in urls if url.startswith("http") and not url.startswith("https://www.google")]

        return relevant_urls
    else:
        print(f"Failed to fetch search results. Status code: {response.status_code}")
        return []

# Main function
def main():
    # Example input JSON object
    input_params = {
        "Primary Category": "Medical Journal",
        "Secondary Category": "Orthopedic",
        "Geography": "India",
        "Date Range": "2022"
    }

    # Perform web crawling
    urls = web_crawler(input_params)

    # Write the results to a CSV file
    with open('crawler_results.csv', 'w', newline='') as csvfile:
        fieldnames = ['URL']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for url in urls:
            writer.writerow({'URL': url})

if __name__ == "__main__":
    main()
