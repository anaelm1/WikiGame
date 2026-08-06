from bs4 import BeautifulSoup
import requests 
import re 

URL = "https://en.wikipedia.org/w/api.php"

HEADERS = {"User-Agent": "CS50WikiGame/1.0 (anaelmumtaz15@gmail.com)"}

def get_wikipedia_page(title):
    PARAMS = {
        "action": "parse", #Gets the HTML of a page
        "page": title , #This is the page's title
        "prop": "text", #Removes extra info 
        "format": "json", #The response will be a json dictionary 
        "redirects": 1, #Does the redirects
    }

    try:
        response = requests.get(URL, headers=HEADERS, params=PARAMS)
        response.raise_for_status()

        data = response.json() 
        '''The format of data is this: {
                                        "parse": {
                                            "title": "Python (programming language)",
                                            "pageid": 23862,
                                            "text": {"*": "<div class=\"mw-parser-output\"><p><b>Python</b> is a high-level...</p></div>"}
                                        }'''

        #checking to make sure page exists
        if "error" in data:
            print(f"API ERROR: {data['error']['info']}")
            return None

        pagetitle = data["parse"]["title"]
        rawhtml = data["parse"]["text"]["*"]

        return pagetitle, rawhtml

    except requests.exceptions.RequestException as e:
        print(f"Network Error: {e}")
        return None

def clean_page(raw_html):
    if not raw_html:
        return 
    soup = BeautifulSoup(raw_html, "html.parser") #converting the whole html into a soup format
    clutter_classes = [".infobox", ".navbox", ".reflist", ".reference", ".mw-editsection", ".metadata"] #tags we wanna remove
 
    for selector in clutter_classes: #loop to go over each of the clutters
        for element in soup.select(selector): #find the clutter in the html
            element.decompose() #delete it

    for a_tag in soup.find_all("a", href=True): #finding all links
        href = a_tag["href"]

        if (href.startswith("/wiki/") or href.startswith("./")) and ":" not in href: #swapping out the wiki href with my apps /play 
            if href.startswith("/wiki/"):
                article_name = href[6:]
            else:
                article_name = href[2:]    

            a_tag["href"] = f"/play?title={article_name}"
        else: 
            del a_tag["href"] #if any other kind of link, just making it plain text
            a_tag.name = "span" 

    return str(soup)    #returning the cleaned html


def random_page():
    PARAMS = {
        "action": "query",          # Tell api to fetch metadata
        "generator": "random",      # Make the fetching random
        "format": "json",           # Datatype
        "grnnamespace": 0,          # Removes weird pages and keeps only mainstream stuff
        "prop": "info|links",
        "pllimit": "max",
        "grnlimit": 1,              # One page is given 
    }

    while True:
        response = requests.get(URL, headers=HEADERS, params=PARAMS)
        data = response.json() 
        
        # Navigate through the query pages dictionary
        pages = data.get("query", {}).get("pages", {})
        if not pages:
            continue
            
        page_data = list(pages.values())[0]
        
        # Extract title, length (in bytes), and count the links
        title = page_data.get("title")
        length = page_data.get("length", 0)
        link_count = len(page_data.get("links", []))
        
        # Filter criteria: Ensure the article is enough for a good game
        if length > 22500 and link_count > 70:
            return title

def normalize(text): #To make the titles same
        if not text:
            return ""
        text = str(text).replace("_", " ").replace("–", "-").replace("-", " ")
        return re.sub(r'\s+', ' ', text).strip().lower()
