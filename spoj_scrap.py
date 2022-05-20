#config
username = "USERNAME" # fill
password = "PASSWORD" # fill
#endconfig

import mechanize
from bs4 import BeautifulSoup
import urllib
import http.cookiejar 
import os

current_directory = os.getcwd()
final_directory = os.path.join(current_directory, r'output')
if not os.path.exists(final_directory):
   os.makedirs(final_directory)

cj = http.cookiejar.CookieJar()
br = mechanize.Browser()
br.set_cookiejar(cj)
br.open("https://www.spoj.com/login/")

br.select_form(nr=0)
br.form['login_user'] = username
br.form['password'] = password
br.submit()
res =br.response().read()
br.open("https://pl.spoj.com/users/"+username+"/")
res =br.response().read()

soup = BeautifulSoup(res)
table = soup.findAll("table")[1]
hrefs = [(item['href'],item.getText()) for item in table('a')]
for href,name in hrefs:
    br.open("https://pl.spoj.com/"+href)
    res = br.response().read()
    soup = BeautifulSoup(res)
    code_link = soup.find("a",title="Edit source code")
    br.open("https://pl.spoj.com"+code_link['href'])
    print("https://pl.spoj.com"+code_link['href'])
    res = br.response().read()
    soup = BeautifulSoup(res)
    code = soup.find("textarea")
    with open("output/"+name+".cpp","w") as f:
        f.write(code.getText())