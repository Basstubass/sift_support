from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from time import sleep
import urllib.request as req
from lxml import etree
import requests
import datetime
import locale

# 自身のユーザー情報
user_id = "#####"
passcode = "####"
manth = [1,2,3,4,5,6,7,8,9,10,11,12]
manth_num = str(input("何月のシフトを調整しますか(整数のみで入力): "))

browser = webdriver.Chrome(executable_path='/Users/suitatsubasa/Desktop/dev/py/chromedriver')
# シフト管理ツール　サイト名
Otasuke = "https://sso.otasuke-part.jp/auth/realms/kspart/protocol/openid-connect/auth?client_id=staff-site&redirect_uri=https%3A%2F%2Fstaff.otasuke-part.jp&state=3ea8cbc3-2c10-494d-83b6-e219290cfedb&response_mode=fragment&response_type=code&scope=openid&nonce=d09d70f1-6035-4ae3-85ef-8715c6e82d92"
browser.get(Otasuke)

element = browser.find_element_by_id('username')
element.clear()
element.send_keys(user_id)

element = browser.find_element_by_id('password')
element.clear()
element.send_keys(passcode)

login_onclick = browser.find_element_by_id('kc-login')
login_onclick.click()

sleep(3)

manth_ber = browser.find_element_by_xpath("/html/body/app-root/div/sp-shift-table-header/header/sp-header/span[2]/sp-header-contents/div[1]/span[2]")
manth_ber.click()

for i in range((len(manth))):
    manth_num = int(manth_num)
    if manth[i] == manth_num:
        manth_num = str(manth_num)
        manth_select = browser.find_element_by_xpath("/html/body/app-root/div/sp-shift-table-header/header/sp-header/span[2]/sp-header-contents/div[2]/div[2]/div[2]/div[" + manth_num + "]")
        manth_select.click()

page_source = browser.page_source
soup = BeautifulSoup(page_source, 'html.parser')
week_day = soup.select('.day-of-week')

week_list = []
for i in week_day:
    week_list.append(i.string)
week = week_list
week_lenght = len(week)
for i in range(week_lenght):
    days = i+1
    dt = datetime.datetime(2021, int(manth_num), days)
    locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
    days_of_week = dt.strftime('%a')
    print(days_of_week)

    if week[i] == "水" and "金":
        days_url = "https://staff.otasuke-part.jp/hope/2ce1069d-3126-435f-afc1-0765c5228247/d2021"+ str(manth_num) + str(days) +"#cdc5eb6a-ab81-4f0b-9c24-ee22f9d075c1"
        browser.get(days_url)
        sleep(3)

        job_status = browser.find_element_by_xpath("/html/body/app-root/div/sp-hope-shift/div/main/form/sp-hope-shop/div/div[2]/div[2]/div[2]/div[1]/select")
        select = Select(job_status)
        select.select_by_value('WORK')

        sleep(3)

        job_time_start = browser.find_element_by_xpath("/html/body/app-root/div/sp-hope-shift/div/main/form/sp-hope-shop/div/div[2]/div[2]/div[2]/div[2]/div/select[1]")
        time_start_select = Select(job_time_start)
        time_start_select.select_by_value('18')
        sleep(3)
        
        job_time_start = browser.find_element_by_xpath("/html/body/app-root/div/sp-hope-shift/div/main/form/sp-hope-shop/div/div[2]/div[2]/div[2]/div[2]/div/select[3]")
        time_start_select = Select(job_time_start)
        time_start_select.select_by_value('21')
        sleep(3)

        save_button = browser.find_element_by_xpath("/html/body/app-root/div/sp-hope-shift/div/footer/div[2]/sp-save-button/button")
        save_button.click()

        sleep(3)
        
        Alert(browser).accept()

    elif week[i] == "日":
        days_url = "https://staff.otasuke-part.jp/hope/2ce1069d-3126-435f-afc1-0765c5228247/d2021"+ str(manth_num) + str(days) +"#cdc5eb6a-ab81-4f0b-9c24-ee22f9d075c1"
        browser.get(days_url)
        sleep(3)

        job_status = browser.find_element_by_xpath("/html/body/app-root/div/sp-hope-shift/div/main/form/sp-hope-shop/div/div[2]/div[2]/div[2]/div[1]/select")
        select = Select(job_status)
        select.select_by_value('WORK')
        sleep(3)

        save_button = browser.find_element_by_xpath("/html/body/app-root/div/sp-hope-shift/div/footer/div[2]/sp-save-button/button")
        save_button.click()

    else:
        days_url = "https://staff.otasuke-part.jp/hope/2ce1069d-3126-435f-afc1-0765c5228247/d2021"+ str(manth_num) + str(days) +"#cdc5eb6a-ab81-4f0b-9c24-ee22f9d075c1"
        browser.get(days_url)
        sleep(3)
        job_status = browser.find_element_by_xpath("/html/body/app-root/div/sp-hope-shift/div/main/form/sp-hope-shop/div/div[2]/div[2]/div[2]/div[1]/select")
        select = Select(job_status)
        select.select_by_value('OFF')
        sleep(3)    
        save_button = browser.find_element_by_xpath("/html/body/app-root/div/sp-hope-shift/div/footer/div[2]/sp-save-button/button")
        save_button.click()
        sleep(3)
        Alert(browser).accept()