import requests
from bs4 import BeautifulSoup, Comment
from urllib.parse import unquote

def is_disambiguation_page(title):
    """
    Checks if the given Wikipedia page title is a disambiguation page.
    If it is, returns (True, first linked article title). Otherwise, returns (False, None).
    """
    S = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"

    PARAMS1 = {
        "action": "query",
        "format": "json",
        "prop": "categories",
        "titles": title,
        "cllimit": "max",
        "clshow": "!hidden"
    }

    response = S.get(url=URL, params=PARAMS1)
    data = response.json()

    pages = data["query"]["pages"]
    page_id = next(iter(pages))
    page = pages[page_id]

    is_disambig = False
    if "categories" in page:
        for cat in page["categories"]:
            if cat["title"] == "Category:Disambiguation pages":
                is_disambig = True
                break

    if not(is_disambig):
        return False, None

    PARAMS2 = {
        "action": "parse",
        "page": title,
        "format": "json",
        "prop": "text"
    }

    response_parse = S.get(url=URL, params=PARAMS2)
    data_parse = response_parse.json()
    html_content = data_parse["parse"]["text"]["*"]

    soup = BeautifulSoup(html_content, "html.parser")
    content_div = soup.find("div", class_="mw-parser-output")

    links = []
    for tag in content_div.find_all("a", href=True):
        href = tag["href"]
        if href.startswith("/wiki/") and not href.startswith("/wiki/Help:") and ":" not in href:
            title = tag.get("title")
            if title and title not in links:
                links.append(title)

    return True, links[0].replace(" ", "_")


def get_internal_links_from_article(title):
    """
    Retrieves all internal Wikipedia article links from the given article title.
    If the page is a disambiguation page, it follows the first link.
    Returns a list of article titles (as strings).
    """
    is_disambigus, link = is_disambiguation_page(title)
    if is_disambigus:
        title = link
    
    S = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"

    internal_links = []
    plcontinue = None

    while True:
        PARAMS = {
            "action": "query",
            "format": "json",
            "prop": "links",
            "titles": title,
            "plnamespace": 0,
            "pllimit": "max"
        }
        if plcontinue:
            PARAMS["plcontinue"] = plcontinue

        response = S.get(url=URL, params=PARAMS)
        data = response.json()

        pages = data["query"]["pages"]
        for page_id in pages:
            if "links" in pages[page_id]:
                for link in pages[page_id]["links"]:
                    internal_links.append(link["title"].replace(" ", "_"))

        if "continue" in data:
            plcontinue = data["continue"]["plcontinue"]
        else:
            break

    return internal_links


def remove_all_hidden_blocks(soup):
    """
    Removes all HTML elements from the BeautifulSoup object that are hidden (via 'hidden' attribute or CSS styles).
    Modifies the soup in place.
    """
    for tag in list(soup.find_all(True)):
        try:
            if "hidden" in tag.attrs:
                tag.decompose()
                continue
            style = tag.attrs.get("style", "")
            if isinstance(style, str):
                normalized = style.replace(" ", "").lower()
                if "display:none" in normalized or "visibility:hidden" in normalized:
                    tag.decompose()
        except Exception:
            continue

def get_all_visible_existing_internal_links(title, steps):
    """
    Returns all visible, existing internal Wikipedia article links from the given article title,
    excluding links that are in the 'steps' list. Only considers links in the main content area.
    """
    steps_dict = set(steps)
    url = f"https://en.wikipedia.org/wiki/{title}"
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    body_content = soup.find('div', id='bodyContent')
    for comment in body_content.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()
    for navbox in body_content.select('.mw-parser-output .navbox'):
        navbox.decompose()
    
    links = body_content.find_all("a", href=True)
    result = set()

    for link in links:
        href = link["href"]

        if not href.startswith("/wiki/"):
            continue
        if ':' in href:
            continue
        if 'new' in (link.get('class') or []):  # Link rosso
            continue

        title = unquote(href.split("/wiki/")[1]).replace(" ", "_")
        result.add(title)
    
    result = result.difference(steps_dict)
    return list(result)
