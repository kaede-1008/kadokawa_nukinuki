import requests
from bs4 import BeautifulSoup
import re
import json
import collections as cl

class Book_Information:
    titlelist = []
    autherlist = []
    datelist = []
    illustlist = []

    url = 'https://www.kadokawa.co.jp/calendar/?target=&largeGenre=12'

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

    head = soup.find_all('span', {'class':'search-count'})

    for incom_date in head:
        
        year_month = re.findall('[0-9]+年[0-9]+月', incom_date.text)

    calendar = soup.find_all('div', {'class':'calendar-result-lists --islist'})

    for id in calendar:
        
        days = id.find_all('div', {'id':re.compile('date-[1-9]+')})

        for day in days:
            
            day_list = re.findall('[0-9]+', day.get('id'))
            date = year_month[0] + day_list[0] + '日'

            book_titles = day.find_all('h2', {'class':'book-title'})
            book_authers = day.find_all('ul', {'class':'book-auther'})

            for (book_title, book_auther) in zip(book_titles,book_authers) :
                book_title = re.sub('\u3000', '/', book_title.text)
                book_auther = re.sub('\xa0', '', book_auther.text)
                book_auther = re.sub('著者', '', book_auther)
                book_auther = re.sub('原作', '', book_auther)
                #book_auther = re.sub('\n', '', book_auther)
                book_auther = re.sub('\u3000', ' ', book_auther)
                
                try:
                    book_title = book_title.split(' ')

                except:
                    pass

                try:
                    book_illust = re.sub('\n', '', book_auther)
                    book_illust = book_auther.split('イラストレーター')
                    illustlist.append(book_illust[1])
                except:
                    illust_flag = True

                try:
                    book_illust = book_illust[0].split('イラスト')
                    if (illust_flag == True):
                        illustlist.append(book_illust[1])
                        illust_flag = False
                except:
                    pass
                if (illust_flag == True):
                    illustlist.append('0\n')

                titlelist.append(book_title[0])
                autherlist.append(book_auther)
                datelist.append(date)
