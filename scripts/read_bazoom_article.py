import requests
import pyperclip
from time import sleep
from bs4 import BeautifulSoup
import subprocess
import os

def read_finalarticle_article(url):
    print(f"Reading article from {url}")
    
    if not "final-article.com" in url:
        print("URL is not a final-article.com URL")
        return None
    
    if url.endswith("/"):
        url = url[:-1]
    copy_url = url + "/edit" if not url.endswith("edit") else url
    print(f"Manually copy the article for publication with Select All:\n{copy_url}")
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    subprocess.Popen([chrome_path, "--new-tab", "--profile-directory=Profile 5", copy_url])
    
    if url.endswith("edit"):
        url = url[:-5]
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        article_content = soup.find('div', id='articleContent')
        if not article_content:
            raise ValueError("Article content not found")

        paragraphs = []
        for element in article_content.children:
            if element.name in ['h1', 'h2', 'h3', 'p']:
                text = element.get_text(strip=True)
                heading_level = int(element.name[1]) if element.name.startswith('h') else None
                paragraphs.append((text, heading_level))

        return paragraphs

    except requests.RequestException as e:
        print(f"Error fetching the article: {e}")
    except ValueError as e:
        print(f"Error parsing the article: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return None


def test_read_finalarticle_article():
    if input("Test with the URL in the clipboard? (y/n) ") == "y":
        test_url = pyperclip.paste()
    else:
        test_url = "https://final-article.com/0a0ed0d6-3a02-4d79-ac15-a79cd3047d92"
    
    result = read_finalarticle_article(test_url)
    
    if result is None:
        print("Test failed: Function returned None")
        return
    
    print(f"Number of paragraphs/headings: {len(result)}")
    
    for i, (text, heading_level) in enumerate(result, 1):
        print(f"Item {i}:")
        sleep(.005)
        print(f"  Text: {text[:50]}..." if len(text) > 50 else f"  Text: {text}")
        sleep(.005)
        print(f"  Heading Level: {heading_level}")
        sleep(.01)
        print()
    
    print("Test completed. Please verify the output manually.")

if __name__ == "__main__":
    test_read_finalarticle_article()