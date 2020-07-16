import requests
from bs4 import BeautifulSoup as bs

def sendCookpadRequest(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
    req = requests.get(url, headers=headers)
    return req

def searchCookpad(self, ingredientsLst):
    url = "https://cookpad.com/us/search/" + "%20".join(ingredientsLst)
    # User-Agent in header
    req = sendCookpadRequest(url)
    if req.status_code == 200:
        htmlContent = req.content
    else:
        htmlContent = "Unable to make GET request"
    return htmlContent

def getRecipeLst(self, htmlContent):
    lst = []
    html = bs(htmlContent, 'html.parser')
    recipe_list = html.find_all("a", "flex items-center")
    for r in recipe_list:
        lst.append(r.get('href'))
    return lst    