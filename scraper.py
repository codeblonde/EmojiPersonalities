from selenium import webdriver
from time import sleep
import csv
import requests
import os

username = "username"
password = "password"

done = ""
users = "user1, user2, ..."
users = users.split(",")

driver = webdriver.Chrome()
driver.get("https://instagram.com")
sleep(2)

def login():
    driver.find_element_by_xpath("//input[@name='username']").send_keys(username)
    driver.find_element_by_xpath("//input[@name='password']").send_keys(password)
    driver.find_element_by_xpath("//button[@type='submit']").click()
    sleep(5)
    driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
    driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()

login()

description = "/html/body/div[4]/div[2]/div/article/div[2]/div[1]/ul/div/li/div/div/div[2]/span"
picture1 = "/html/body/div[4]/div[2]/div/article/div[1]/div/div[1]/div[2]/div/div/div/ul/li[2]/div/div/div[1]/div[1]/div[1]/img"
picture2 = "/html/body/div[4]/div[2]/div/article/div[1]/div/div/div[1]/div/div/img"
picture3 = "/html/body/div[4]/div[2]/div/article/div[1]/div/div[1]/div[2]/div/div/div/ul/li[2]/div/div/div/div[1]/div[1]/img"
picture4 = "/html/body/div[4]/div[2]/div/article/div[1]/div/div/div[1]/img"
picture5 = "/html/body/div[4]/div[2]/div/article/div[1]/div/div[1]/div[2]/div/div/div/ul/li[2]/div/div/div/div[1]/img"
picture6 = "/html/body/div[4]/div[2]/div/article/div[1]/div/div/div[1]/div[1]/img"


failed = 0
saved = 0

for user in users:
    saved = 0
    os.makedirs(user)
    with open('./'+user+'/'+user+'.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter= ";")

        driver.get("https://instagram.com/"+user)
        #clicking first picture
        driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div[3]/article/div[1]/div/div[1]/div[1]").click()
        sleep(5)
        while (saved < 200):
            picture_link = None
            try:
                picture_link = driver.find_element_by_xpath(picture1)
            except Exception:
                print("trying to fetch a picture.")
            try:
                picture_link = driver.find_element_by_xpath(picture2)
            except Exception:
                print("trying to fetch a picture.")
            try:
                picture_link = driver.find_element_by_xpath(picture3)
            except Exception:
                print("trying to fetch a picture.")
            try:
                picture_link = driver.find_element_by_xpath(picture4)
            except Exception:
                print("trying to fetch a picture.")
            try:
                picture_link = driver.find_element_by_xpath(picture5)
            except Exception:
                print("trying to fetch a picture.")
            try:
                picture_link = driver.find_element_by_xpath(picture6)
            except Exception:
                print("trying to fetch a picture.")
                
            if picture_link is not None:
                try:
                    pic_url = picture_link.get_attribute("src")
                    file_name = user+str(saved)+".jpg"

                    response = requests.get(pic_url)
                    file = open('./'+user+'/'+file_name, "wb")
                    file.write(response.content)
                    file.close()

                    description_text = driver.find_element_by_xpath(description).text
                    description_text = description_text.replace("\n", " ").strip() 
                    data = [user, file_name, description_text]
                    writer.writerow(data)
                    saved += 1
                    print("Data Saved: ", saved)
                except Exception:
                    print("Something went wrong")
            else:
                failed += 1
                print("Failed: ", failed)
            try:    
                driver.find_element_by_xpath("//a[contains(text(), 'Next')]").click()
            except Exception:
                print("Not enough pictures")
            sleep(7)
    
