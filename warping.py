import requests
from bs4 import BeautifulSoup
import html2text

def get_data_from_website(url):
    # Fetching Webpage Content
    response = requests.get(url)
    if response.status_code == 500:
        print("Server error")
        return

    # Parsing HTML with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Removing Unwanted Content (JavaScript and CSS)
    for script in soup(["script", "style"]):
        script.extract()

    # Converting HTML to Markdown
    html = str(soup)
    html2text_instance = html2text.HTML2Text()
    html2text_instance.images_to_alt = True
    html2text_instance.body_width = 0
    html2text_instance.single_line_break = True
    text = html2text_instance.handle(html)

    # Extracting Metadata (Title, Description, Keywords)
    try:
        page_title = soup.title.string.strip()
    except:
        page_title = url.path[1:].replace("/", "-")

    meta_description = soup.find("meta", attrs={"name": "description"})
    meta_keywords = soup.find("meta", attrs={"name": "keywords"})

    description = meta_description.get("content") if meta_description else page_title
    keywords = meta_keywords.get("content") if meta_keywords else ""

    # Returning Text and Metadata
    metadata = {
        'title': page_title,
        'url': url,
        'description': description,
        'keywords': keywords
    }

    return text, metadata
