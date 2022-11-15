from bs4 import BeautifulSoup
import requests
import re


whichGpu = input('what gpu(product) do you want to search for: ')

url = f'https://www.newegg.com/p/pl?d={whichGpu}&N=4131'
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

#^ we want to figure out how many pages of results do we have
pageText = doc.find(class_='list-tool-pagination-text').strong
pages = str(pageText).split('/')[-2]
numberOfPages = int(re.findall(r'\b\d+\b', pages)[0])

items_found = {}

#^ loop through all of the pages and grab all of the elements on those pages

for page in range(1,numberOfPages+1):
    url = url = f'https://www.newegg.com/p/pl?d={whichGpu}&N=4131&page={page}'
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")
    #^ grab every item containing 3080(product)
    div = doc.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
	items = div.find_all(text=re.compile(whichGpu))

    for item in items:
        #^ we ar going to look for the name of the item the price of the item and its like
        