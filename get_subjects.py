import requests
from bs4 import BeautifulSoup

page = requests.get('http://www.rating.unecon.ru/index.php?&y=2018&k=1&f=1&up=12020&s=3&g=all&upp=all&ball=hide&sort=ball')
soup = BeautifulSoup(page.text, 'html.parser')

sub = [i.text for i in soup.find(class_="upp_descr").find_all('b')]
print(sub)






