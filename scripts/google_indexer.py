import requests

def index_page(url):
    """
    Sends a request to Google to index the specified URL.
    """
    endpoint = 'https://www.google.com/ping'
    params = {'sitemap': url}
    response = requests.get(endpoint, params=params)
    response.raise_for_status()
    print('Successfully requested indexing of', url)

# Example usage:
index_page('https://www.example.com')
