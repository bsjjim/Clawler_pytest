from bs4 import BeautifulSoup
from datetime import  datetime
import requests
import sys
import json

def safeunicode(s):
    try:
        return s.encode('ISO-8859-1')
    except UnicodeEncodeError:
        return s

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
    for div in soup.findAll("dl", {"class": "art_list_item"}):
        div_text = div.find('a')['href']
        linklist.append(div_text)
        # print (div_text)

    data = {}
    i = 1
    for link in linklist :
        if (link == ''):
            continue
        news = newsCrawlingDatail(link)
        contents = {}
        contents['url'] = link
        contents['news'] = news
        # print(link)
        # print(news)
        # print(i)
        data[i] = contents
        i += 1

    print(json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False))

    dt = datetime.now()
    filename = dt.strftime('%Y%m%d%H%M%S') + ".txt"

    with open(filename, 'w', encoding='UTF-8') as f:
        json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)


def newsCrawlingDatail(linkurl):
    rval = ""

    try :
        source_code = requests.get(linkurl)
        # data = source_code.text.encode('ISO-8859-1')
        data = safeunicode(source_code.text)
        soup = BeautifulSoup(data, "html.parser")

        for div in soup.findAll("div", {"class": "par"}):
            div_text = div.text
            rval += (div_text)
            #print(div_text)
            #print("############################################################################################################")
    except SystemError as e:
        print(e)

    return rval

if __name__ == "__main__" :

    hpurl = 'http://www.chosun.com/'
    url = 'http://www.chosun.com/'
    newsCrawling(hpurl, url)
