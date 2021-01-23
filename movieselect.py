from time import sleep
from selenium import webdriver
import webbrowser
import pyrebase
flag=0

config = {
  "apiKey": "MY FIREBASE API KEY",
  "authDomain": "projectId.firebaseapp.com",
  "databaseURL": "https://netflixremote-20291.firebaseio.com/",
  "storageBucket": "projectId.appspot.com",
}
options = webdriver.ChromeOptions()
options.add_argument("--headless")
#options.add_argument("user-data-dir=PATH/TO/MY/USER/CHROME/DATA")



def stream_handler(message):
    global flag
    if (flag==0):
        flag=1
        print("Ignored first iteration")
        return 6
    print("Let's begin")
    browser = webdriver.Chrome('.\chromedriver_win32\chromedriver.exe', options=options)
    browser.get('https://reelgood.com/roulette/netflix')
    print("Opened Chrome to reelgood")
    sleep(2)
    allgenrebutton = browser.find_element_by_xpath("//div[@class='css-9hxsqq el7la3n1']")
    allgenrebutton.click()
    print("Clicked all genre")
    selectedgenre = browser.find_elements_by_xpath("//div[@class='css-1jcnj6t el7la3n4']")[message['data']]
    selectedgenre.click()
    print("Clicked selected genre")
    spinbutton = browser.find_element_by_xpath("//button[@class='css-1lm9uo8 eyx6tna4']")
    spinbutton.click()
    print("Clicked spinbutton. Waiting for 5 seconds...")
    sleep(5)
    nameelement = browser.find_element_by_xpath("//div[@class='css-hin13p e4ghog315']")
    print(nameelement.text[:nameelement.text.find('\n')])
    watchbutton = browser.find_element_by_xpath("//button[@class='css-1fvssqh eyx6tna4']")
    watchbutton.click()
    print("Clicked watch button. Waiting 1 second...")
    #netflixbutton = browser.find_element_by_xpath("//a[@class='css-9poff3 e156vy7w11']")
    sleep(1)
    print("Finding element with URL")
    streamclass = browser.find_elements_by_xpath("//div[@class='css-1gbib28 e156vy7w3']")[0]
    netflixclass = streamclass.find_elements_by_xpath(".//*[text()='Netflix']")[0]

    netflixbutton=netflixclass.find_elements_by_xpath("./..")[0]

    url = netflixbutton.get_attribute("href") #provides link
    print("Have URL")
    print(url)
    browser.close()

    #browser.get(url)
    print("Opening browser")
    webbrowser.open(url)
    sleep(5)
    #fullscreenbutton = browser.find_elements_by_xpath("//button[@aria-label='Full screen']")
    sleep(1)
    print("Reached the end")

firebase = pyrebase.initialize_app(config)

db=firebase.database()
my_stream=db.child("GenreVal").stream(stream_handler)
print("Waiting to detect a change in database")
