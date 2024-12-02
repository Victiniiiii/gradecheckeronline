import time
import datetime
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
import requests
import os

username = input("Please enter your username: ")
password = input("Please enter your password: ")
PUSHBULLET_API_KEY = input("Please enter your Pushbullet API Key: ")
PUSHBULLET_DEVICE_IDEN = input("Please enter your Pushbullet Device Identification Number: ")
login_url = "https://kimlik.ege.edu.tr/Identity/Account/Login?ReturnUrl=%2F"
grade_url = input("Please enter the grade page URL: ")
os.system('cls' if os.name == 'nt' else 'clear')

options = Options()
options.headless = True
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Firefox(options=options)
driver.set_page_load_timeout(60)

def send_pushbullet_notification(title, body):
    data = {
        "type": "note",
        "title": title,
        "body": body,
        "device_iden": PUSHBULLET_DEVICE_IDEN
    }
    headers = {
        "Access-Token": PUSHBULLET_API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.post('https://api.pushbullet.com/v2/pushes', json=data, headers=headers)
    if response.status_code != 200:
        print("Failed to send notification")
    else:
        print("Notification sent")

def login(driver, username, password):
    driver.get(login_url)
    time.sleep(2)  
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    username_field.send_keys(username)
    time.sleep(random.randint(1, 3))  
    password_field.send_keys(password)
    time.sleep(random.randint(1, 3)) 
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)

def check_for_changes(driver, initial_html):
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    if driver.page_source != initial_html and driver.title == "Not Görüntüleme" and previous_title == "Not Görüntüleme":
        print(f"Galiba bir notun değişti !!!", "Saat:", current_time ,"sayfa başlığı:" + driver.title+ " önceki sayfa başlığı: "+ previous_title)
        send_pushbullet_notification(f"Galiba bir notun değişti !!!", f"Sayfa başlığı: {driver.title}, önceki sayfa başlığı: {previous_title}")
        initial_html = driver.page_source
    elif driver.title != "Not Görüntüleme" and previous_title == "Starting...":
        print("Galiba uygulama başlayamadı... bir baksan ?")
        send_pushbullet_notification("Galiba uygulama başlayamadı...","bir baksan?")
    elif driver.title != "Not Görüntüleme" and previous_title == "Not Görüntüleme":
        print(f"Sanırsam site çöktü hehe", "Saat:", current_time ,"sayfa başlığı:" + driver.title+ "önceki sayfa başlığı:"+ previous_title)
        send_pushbullet_notification(f"Sanırsam site çöktü hehe", f"Sayfa başlığı: {driver.title}, önceki sayfa başlığı: {previous_title}")
    elif driver.title == "Not Görüntüleme" and previous_title != "Not Görüntüleme" and previous_title != "Starting...":
        print(f"Site geri açıldı !", "Saat: ", current_time ,"sayfa başlığı:" + driver.title+ "önceki sayfa başlığı:"+ previous_title)
        send_pushbullet_notification(f"Site geri açıldı !", f"Sayfa başlığı: {driver.title}, önceki sayfa başlığı: {previous_title}")
    else:
        print(current_time, "saatinde", driver.title, "başlıklı sayfada bir fark bulunamadı.","Önceki sayfa başlığı:",previous_title,"idi.")

try:
    login(driver, username, password)
    driver.get(grade_url)
    time.sleep(5)
    initial_html = driver.page_source
    start_time = time.time()
    send_pushbullet_notification("Gradechecker çalışıyor.", f"Sayfa başlığı: {driver.title}")

    while True:
        previous_title = driver.title
        check_for_changes(driver, initial_html)
        driver.get(grade_url)    
        time.sleep(random.randint(480, 540)) 

        if time.time() - start_time > 1439:
            print("Tekrar oturum açılıyor.")
            login(driver, username, password)
            driver.get(grade_url)
            time.sleep(5)
            start_time = time.time()

except TimeoutException:
    send_pushbullet_notification("Sanırım internette sorun var.", f"Timeout Exception")
    login(driver, username, password)
    driver.get(grade_url)
    time.sleep(5)
    start_time = time.time()

    while True:
        previous_title = driver.title
        check_for_changes(driver, initial_html)
        driver.get(grade_url)    
        time.sleep(random.randint(480, 540)) 

        if time.time() - start_time > 1439:
            print("Tekrar oturum açılıyor.")
            login(driver, username, password)
            driver.get(grade_url)
            time.sleep(5)
            start_time = time.time()

except Exception as e:
    send_pushbullet_notification("Script Error", f"An error occurred: {str(e)}")
    raise
