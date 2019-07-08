import requests
from parsel import Selector
import time
import pandas as pd


start = time.time()


all_images  = {}

result = []
response = requests.get('https://www.tk421.net/lotr/film/')
selector = Selector(response.text)

href_links = selector.xpath('//a/@href').getall()
del href_links[-1]


def moviename(tag):
    if('fotr' in tag):
        return 'The Fellowship of the Ring' 
    elif('ttt' in tag):
        return 'The Two Towers' 
    elif('rotk' in tag):
        return 'The Return of the King' 
    else:
        return None



txtflag = 0
for link in href_links:
    try:
        urlapp = 'https://www.tk421.net/lotr/film/' + link
        print('In page ' + urlapp)
        response1 = requests.get(urlapp)
        selector1 = Selector(response1.text)
        if response1.status_code == 200:
            former = None
            inter = []
            for i in selector1.xpath('//p'):
                _tmp = Selector(i.get())
                if(_tmp.xpath('//p/text()').get()):
                    imgurl = _tmp.xpath('//img/@src').get()
                    #tag = moviename(imgurl)
                    if(txtflag and former and imgurl and imgurl[:4]=='img/'):
                        inter = []
                        inter.append(former)
                        inter.append(imgurl)
                        inter.append(moviename(imgurl))
                        result.append(inter)
                        txtflag = 0
                        former = None

    except Exception as exp:
        print('Error navigating to link : ', link)
        print(exp)




sol = pd.DataFrame(result, columns = ['id','dialog' , 'url', 'movie']) 
sol.to_csv('Content-v0.csv', sep='|')


end = time.time()
print("Time taken in seconds : ", (end-start))
