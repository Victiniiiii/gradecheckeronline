import time
import datetime
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import os

login_url = "https://kimlik.ege.edu.tr/Identity/Account/Login?ReturnUrl=%2F"
grade_url = "https://kimlik.ege.edu.tr/Redirect/Redirect?AppEncId=z3Td%2Fth1x8vcvHw%2BDyN0G7GVy9eklCUQxjzDjMFwZaI%3D"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=chrome_options)

username = input("Enter your username: ")
password = input("Enter your password: ")
PUSHBULLET_API_KEY = input("Enter your Pushbullet API Key: ")
PUSHBULLET_DEVICE_IDEN = input("Enter your Pushbullet Device Identification Number: ")
os.system('cls' if os.name == 'nt' else 'clear')

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
    current_html = driver.page_source
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    if current_html != initial_html and driver.title == "Not Görüntüleme":
        print(f"Galiba bir notun değişti !!!", current_time , driver.title)
        send_pushbullet_notification(f"Galiba bir notun değişti !!!", f"Sayfa başlığı: {driver.title}")
        initial_html = current_html
    elif driver.title != "Not Görüntüleme":
        send_pushbullet_notification(f"Sanırsam site çöktü hehe", f"Sayfa başlığı: {driver.title}")
    else:
        print(f"No changes detected at", current_time , driver.title)

try: 
    login(driver, username, password)
    driver.get(grade_url)
    time.sleep(5)
    initial_html = driver.page_source
    start_time = time.time()
    send_pushbullet_notification("Gradechecker çalışıyor.", f"Sayfa başlığı: {driver.title}")

    while True:
        check_for_changes(driver, initial_html)
        driver.get(grade_url)
        time.sleep(random.randint(480, 540))

        if time.time() - start_time > 1439:  # Re-login every 1439 seconds
            print("Re-logging in!")
            login(driver, username, password)
            driver.get(grade_url)
            time.sleep(5)
            start_time = time.time()

except Exception as e:
    send_pushbullet_notification("Script Error", f"An error occurred: {str(e)}")
    raise  # Re-raise the exception to see the error in the log
