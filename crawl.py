# Import Python package for scrapping

from genericpath import exists
import requests
from googletrans import Translator
from bs4 import BeautifulSoup
import os


site_url = "https://www.classcentral.com"

# Function to scrape page contents


def get_page_markup(link):
    print("Requesting site information...")
    response = requests.get(
        link, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win32; x32)"})
    # print(response)
    if response.status_code != 200:
        print("Error fetching page")
        exit()
    else:
        return response.content

# Save file here


def save_file(directory, content):
    # print("Creating file...")
    file_created = open(directory, "w")
    # print("Aligning text...")
    file_created.write(content)
    # print("Done, rounding up...")
    file_created.close()


def translate_contents(content, isIndex, language, directory):
    # Elements to search
    soup = BeautifulSoup(content, 'lxml')
    # print(soup)
    tags = ['p', 'span', 'h1', 'h2', 'h3', 'h4',
            'h5', 'h6', 'a', 'strong', 'li', 'button']
    for tag in tags:
        # print(f"Locating all text in {tag} tags")
        # Find all text in the tag selected
        all_tags = soup.find_all(tag)
        for tag_text in all_tags:
            old_text = tag_text.text.strip()
            if tag_text.text != "" and tag_text.text != " ":
                # print(f"Translating: {old_text}...")
                # if tag_text.text.parent.name not in ['script', 'style', 'link', 'head', 'title', 'a', 'meta']:
                translator = Translator()
                try:
                    # Detect language so only english is translated
                    if translator.detect(old_text).lang != language:
                        translated_text = translator.translate(
                            old_text, dest=language).text
                        if old_text != translated_text:
                            for node in soup.findAll(text=old_text):
                                node.replaceWith(translated_text)
                                # soup = soup.replace_with(old_text, translated_text)
                        else:
                            # print("Already translated, skipping...")
                            break
                        # If this doesn't work, try encoding here again before repeating the loop
                        print(f"Translated: " + translated_text)
                except:
                    # print(f"Error occured in translating {old_text} ...")
                    continue
            # else:
                # print(f"Empty text in {tag} tag, skipping...")

            tag_text = ""

    if isIndex == 0:
        print("Creating index file file...")
        file_dir = directory
    else:

        try:
            original_mask = os.umask(0)
            file_dir = os.makedirs(directory, mode=755, exist_ok=True)
        except:
            print("could not create file {directory}")
            # original_mask = os.umask(0)
        finally:
            os.umask(original_mask)
    file_dir = directory + '/index.html'
    file_saved = save_file(file_dir, soup.prettify())

    if (file_saved):
        return True
        # return soup.prettify()
    else:
        return "Unable to create file"
        exit()


print("Scrapping HTML page...")
# new_html = translate_contents(get_page_markup(site_url), 0, "hi", "index.html")

new_html = get_page_markup(site_url)

soup = BeautifulSoup(new_html, 'html.parser')

print("Saved index page, finding all 'a' tags...")
# # all_css = [css.get('src') for css in new_html.find_all('link')]
# # Download css but will be skipped for this project as all css file has been downloaded
# all_img = [css.get('src') for css in new_html.find_all('img')]
# # Download img
# all_js = [css.get('src') for css in new_html.find_all('script')]
# # Download js files


# # Find all a tag in the current file
all_hrefs = [a.get('href') for a in soup.find_all('a')]
# print(f"Found {len(all_hrefs)} links in index")
unique_hrefs = []

for href in all_hrefs:
    if any(x in href for x in ['%2', 'python: ', 'twitter', 'facebook', 'twitter', 'youtube', 'cdn', 'linkedin', 'instagram']):
        pass
    else:
        if href not in unique_hrefs:
            unique_hrefs.append(href)

# print(len(unique_hrefs))
for link in unique_hrefs:
    if link != "/":
        # print(link)
        if site_url in link:
            linkLength = len(site_url)
            link = link[linkLength:]
        if link[-1] == '/':
            link = link[:-1]
        if link[0] == '/':
            link = link[1:]
        print(site_url + '/' + link + '/index.html')
        if (exists(link + '/index.html')):
            print("File exist, skipping...")
            pass
        else:
            print("File not found, scrapping")
            # print("Scrapping link for: " + link)
            page_content = translate_contents(get_page_markup(site_url + '/' + link), 1, "hi", link)

print(f"{site_url} has been scraped one level deep")
exit()
