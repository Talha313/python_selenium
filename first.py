# pip install pyvirtualdisplay selenium
from selenium import webdriver
import xlrd
from xlrd import open_workbook
import xlwt

from selenium.webdriver.common.keys import Keys
import time
import requests
from bs4 import BeautifulSoup

item_list = []
def content():
    driver = webdriver.Chrome()
    # driver.get("http://www.python.org")
    driver.get("https://www.amazon.com/")
    assert "Amazon" in driver.title
    elem = driver.find_element_by_name("field-keywords")
    elem.clear()
    elem.send_keys("697574-B21")
    elem.send_keys(Keys.RETURN)
    # print(html)
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    first_row = ['Tag', 'Title', 'Brand']
    item_list.append(first_row)

    try:
        pre_tag='https://www.amazon.com'
        html = driver.page_source
        main_div = soup.find("div", attrs={"class": "nav_redesign s-left-nav-rib-redesign s-span-page"})
        # print(main_div.prettify())
        ul_sopn = main_div.find("ul", {"class": "s-result-list s-col-1 s-col-ws-1 s-result-list-hgrid s-height-equalized s-list-view s-text-condensed s-item-container-height-auto"})
        # print(ul_sopn)
        li_spon = ul_sopn.find("li", {"class": "AdHolder"})
        tag = str(li_spon.find("a", attrs={"class": "a-link-normal a-text-normal"})['href'])
        tag=pre_tag+tag
        brand = str(li_spon.find("div", {"class": "a-row a-spacing-none"}).text)
        title = str(li_spon.find("h2").text)
        new_title = title.replace("[Sponsored]", "")
        newbrand = brand.replace("by", "")
        values_list = []
        values_list.append(tag)
        values_list.append(new_title)
        values_list.append(newbrand)
        item_list.append(values_list)
        # print(tag)
        # print(newbrand)
        # print(new_title)
        #   print(item_list)
        li_sim = ul_sopn.find_all("li", {"class": "s-result-item celwidget "})
        for item in li_sim:
            values_list = []
        # print(item.prettify())
        # break

            tag_sim = str(item.find("a", attrs={"class": "a-link-normal a-text-normal"})['href'])
            brand_sim = str(item.find("div", {"class": "a-row a-spacing-none"}).text)
            div_fix = item.find("div", {"class": "a-row a-spacing-none scx-truncate-medium sx-line-clamp-2"})
        # print(div_fix.prettify())
        # break
            title_sim = str(div_fix.find("h2").text)
        # print(title_sim)
            newbrand_sim = brand_sim.replace("by", "")
            values_list.append(tag_sim)
            values_list.append(title_sim)
            values_list.append(newbrand_sim)
            item_list.append(values_list)
    except Exception as e:
        print(e)
    finally:
        driver.close()

    print(item_list)
def write():

    try:
        book = xlwt.Workbook()
        sheet = book.add_sheet(sheetname='sheet1')
        for i in range(0, 4):
            for j in range(0, 3):
                sheet.write(i, j, item_list[i][j])
        book.save('output.xls')
    except Exception as e:
        print(e)

if __name__ == '__main__':

    content()
    write()
    print(len(item_list))
