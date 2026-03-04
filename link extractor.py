import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote # This fixes the special characters like 'ž'

def get_main_body_links(page_title):
    print(page_title)
    formatted_title = page_title.replace(" ", "_")
    url = f"https://en.wikipedia.org/wiki/{formatted_title}"
    
    headers = {'User-Agent': 'Link find test(aryand4120@gmail.com)'}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error: Could not find page. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    content = soup.find(id="mw-content-text").find(class_="mw-parser-output")
    
    if not content:
        return []

    body_links = []
    stop_ids = {'Notes', 'References', 'External_links', 'See_also', 'Further_reading'}

    # Iterate through the elements in the main body
    for element in content.children:
        # Stop if we hit a bottom-page header
        if element.name in ['h2', 'h3']:
            headline = element.find(class_="mw-headline")
            if headline and headline.get('id') in stop_ids:
                break
        
        # Grab links from paragraphs and lists
        if element.name in ['p', 'ul', 'ol']:
            for a_tag in element.find_all('a', href=True):
                href = a_tag['href']
                # Ensure it's an internal wiki link and not a file/meta-page
                if href.startswith('/wiki/') and ':' not in href:
                    # Clean the URL and handle special characters (like %C5%BE -> ž)
                    raw_title = href.replace('/wiki/', '').replace('_', ' ')
                    clean_title = unquote(raw_title)
                    body_links.append(clean_title)

    # Use a list comprehension to remove duplicates while keeping order
    seen = set()
    return [x for x in body_links if not (x in seen or seen.add(x))]

# Test it out
links = get_main_body_links("Torrence Parsons")
print(links)