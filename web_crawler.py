import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import argparse

def fetch_page_urls(url):
    """Fetches contractor URLs from a given page URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for non-200 status codes
    except requests.RequestException as e:
        print(f"Failed to fetch data from {url}: {e}")
        return None

    # Parse the page content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    all_contractor = soup.find('div', id='all_contractor')

    if all_contractor:
        # Find all section cards containing contractor URLs
        section_cards = all_contractor.find_all('div', class_='section-card')
        # Extract URLs from the section cards
        contractor_urls = [card.find('a', href=True)['href'] for card in section_cards if card.find('a', href=True)]
        return contractor_urls
    else:
        print("Warning: No 'all_contractor' div found on the page.")
        return []

def fetch_contractor_data(url, page_num):
    """Crawls data from a contractor URL."""
    try:
        # Set up and start the Selenium WebDriver
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.get(url)
        page_source = driver.page_source
        driver.quit()

        # Parse the page source using BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')
        section_card = soup.find('div', class_='section-card')
        
        if not section_card:
            print(f"Warning: No 'section-card' div found on the page {url}.")
            return None

        # Extract contractor details 'from the section card
        company_name = section_card.find('h3', class_='card-title').text.strip()
        membership_number = section_card.find('div', string='Membership Number').find_next('div', class_='info-value').text.strip()
        city = section_card.find('div', string='City').find_next('div', class_='info-value').text.strip()
        print(company_name)

        # Email is loaded via JavaScript
        email = section_card.find('div', string='Email ').find_next('div', class_='info-value').text.strip()

        # Extract contractor activities
        activities_section_card = soup.find(lambda tag: tag.name == 'div' and tag.get('class') == ['section-card'] and tag.find('h3', class_='card-title', string='Interests'))
        if activities_section_card:
            activities_elements = activities_section_card.find_all('li', class_='list-item')
            activities = ', '.join(item.text.strip() for item in activities_elements)
        else: 
            activities = 'No data'
        
        # Store contractor data in a dictionary
        contractor_data = {
            'Page': page_num,
            'Name': company_name,
            'Number': membership_number,
            'Email': email,
            'Activities': activities,
            'City': city
        }
        return contractor_data
    except Exception as e:
        print(f"Failed to crawl contractor URL {url}: {e}")
        return None

def fetch_contractors(num_pages):
    """Fetches contractor data from multiple pages."""
    all_contractors = []
    for page_num in range(1, num_pages + 1):
        page_url = f"https://muqawil.org/en/contractors?page={page_num}"
        print(f"Fetching contractors of page {page_num}...")

        # Get the list of contractor URLs on the current page
        page_contractors_urls = fetch_page_urls(page_url)
        if page_contractors_urls:
            # Fetch data for each contractor URL
            for contractor_url in page_contractors_urls:
                contractor_data = fetch_contractor_data(contractor_url, page_num)
                if contractor_data:
                    all_contractors.append(contractor_data)
    return all_contractors

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Crawl contractor data from muqawil.org.')
    parser.add_argument('-n', '--num_pages', type=int, default=10, help='Number of pages to crawl (default is 10)')
    args = parser.parse_args()

    # Number of pages to crawl
    num_pages = args.num_pages  
    contractors = fetch_contractors(num_pages)

    # Save the collected data to an Excel file
    df = pd.DataFrame(contractors)
    df.to_excel(f'output-{num_pages}.xlsx', index=False)