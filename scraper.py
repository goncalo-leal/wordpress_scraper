import json
import requests
import urllib.request
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
url = 'https://essenciadapoesia.wordpress.com/'

r = requests.get(url, headers = headers)
soup = BeautifulSoup(r.content, features = 'lxml')

archives = soup.find('aside', class_ = 'widget_archive').find_all('a')

main_bd = {}
categories_division = {}
date_division = {}

for archive in archives:
    # temos a certeza que a data só aparece uma vez, por isso não é preciso verificar se já existe no dicionário (para já)
    date = archive.text
    print(date)

    url = archive["href"]
    r = requests.get(url, headers = headers)
    soup = BeautifulSoup(r.content, features = 'lxml')

    articles = soup.find_all('article', class_ = 'post')

    poem_titles = []
    for item in articles:
        title = item.find({'h1': 'entry-title'}).text
        d = item.find({'time': 'entry-date'}).text
        poem_titles.append(title)

        content = item.find('div', class_ = 'entry-content')
        poem_lines = ""
        for p in content.find_all('p'):
            poem_lines += p.text
            for br in p.find_all("br"):
                poem_lines += '\n'
            poem_lines += '\n'

        img = content.find('img')
        if img:
            img = img["src"]
        else:
            img = None

        footer = item.find('footer', class_ = 'entry-meta')
        cat_span = footer.find('span', class_ = 'cat-links')
        categories = cat_span.find('a')

        cats = []
        for categorie in categories:
            cats.append(categorie)

            if categorie in categories_division.keys():
                categories_division[categorie]['quantity'] += 1
                categories_division[categorie]['poems'].append(title)
                continue
                
            categories_division[categorie] = {}
            categories_division[categorie]['quantity'] = 1
            categories_division[categorie]['poems'] = [title]

        main_bd[title] = {
            'date':             date,
            'img_url':          img,
            'poem':             poem_lines,
            'categories':       cats,
            'date_division':    d
        }
    
    date_division[date] = {'quantity': len(poem_titles), 'poems': poem_titles}

dates_file = open("date_division.json", 'wb')
cats_file = open("categories_division.json", 'wb')
main_file = open("main.json", 'wb')

dates = json.dumps(date_division, indent=4, sort_keys=True).encode('utf-8')
cats = json.dumps(categories_division, indent=4, sort_keys=True).encode('utf-8')

dates_file.write(dates)
cats_file.write(cats)

for poem in main_bd.keys():
    name = poem.replace(' ', '_')

    main_bd[poem]['poem_file'] = name + ".txt"
    f = open("poems/" + name + ".txt", 'w')
    f.write(poem)
    f.write('\n')
    f.write('\n')
    f.write(main_bd[poem]['poem'])
    f.close()

    if main_bd[poem]['img_url']:
        urllib.request.urlretrieve(main_bd[poem]['img_url'], "imgs/" + name + ".jpg")
        main_bd[poem]['img_file'] = name + ".jpg"
    else:
        main_bd[poem]['img_file'] = None


main = json.dumps(main_bd, indent=4, sort_keys=True).encode('utf-8')
main_file.write(main)

dates_file.close()
cats_file.close()
main_file.close()