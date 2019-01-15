from selenium import webdriver
import xlrd
import pickle
import itertools
import re
from xlrd import open_workbook
import xlwt
import  random
from selenium.webdriver.common.keys import Keys
from time import sleep
import lxml
import requests
from bs4 import BeautifulSoup

session_requests = requests.session()
desktop_agents = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']


def random_headers():
    return {'User-Agent': random.choice(desktop_agents)}

def url_request():
    race_url = []
    try:
        url = "https://www.racingpost.com/racecards/"

        result = session_requests.get(url, headers=random_headers())
        print(result.ok, result.status_code)
        if (result.ok and result.status_code == 200):
            soup = BeautifulSoup(result.text, 'lxml')

            append_url="https://www.racingpost.com"
       # print(soup.prettify())
            events=soup.find_all("section", attrs={"class":"ui-accordion__row"})

            for event in events:

                races=event.find_all("a", attrs={"class":"RC-meetingItem__link"})
                for race in races:
                    race_url.append(append_url+race.get('href'))
                   # print(append_url+race.get('href'))

                break

            #print(race_url)
            return race_url

            #print("try block")
    except Exception as e:
        print(e)

def get_hroses(race_url):
    horses_url=[]
    apppend_url="https://www.racingpost.com"
    url=race_url[0]
 #   for url in race_url:
    result = session_requests.get(url, headers=random_headers())
    print(result.ok, result.status_code)
    if (result.ok and result.status_code == 200):

    #print(url)
        soup=BeautifulSoup(result.text, "lxml")
        main_div=soup.find_all("div",attrs={"class":"RC-runnerRow"})

        for a in main_div:
            horse_tag=apppend_url+a.find("a", {"class":"RC-runnerName"})['href']
            new_tag=horse_tag.replace("#race-id=719529", "/pedigree")
            #print(new_tag)
            horses_url.append(new_tag)
        # print(horses_url)
      #  for url in horses_url:
      #   with open ('url.csv',mode='wb') as f:
      #       pickle.dump(horses_url,f)
    return horses_url
    with open('url.text',mode='w') as f:
         for urls in horses_url:
                f.write('%s\n' % urls)

def login():
    try:
        driver = webdriver.Chrome()
        driver.get("https://www.racingpost.com/members-club/my-account/")
        assert "My Account" in driver.title

        elem_ok = driver.find_element_by_xpath("//*[@id='CybotCookiebotDialogBodyButtonAccept']")
        elem_ok.send_keys(Keys.ENTER)
        sleep(12)

        elem1 = driver.find_element_by_name("email")
        elem1.clear()
        elem1.send_keys("moliphant@me.com")
        elem1.send_keys(Keys.TAB)

        # elem1.send_keys(Keys.RETURN)

        elem2 = driver.find_element_by_name("password")
        elem2.clear()
        elem2.send_keys("Circle88")
        #
        elem_sign = driver.find_element_by_xpath(
            "//*[@id='react-rp-auth-root']/div/div[2]/div/div/div/div/form/div[4]/button")
        elem_sign.send_keys(Keys.ENTER)
        sleep(20)
    except Exception as e:
        print(e)

    return  driver

def horse_page(driver):
    url_list=[]
    with open('url.text',mode='r') as f :
        for line in f:
            curr=line[:-1]
            url_list.append(curr)
            break



        page=url_list[0]
        driver.get(page)
        result=session_requests.get(page,  headers=random_headers())
        print(result.ok, result.status_code)
        if (result.ok and result.status_code == 200):
            soup = BeautifulSoup(result.text, "lxml")
            soup = BeautifulSoup(driver.page_source, "lxml")
            main=soup.find("main", {"class":"pp-container"})
            horse_name= str(soup.find("h1", attrs={"class": "hp-nameRow__name"}).text)
            name_code=str(soup.find("span",{"class":"hp-nameRow__code"}).text)
            print(horse_name)
            detail_div=soup.find("div", {"class":"hp-details__data"})
            yo=str(detail_div.find("dt", {"class":"pp-definition__term"}).text)
            info=str(detail_div.find("span",{"class":"hp-details__info"}).text)
            # breader = str(soup.find("div", {"class": "pp-definition hidden-md-up"}).text)
            # trainer = str(soup.find("dt", {"class": "pp-definition__term"}).text)
            # trainer_link=str(soup.find("a", {"class": "ui-link js-popupLink"})['href'])
            # owner=str(soup.find("ul", {"class": "hp-details__owners-list"}).text)
            # div_for_sire= soup.find("div", {"class": "hp-details__section"})
            # sire=str(soup.find("dt",{"class":"pp-definition__term"}).text)
            # sire_info = str(div_for_sire.find("a", {"class": "ui-link js-popupLink hp-horseDefinition__link"})['href'])#+str(div_for_sire.find("span",{"class":"hp-horseDefinition__country"}).text)


            print(horse_name)
            print(name_code)
            print(yo,info)
            # print(breader)
            # print(trainer)
            # print(trainer_link)
            # print(trainer_info)
            # print(div_for_sire)
            # print(sire)
            # print(sire_info)
          # except Exception as e:
          #   print(e)
if __name__ == '__main__':
    # race_url=url_request()
    # print(race_url)
    # horses_url=get_hroses(race_url)
    # print(horses_url)
    driver=login()
    horse_page(driver)
