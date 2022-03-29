from selenium import webdriver
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import random


def get_time_gmt3(date):
    split_date = date.split(":")
    hour = int(split_date[0])
    hour = (hour + 3) % 24
    if hour < 10:
        hour = "0" + str(hour)
    else:
        hour = str(hour)

    return hour + date[2:]


ser = Service("D:\Desktop\Coding\chromedriver.exe")
op = webdriver.ChromeOptions()
op.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
s = webdriver.Chrome(service=ser, options=op)
link = sys.argv[1]
problem_name = sys.argv[2]
username_email = sys.argv[3]
pwd = sys.argv[4]

s.get(link)
s.implicitly_wait(8)

username_form = s.find_element(By.XPATH, '//*[@id="LoginInput_UserNameOrEmailAddress"]')
username_form.click()
time.sleep(1)
username_form.send_keys(username_email)
time.sleep(1)

pwd_form = s.find_element(By.XPATH, '//*[@id="LoginInput_Password"]')
pwd_form.click()
time.sleep(1)
pwd_form.send_keys(pwd)
time.sleep(1)

login_button = s.find_element(By.XPATH, '/html/body/div/div/div/div/div/div/form/button')
login_button.click()
time.sleep(random.randint(7, 10))

submission_table = s.find_element(By.XPATH, '//*[@id="contest-submissions-table"]/tbody')
f = open("results.txt", "w")
page_count = int(s.find_element(By.XPATH, '//*[@id="contest-submissions-table_paginate"]/ul/li[8]/a').text)
page_counter = 0
while page_counter != page_count:
    tr_ind = 1
    for row in submission_table.find_elements(By.CSS_SELECTOR, 'tr'):
        table_elements = row.find_elements(By.TAG_NAME, 'td')
        problem_name_temp = table_elements[2].text

        if problem_name_temp == problem_name:
            view_link = s.find_element(By.XPATH, f'//*[@id="contest-submissions-table"]/tbody/tr[{tr_ind}]/td[8]/a').get_attribute('href')
            submitted_by = table_elements[3].text
            time_of_date = get_time_gmt3(table_elements[4].text.split()[1])
            state = table_elements[6].text
            f.write(f"{time_of_date}\t{submitted_by}\t{state}\t{view_link}\n")

        tr_ind += 1

    next_button = s.find_element(By.CLASS_NAME, 'next')
    page_counter += 1
    next_button.click()
    time.sleep(random.uniform(3.5, 5))

f.close()
s.close()
