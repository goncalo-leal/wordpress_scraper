import json
import requests
import urllib.request
from bs4 import BeautifulSoup

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)

    copiado de https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
url = 'https://essenciadapoesia.wordpress.com/'

r = requests.get(url, headers = headers)
soup = BeautifulSoup(r.content, features = 'lxml')

archives = soup.find('aside', class_ = 'widget_archive').find_all('a')

main_bd = {}
categories_division = {}
date_division = {}

i = 0
l = len(archives)
printProgressBar(i, l, prefix = 'Saving Poems:', suffix = 'Complete', length = 50)
for archive in archives:
    # temos a certeza que a data só aparece uma vez, por isso não é preciso verificar se já existe no dicionário (para já)
    date = archive.text
    
    i += 1
    printProgressBar(i, l, prefix = 'Scrapping Poems:', suffix = date + "     ", length = 50)

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

            if p.find_all("br").__len__() > 1:
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

dates_file.close()
cats_file.close()

l = len(main_bd.keys())
printProgressBar(0, l, prefix = 'Saving Poems:', suffix = 'Complete', length = 50)
i = 0
for poem in main_bd.keys():
    name = poem.replace(' ', '_')

    main_bd[poem]['poem_file'] = name + ".txt"
    f = open("poems/" + name + ".txt", 'w')
    f.write(poem.strip() + '\n\n')
    f.write(main_bd[poem]['poem'].strip())
    f.close()

    if main_bd[poem]['img_url']:
        urllib.request.urlretrieve(main_bd[poem]['img_url'], "imgs/" + name + ".jpg")
        main_bd[poem]['img_file'] = name + ".jpg"
    else:
        main_bd[poem]['img_file'] = None

    i += 1

    printProgressBar(i, l, prefix = 'Saving Poems:', suffix = 'Complete', length = 50)

main = json.dumps(main_bd, indent=4, sort_keys=True).encode('utf-8')
main_file.write(main)
main_file.close()