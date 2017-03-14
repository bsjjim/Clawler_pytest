from bs4 import BeautifulSoup
from datetime import  datetime
import requests
import sys
import json

def newsCrawling(hpurl, url):
    linklist = []

    source_code = requests.get(url)
    # print(source_code.encoding)
    # print(source_code.text.encode('utf-8'))
    # print(type(source_code.text))
    # print(source_code.text.encode('ISO-8859-1'))
    soup = BeautifulSoup(source_code.text.encode('ISO-8859-1'), "html.parser")
    # soup.decode('utf-8')
    # print(type(soup))
    # for div in soup.findAll("div", {"class":"list"}):
    for div in soup.findAll("h4", {"class": "article-title"}):
        div_text = div.find('a')['href']
        linklist.append(div_text)
        # print (div_text)

    data = {}
    i = 1
    for link in linklist :
        linkurl = url + link

        news = newsCrawlingDatail(linkurl)
        contents = {}
        contents['url'] = linkurl
        contents['news'] = news
        # print(news)
        # print(i)
        data[i] = contents
        i += 1

    print(json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False))

    dt = datetime.now()
    filename = dt.strftime('%Y%m%d%H%M%S') + ".txt"

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)

def newsCrawlingDatail(linkurl):
    source_code = requests.get(linkurl)
    soup = BeautifulSoup(source_code.text.encode('ISO-8859-1'), "html.parser")
    rval = ""
    for div in soup.findAll("div", {"class": "text"}):
        div_text = div.text
        rval += (div_text)

    return rval

if __name__ == "__main__" :

    hpurl = 'http://www.hani.co.kr'
    url = 'http://www.hani.co.kr/arti/list.html'
    newsCrawling(hpurl, url)
