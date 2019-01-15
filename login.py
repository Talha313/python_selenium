from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from time import sleep
try:
    driver=webdriver.Chrome()
    driver.get("https://www.racingpost.com/members-club/my-account/")
    assert "My Account" in driver.title

    elem_ok=driver.find_element_by_xpath("//*[@id='CybotCookiebotDialogBodyButtonAccept']")
    elem_ok.send_keys(Keys.ENTER)
    sleep(12)

    elem1=driver.find_element_by_name("email")
    elem1.clear()
    elem1.send_keys("moliphant@me.com")
    elem1.send_keys(Keys.TAB)

    #elem1.send_keys(Keys.RETURN)

    elem2=driver.find_element_by_name("password")
    elem2.clear()
    elem2.send_keys("Circle88")
    #
    elem_sign=driver.find_element_by_xpath("//*[@id='react-rp-auth-root']/div/div[2]/div/div/div/div/form/div[4]/button")
    elem_sign.send_keys(Keys.ENTER)

   # elem_sign.send_keys(Keys.ENTER)
    sleep(40)
    driver.close()

except Exception as e:
    print(e)