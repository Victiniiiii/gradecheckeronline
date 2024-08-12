import time
import datetime
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
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

Tarihsent = 0
Bilgsent = 0
Matstatsent = 0
Matrissent = 0
Algosent = 0
Oprsent = 0
Nesnesent = 0
Mat4sent = 0

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
    time.sleep(3)

def check_for_changes():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    global previous_title
    global Tarihsent
    global Bilgsent
    global Matstatsent
    global Matrissent
    global Algosent
    global Oprsent
    global Nesnesent
    global Mat4sent
    global Tarih
    global Bilg1
    global MatStat
    global Matris
    global Algo
    global Opr
    global Nesne
    global Mat4

    Tarih = driver.find_element(By.ID,"rptTranskript_ctl05_rptTranskriptDers_ctl00_tdBasariNotu")        
    Bilg1 = driver.find_element(By.ID,"rptTranskript_ctl05_rptTranskriptDers_ctl01_tdBasariNotu")        
    MatStat = driver.find_element(By.ID,"rptTranskript_ctl05_rptTranskriptDers_ctl02_tdBasariNotu")        
    Matris = driver.find_element(By.ID,"rptTranskript_ctl05_rptTranskriptDers_ctl03_tdBasariNotu")
    Algo = driver.find_element(By.ID,"rptTranskript_ctl05_rptTranskriptDers_ctl04_tdBasariNotu")
    Opr = driver.find_element(By.ID,"rptTranskript_ctl05_rptTranskriptDers_ctl05_tdBasariNotu")
    Nesne = driver.find_element(By.ID,"rptTranskript_ctl05_rptTranskriptDers_ctl06_tdBasariNotu")
    Mat4 = driver.find_element(By.ID,"rptTranskript_ctl05_rptTranskriptDers_ctl07_tdBasariNotu")       

    if Tarih.text.strip() and Tarihsent == 0:
        Tarih = Tarih.text.strip() 
        print("Atatürk İlkeleri ve İnkilap Tarihi II Ortalaması:",Tarih)        
        send_pushbullet_notification(f"Bir not açıklandı.", f"Tarih Ortalaması: {Tarih}")
        Tarihsent = 1
    elif Bilg1.text.strip() and Bilgsent == 0:
        Bilg1 = Bilg1.text.strip()
        print("İstatistikte Bilgisayar Uygulamaları I Ortalaması:",Bilg1)        
        send_pushbullet_notification(f"Bir not açıklandı.", f"Bilg1 Ortalaması: {Bilg1}")
        Bilgsent = 1
    elif MatStat.text.strip() and Matstatsent == 0:
        MatStat = MatStat.text.strip()
        print("Mathematical Statistics Ortalaması:",MatStat)
        send_pushbullet_notification(f"Bir not açıklandı.", f"Matstat Ortalaması: {MatStat}")
        Matstatsent = 1
    elif Matris.text.strip() and Matrissent == 0:
        Matris = Matris.text.strip()
        print("Matris Teorisi ve İstatistik Uygulamaları Ortalaması:",Matris)        
        send_pushbullet_notification(f"Bir not açıklandı.", f"Matris Ortalaması: {Matris}")
        Matrissent = 1
    elif Algo.text.strip() and Algosent == 0:
        Algo = Algo.text.strip()
        print("İstatistiksel Uygulamalar ile Algoritma Tasarımı Ortalaması:",Algo)        
        send_pushbullet_notification(f"Bir not açıklandı.", f"Algo Ortalaması: {Algo}")
        Algosent = 1
    elif Opr.text.strip() and Oprsent == 0:
        Opr = Opr.text.strip()
        print("Introduction to Operations Research Ortalaması:",Opr)        
        send_pushbullet_notification(f"Bir not açıklandı.", f"Opr Ortalaması: {Opr}")
        Oprsent = 1
    elif Nesne.text.strip() and Nesnesent == 0:
        Nesne = Nesne.text.strip()
        print("Nesne Tabanlı Programlama Ortalaması:",Nesne)        
        send_pushbullet_notification(f"Bir not açıklandı.", f"Nesne Ortalaması: {Nesne}")
        Nesnesent = 1       
    elif Mat4.text.strip() and Mat4sent == 0:
        Mat4 = Mat4.text.strip()
        print("Matematik IV Ortalaması:",Mat4)        
        send_pushbullet_notification(f"Bir not açıklandı.", f"Mat4 Ortalaması: {Mat4}")
        Mat4sent = 1
    else:
        print(current_time, "saatinde", driver.title, "başlıklı sayfada bir fark yok.","Önceki sayfa başlığı:",previous_title,"idi.")


login(driver, username, password)
driver.get(grade_url)
time.sleep(5)
start_time = time.time()

while True:
    previous_title = driver.title
    check_for_changes()       
    time.sleep(3) 
    print("Şimdilik notların:")
    if Tarihsent == 1: print("Tarih:",driver.find_element(By.ID,"rptTranskript_ctl05_rptTranskriptDers_ctl00_tdBasariNotu").text.strip(),)
    if Bilgsent == 1: print("Bilg1:",driver.find_element(By.ID,"rptTranskript_ctl05_rptTranskriptDers_ctl01_tdBasariNotu").text.strip(),)
    if Matstatsent == 1: print("Matstat:",driver.find_element(By.ID,"rptTranskript_ctl05_rptTranskriptDers_ctl02_tdBasariNotu").text.strip(),)
    if Matrissent == 1: print("Matris:",driver.find_element(By.ID,"rptTranskript_ctl05_rptTranskriptDers_ctl03_tdBasariNotu").text.strip(),)
    if Algosent == 1: print("Algo:",driver.find_element(By.ID,"rptTranskript_ctl05_rptTranskriptDers_ctl04_tdBasariNotu").text.strip(),)
    if Oprsent == 1: print("Opr:",driver.find_element(By.ID,"rptTranskript_ctl05_rptTranskriptDers_ctl05_tdBasariNotu").text.strip(),)
    if Nesnesent == 1: print("Nesne:",driver.find_element(By.ID,"rptTranskript_ctl05_rptTranskriptDers_ctl06_tdBasariNotu").text.strip(),)
    if Mat4sent == 1: print("Mat4:",driver.find_element(By.ID,"rptTranskript_ctl05_rptTranskriptDers_ctl07_tdBasariNotu").text.strip(),)
    driver.get(grade_url)    
    time.sleep(random.randint(480, 540)) 

    if time.time() - start_time > 1439:
        print("Tekrar oturum açılıyor.")
        login(driver, username, password)
        driver.get(grade_url)
        time.sleep(3)
        start_time = time.time()

