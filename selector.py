from copy import copy
import sys
import json
import getopt
import shutil, os
from docx import Document
from datetime import datetime

months = {
    "Janeiro": "January",
    "Fevereiro": "February",
    "Março": "March",
    "Abril": "April",
    "Maio": "May",
    "Junho": "June",
    "Julho": "July",
    "Agosto": "August",
    "Setembro": "September",
    "Outubro": "October",
    "Novembro": "November",
    "Dezembro": "December"
}

def get_total():
    f = open('./main.json')
    poems = json.load(f)
    f.close()

    print(f"Total: {len(poems)}")

def order_by_date(poems):
    print("Ordering by date...")

    new_dict = {}
    for poem in poems:
        date_time_str = poems[poem]["date_division"]
        date = date_time_str.split(" ")
        date_time_obj = datetime.strptime(months[date[0]] + " " + date[1] + " " + date[2], '%B %d, %Y').timestamp()

        new_dict[poem] = [int(round(date_time_obj)), poems[poem]["poem_file"]]

    sorted_dict = {k: v for k, v in sorted(new_dict.items(), key=lambda item: item[1][0])}

    return sorted_dict

def copy_to_destiny(poems, destiny):
    print("Copying files to destiny directory...")

    for poem in poems:
        shutil.copy(f"./poems/{poems[poem]['file']}", destiny)

def create_word_file(poems, destiny):
    print("Creating word file...")

    document = Document()
    for poem in poems:            
        with open(f"./poems/{poems[poem]['file']}", "r") as read_file:
            document.add_paragraph(read_file.read().strip() + "\n\n\n")
        document.add_page_break()

    document.save(f'{destiny}.docx')

def main(argv):
    output_dir = ''
    n = 0
    try:
        opts, args = getopt.getopt(argv,"htn:d:",["n=","dir=", "help", "total"])
    except getopt.GetoptError:
        print('selector.py -n <number of poems> -d <output directory>')
        sys.exit(2)

    if len(opts) == 0:
        print('selector.py -n <number of poems> -d <output directory>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('selector.py -n <number of poems> -d <output directory>')
            sys.exit()

        elif opt in ("-n", "--n"):
            if not arg.isdigit():
                print("Number of poems must be a number")
                sys.exit(2)
            n = int(arg)

        elif opt in ("-d", "--dir"):
            output_dir = arg
            
        elif opt in ("-t", "--total"):
            get_total()
            sys.exit(0)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    f = open('./main.json')
    poems = json.load(f)
    f.close()

    sorted_dict = order_by_date(poems)

    print(type(n))

    to_save = {}
    i = 1
    for poem in sorted_dict.keys():
        to_save[poem] = {
            'name': poem,
            'date': poems[poem]["date_division"],
            'file': poems[poem]["poem_file"]
        }
        
        if i == n:
            print(i)
            break

        i += 1
    print(i)

    copy_to_destiny(to_save, output_dir)

    with open("sorted.json", "w") as write_file:
        json.dump(to_save, write_file, indent=4, ensure_ascii=False)

    create_word_file(to_save, output_dir)

if __name__ == "__main__":
   main(sys.argv[1:])