import requests
from bs4 import BeautifulSoup


page = requests.get('http://www.rating.unecon.ru/index.php?&y=2018&k=1&f=1&up=12020&s=3&g=all&upp=all&ball=hide&sort=ball')
soup = BeautifulSoup(page.text, 'html.parser')

students_info_list = soup.tbody
subjects_list = [i.text for i in soup.find(class_="upp_descr").find_all('b')]

pers_points = dict()
pers_pos = dict()

for i in students_info_list:
    try:
        pers_points[i.a.text] = [j.text for j in i.find_all(class_='w50 no_mobile')]
        pers_pos[i.a.text]= i.td.text
    except Exception:
        pass

# print(pers_points)
# print(pers_pos)