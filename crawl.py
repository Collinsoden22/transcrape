# Write a script to scrape web pages one level deep recursively, for each page, translate text inside HTML tags to Hindi and create a file with it, linking css, javascript and images files from assets directory

import requests
from bs4 import BeautifulSoup
import re
from google_trans_new import google_translator
import os

# Set the base URL for the web page to scrape 
base_url = 'https://www.classcentral.com/' 
# Create a directory to store assets 
assets_dir = 'assets/' 
# Create a directory to store translated pages 
translated_pages_dir = 'pages/' 

 # Create a list of URLs to scrape recursively 
urls_to_scrape = requests.get(base_url, headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

# Get all href elements
all_hrefs = [a.get('href') for a in BeautifulSoup(urls_to_scrape.content, 'html.parser').find_all('a')]

# print(all_hrefs)
 # Create a translator object for translating text to Hindi  
translator = google_translator()  

 # Loop through each URL in the list and scrape it recursively one level deep  
for url in all_hrefs:  

    # Make an HTTP request and get the response from the server  
    response = requests.get("https://www.classcentral.com/" + str(url), headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})  

    # Parse HTML content from response using BeautifulSoup library  
    soup = BeautifulSoup(response.content, 'html.parser')  

    # Find all links on the page and add them to the list of URLs to scrape recursively one level deep  
    # for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):  

    #     if link['href'] not in urls_to_scrape:  

    #         urls_to_scrape.append(link['href'])  

    # Find all text inside HTML tags and translate it into Hindi using Google Translate API    
    for tag in soup.findAll(text=True):
        if tag != "":
            translatedText = translator.translate(tag, lang_src='en', lang_tgt='hi')

            soup.body.replaceWithChildren(BeautifulSoup(translatedText.text, 'html.parser'))    

    # Find all css, javascript and images files on the page and save them in assets directory    
    for link in soup.findAll('link', attrs={'href': re.compile("^http://")}):    

        filename = os.path.basename(link['href'])    

        r = requests.get(link['href'], stream=True)    
