from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
from webdriver_manager.chrome import ChromeDriverManager

'''
This scripts takes in a file which contains a list of youtube channels and returns all the published videos for each channel
Have a list of youtube channel to be scraped in the same directory (named "list_channel.txt")
'''

#Open the list of youtube channel
f = open("list_channel.txt", "r")
channels = []
for x in f:
  print(x)
  channels.append(x)

webdriver = webdriver.Chrome(ChromeDriverManager().install())
sleep(2)
total = 0
print(channels)

# For each youtube channel
for channel in channels:
    url_list = []
    print("Channel: ", channel)
    webdriver.get(channel)
    sleep(3)
    channel_name = webdriver.find_element("xpath", "//div[@id='inner-header-container']//yt-formatted-string[@class='style-scope ytd-channel-name']").text
   
    #Scroll all the way to the page (loading more videos)
    ht = webdriver.execute_script("return document.documentElement.scrollHeight;")
    while True:
        prev_ht = webdriver.execute_script("return document.documentElement.scrollHeight;")
        webdriver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        sleep(2)
        ht=webdriver.execute_script("return document.documentElement.scrollHeight;")

        if prev_ht == ht:
            break 

    # Get all the links to the videos
    links = webdriver.find_elements("xpath", '//*[@id="video-title"]')
    for link in links:
        videourl = link.get_attribute("href")
        url_list.append(videourl)
        print(link.get_attribute("href"))
        
    #This is to process how many videos are there in a channel
    print("Total number of videos: ", channel_name, len(links))
    total = total + len(links)
    print(total)
    print("\b")
    filename = channel_name + ".txt"
    # Writing into a text file
    with open(filename, "w") as obj:
        for x in url_list:
            obj.write(x + "\n")


print(total, "× 0.5円＝ ", total*0.5)
