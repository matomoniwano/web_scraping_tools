from re import A
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os
import re
import requests
from bs4 import BeautifulSoup
import lxml.html
from lxml import etree
import json

webdriver = webdriver.Chrome(ChromeDriverManager().install())

# available checker for beautifulsoup attribute. Returns "-" if requested attribute is not found
def available_checker(a, b):
    try:
        test = a[b]
    except:
        test = "-"
    else:
        test = a[b]
    
    return test
# available checker for selenium xpath. return "-" if requested xpath is not found
def available_checker_t(xpath):
    try:
        test = webdriver.find_element("xpath", xpath)
    except:
        test = "-"
    else:
        test = webdriver.find_element("xpath", xpath).text
    
    return test

# a function to call the flow for selenium data scraping. This is called when beautiful soup throws an error
def selenium(url):
    webdriver.get(url)
    name_a = available_checker_t("//div[@class='BasicInfoSection__CompanyName-sc-kk2ai9-5 gklgOU']")
    # Mission
    mission_a = available_checker_t("//p[@class='TogglableTextArea__Input-sc-1qdxy12-1 eslxJH MissionSection__Origin-sc-zsxd0q-2 dxKnZN']")
    info_available = True
    try:
        basicinfo = webdriver.find_elements("xpath", "//li[@class='BasicInfoSection__ListItem-sc-kk2ai9-9 cNUmLM']")
    except:
        info_available = False
    else:
        basicinfo = webdriver.find_elements("xpath", "//li[@class='BasicInfoSection__ListItem-sc-kk2ai9-9 cNUmLM']")
        
    
    location_a = "-"
    website_a = "-"
    establishment_a = "-"
    representive_a = "-"
    members_a = "-"

    if info_available is True: 
        location_a = available_checker_t("//i[@class='BasicInfoSection__WrappedIcon-sc-kk2ai9-10 jEGzdr wt-icon wt-icon-location']/..//div[@class='BasicInfoSection__CompanyInfoDescription-sc-kk2ai9-12 dRNBeI']")
        website_a = available_checker_t("//i[@class='BasicInfoSection__WrappedIcon-sc-kk2ai9-10 jEGzdr wt-icon wt-icon-link']/..//div[@class='BasicInfoSection__CompanyInfoDescription-sc-kk2ai9-12 dRNBeI']")
        establishment = available_checker_t("//i[@class='BasicInfoSection__WrappedFaIcon-sc-kk2ai9-11 hnjfVJ fa fa-flag']/..//div[@class='BasicInfoSection__CompanyInfoDescription-sc-kk2ai9-12 dRNBeI']")
        representive = available_checker_t("//i[@class='BasicInfoSection__WrappedIcon-sc-kk2ai9-10 jEGzdr wt-icon wt-icon-person']/..//div[@class='BasicInfoSection__CompanyInfoDescription-sc-kk2ai9-12 dRNBeI']")
        members = available_checker_t("//i[@class='BasicInfoSection__WrappedFaIcon-sc-kk2ai9-11 hnjfVJ fa fa-users']/..//div[@class='BasicInfoSection__CompanyInfoDescription-sc-kk2ai9-12 dRNBeI']")
        
    

    if establishment != "-":
        establishment = establishment.replace(" に設立", "")
    if representive != "-":
        representive = representive.replace(" が創業", "")
    if members != "-":
        members = members.replace("人のメンバー", "")

    return name_a, website_a, location_a, establishment_a, representive_a, members_a, mission_a, url




links = []
names = []
pages = []
# with open("category.txt") as file_in:
#     for line in file_in:
#         links.append(line)

# with open("filename.txt", encoding="utf8") as f:
#     for name in f:
#         names.append(name)

#desired url and category
url = "https://www.wantedly.com/companies/?industry_tags%5B%5D=20"
hi = "化学・鉄鋼・製紙・素材"


page = 1
while True:
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")

    elems = soup.find_all(href=re.compile("/companies/"))

    for i in elems:
        next_link = "https://www.wantedly.com" + i.attrs['href']
        try:
            res_s = requests.get(next_link)
        except:
            links.append(i.text)
            pages.append(page)
            continue
        else:
            res_s = requests.get(next_link)
            soup_s =  BeautifulSoup(res_s.content, 'lxml')

        try:
            names = json.loads(soup_s.find("script", {"type": "application/ld+json"}).text)
        except:
            names = []
        else:
            names = json.loads(soup_s.find("script", {"type": "application/ld+json"}).text)

        name = available_checker(names, "name")
        website = available_checker(names, "sameAs")
        address = available_checker(names, "address")
        date = available_checker(names, "foundingDate")
        try:
            founder = names["founder"]["name"]
        except:
            founder = "-"
        else:
            founder = names["founder"]["name"]
        
        try:
            member = names["numberOfEmployees"]["value"]
        except:
            member = "-"
        else:
            member = names["numberOfEmployees"]["value"]
            

        mission = available_checker(names, "description")
        urll = available_checker(names, "url")
        if date is None:
            date = "-"
        if date != "-":
            date = date[:-3]
            date = date.replace("-", "/")

        if name == "-":
            name, website, address, date, founder, member, mission, urll = selenium(next_link)
        
        #apppend into an existing file
        add_data = pd.DataFrame({"項":[""], "企業名":[name], "企業HP":[website], "住所":[address], "設立":[date], "代表者名":[founder], "メンバー数":[member], "ミッション":[mission], "URL":[urll]})
        add_data.to_csv(hi + ".csv", mode='a', index=False, header=False)

        res = requests.get(url)
        soup = BeautifulSoup(res.text, "lxml")

    
    print("page", page)
    page = page + 1
    try:
        u = soup.find_all("span", {"class":"next"})
        j = u[0].find("a")
    except:
        break
    else:
        u = soup.find_all("span", {"class":"next"})
        j = u[0].find("a")
        url = "https://www.wantedly.com" + j['href']   


for i in range(len(links)):
    print("failed", pages[i], links[i])
