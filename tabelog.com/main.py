from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
from webdriver_manager.chrome import ChromeDriverManager

def available_checker(xpath):
    try:
        test = webdriver.find_element("xpath", xpath).text
    except:
        test = "N/A"
    else:
        test = webdriver.find_element("xpath", xpath).text
    
    return test


# URL of search result page of Tabelog.com
url = "https://tabelog.com/rstLst/?vs=1&sa=&sk=&lid=top_navi1&vac_net=&svd=20220811&svt=2100&svps=2&hfc=1&sw="
webdriver = webdriver.Chrome(ChromeDriverManager().install())
webdriver.get(url)

page_results = webdriver.find_elements("xpath", "//a[@class='list-rst__rst-name-target cpy-rst-name']")
for result in page_results:
    link = result.get_attribute("href")
    webdriver.switch_to.new_window('tab')
    webdriver.get(link)
    #Get telephone number
    tel_num = available_checker("//p[@class='rstdtl-side-yoyaku__tel-number']")
    #Get name of restaurant
    name_res = available_checker("//h2[@class='display-name']")
    #Get number of reviews
    comment = available_checker("//em[@class='num']")
    #Checks whether the restaurant is official or not
    try:
        official = webdriver.find_element("xpath", "//p[@class='owner-badge__icon']").text
    except:
        official = "非公式"
    else:
        official = webdriver.find_element("xpath", "//p[@class='owner-badge__icon']").text
    #Get average price spend during dinner
    night = available_checker("//p[@class='rdheader-budget__icon rdheader-budget__icon--dinner']//span[@class='rdheader-budget__price']")
    #Get average price spend during lunch
    lunch = available_checker("//p[@class='rdheader-budget__icon rdheader-budget__icon--lunch']//span[@class='rdheader-budget__price']")
    #Get the overal review score
    rate = available_checker("//span[@class='rdheader-rating__score-val-dtl']")
    print(name_res, tel_num, comment, official, night, lunch, rate)
    webdriver.close()
    webdriver.switch_to.window(webdriver.window_handles[0])
