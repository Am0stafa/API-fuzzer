from bs4 import BeautifulSoup
import requests
import re


whichProduct = input('what product do you want to search for: ')

url = f'https://www.newegg.com/p/pl?d={whichProduct}&N=4131'
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

#^ we want to figure out how many pages of results do we have
pageText = doc.find(class_='list-tool-pagination-text').strong  # type: ignore
pages = str(pageText).split('/')[-2]
numberOfPages = int(re.findall(r'\b\d+\b', pages)[0])

items_found = {}

#^ loop through all of the pages and grab all of the elements on those pages

for page in range(1,numberOfPages+1):
    url = url = f'https://www.newegg.com/p/pl?d={whichProduct}&N=4131&page={page}'
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")
    #^ grab every item containing 3080(product)
    div = doc.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
    items = div.find_all(text=re.compile(whichProduct))  # type: ignore

    for item in items:
        #^ we ar going to look for the name of the item and the price of the item and its link
        parent = item.parent
        if parent.name != "a":
            continue
            
        link = parent['href']
        next_parent = item.find_parent(class_="item-container") #^ to locate certain parent:looks for any ancestor in the tree that has a specific class name
        try:
            price = next_parent.find(class_="price-current").find("strong").string
            items_found[item] = {"price": int(price.replace(",", "")), "link": link}
        except:
            pass
         
#* to sort a dictionary in python we need to first convert it to a list, sort the list then turn it back to a dictionary 
sorted_items = sorted(items_found.items(), key=lambda x: x[1]['price'])

for item in sorted_items:
	print(item[0])
	print(f"${item[1]['price']}")
	print(item[1]['link'])
	print("-------------------------------")