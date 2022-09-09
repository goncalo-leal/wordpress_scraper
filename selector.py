import json
import shutil, os
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

f = open('./main.json')
poems = json.load(f)

new_dict = {}
for poem in poems:
    print(poems[poem]["date_division"])

    date_time_str = poems[poem]["date_division"]
    date = date_time_str.split(" ")
    print(months[date[0]] + " " + date[1] + " " + date[2])
    date_time_obj = datetime.strptime(months[date[0]] + " " + date[1] + " " + date[2], '%B %d, %Y').timestamp()

    new_dict[poem] = [int(round(date_time_obj)), poems[poem]["poem_file"]]

f.close()

sorted_dict = {k: v for k, v in sorted(new_dict.items(), key=lambda item: item[1][0])}

to_save = {}
i = 1
for poem in sorted_dict.keys():
    to_save[poem] = {
        'name': poem,
        'date': poems[poem]["date_division"],
        'file': poems[poem]["poem_file"]
    }

    shutil.copy(f"./poems/{poems[poem]['poem_file']}", "vol1")
    
    if i == 109:
        break

    i += 1

with open("sorted.json", "w") as write_file:
    json.dump(to_save, write_file, indent=4, ensure_ascii=False)