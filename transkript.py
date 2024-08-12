import time
import random
import csv
import requests
import datetime
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

login_url = "https://kimlik.ege.edu.tr/Identity/Account/Login?ReturnUrl=%2F"
grade_url = input("Transkript sayfası linki: ")
errorverdi = 0
username = input("Kullanıcı Adı: ")
password = input("Şifre: ")
PUSHBULLET_API_KEY = input("Pushbullet API Key: ")
PUSHBULLET_DEVICE_IDEN = input("Pushbullet Device Identification Number: ")
os.system('cls' if os.name == 'nt' else 'clear') # konsolu temizler

sayac = 0
semestercount = 0
semestercount2 = 0
semestercount3 = 1
derssayisi = 0
test1 = 0
ilksefer = 0

options = Options()
options.headless = True
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Firefox(options=options)
driver.set_page_load_timeout(30)

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
        print("Hata! Telefona bildirim yollanamadı.")
    else:
        print("Başarıyla telefona bildirim yollandı.")

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

def get_grades(driver):
    if driver.title == "Not Görüntüleme":        
        semestercount = 0
        semestercount2 = 0
        global semestercount3
        global ilkdersadi
        global ilkdevamsizlik
        global ilkyilici
        global ilkfinal
        global ilkbutunleme
        global ilksinifortalamasi
        data = []      
        sayac = 0
        while semestercount < semestercount3:
            try:
                if ilksefer == 1:
                    ilkdersadi[sayac] = driver.find_element(By.ID, f"rptGrup_ctl{semestercount:02d}_rptDers_ctl{semestercount2:02d}_tdDersAdi").text.strip()
                    ilkdevamsizlik[sayac] = driver.find_element(By.ID, f"rptGrup_ctl{semestercount:02d}_rptDers_ctl{semestercount2:02d}_tdDevamDurumu").text.strip()   
                    ilkyilici[sayac] = driver.find_element(By.ID, f"rptGrup_ctl{semestercount:02d}_rptDers_ctl{semestercount2:02d}_tdYid").text.strip()
                    ilkfinal[sayac] = driver.find_element(By.ID, f"rptGrup_ctl{semestercount:02d}_rptDers_ctl{semestercount2:02d}_divFinalNotu").text.strip()
                    ilkbutunleme[sayac] = driver.find_element(By.ID, f"rptGrup_ctl{semestercount:02d}_rptDers_ctl{semestercount2:02d}_tdBut").text.strip()
                    ilksinifortalamasi[sayac] = driver.find_element(By.ID, f"rptGrup_ctl{semestercount:02d}_rptDers_ctl{semestercount2:02d}_tdSinifOrtalamasi").text.strip()
                    print(ilkdersadi[sayac])
                    print(ilkdevamsizlik[sayac])
                    print(ilkyilici[sayac])
                    print(ilkfinal[sayac])
                    print(ilkbutunleme[sayac])
                    print(ilksinifortalamasi[sayac])
                    
                dersadidizi[sayac] = driver.find_element(By.ID, f"rptGrup_ctl{semestercount:02d}_rptDers_ctl{semestercount2:02d}_tdDersAdi").text.strip()
                devamsizlikdizi[sayac] = driver.find_element(By.ID, f"rptGrup_ctl{semestercount:02d}_rptDers_ctl{semestercount2:02d}_tdDevamDurumu").text.strip()   
                yilicidizi[sayac] = driver.find_element(By.ID, f"rptGrup_ctl{semestercount:02d}_rptDers_ctl{semestercount2:02d}_tdYid").text.strip()
                finaldizi[sayac] = driver.find_element(By.ID, f"rptGrup_ctl{semestercount:02d}_rptDers_ctl{semestercount2:02d}_divFinalNotu").text.strip()
                basarinotudizi[sayac] = driver.find_element(By.ID, f"rptGrup_ctl{semestercount:02d}_rptDers_ctl{semestercount2:02d}_tdBn").text.strip()
                butunlemedizi[sayac] = driver.find_element(By.ID, f"rptGrup_ctl{semestercount:02d}_rptDers_ctl{semestercount2:02d}_tdBut").text.strip()
                harfnotudizi[sayac] = driver.find_element(By.ID, f"rptGrup_ctl{semestercount:02d}_rptDers_ctl{semestercount2:02d}_tdHbn").text.strip()
                sinifortalamasidizi[sayac] = driver.find_element(By.ID, f"rptGrup_ctl{semestercount:02d}_rptDers_ctl{semestercount2:02d}_tdSinifOrtalamasi").text.strip()

                data.append([sayac, dersadidizi[sayac], devamsizlikdizi[sayac], yilicidizi[sayac], finaldizi[sayac], basarinotudizi[sayac], butunlemedizi[sayac], harfnotudizi[sayac], sinifortalamasidizi[sayac]])
                sayac += 1
                semestercount2 += 1                    
            except:
                semestercount += 1     
                semestercount2 = 0
    return data

def save_to_csv(data, filename):
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Sayaç', 'Ders Adı', 'Devamsızlık', 'Yıl İçi Ortalaması', 'Final Notu', 'Başarı Notu', 'Bütünleme Notu', 'Harf Notu', 'Sınıf Ortalaması'])
            writer.writerows(data)
        print(f"Veri {filename} adlı dosyaya kaydedildi.")
    except Exception as e:
        print(f"Veri {filename} adlı dosyaya kaydedilemedi. Hata: {e}")

def start():
    global ilksefer
    global sayac
    global errorverdi
    global test1
    test2 = 0
    global semestercount
    global semestercount3 
    global derssayisi
    global dersadidizi
    global devamsizlikdizi
    global yilicidizi
    global finaldizi
    global basarinotudizi
    global butunlemedizi
    global harfnotudizi
    global sinifortalamasidizi
    global ilkdersadi 
    global ilkdevamsizlik 
    global ilkyilici 
    global ilkfinal 
    global ilkbutunleme 
    global ilksinifortalamasi 

    login(driver, username, password)    
    try:
        driver.get(grade_url)
        if errorverdi == 1:
            errorverdi = 0
            send_pushbullet_notification("Site tekrar açıldı", "Çökmüştü")
        else:
            send_pushbullet_notification("Notkontrol çalışıyor.", f"Sayfa başlığı: {driver.title}")  
    except TimeoutException:
        print(f"Kod",datetime.datetime.now().strftime("%H:%M"),"anında çöktü. 30 dakika sonra tekrar başlayacak...")
        if errorverdi == 0:
            send_pushbullet_notification("Notlar sayfası çöktü", "Notlar görüntülenemiyor.")
        errorverdi = 1
        time.sleep(1800)
        start()
    time.sleep(5)
    start_time = time.time()
    current_data = get_grades(driver)
    last_data = current_data    

    while True:               
        try:
            driver.find_element(By.ID, f'rptGrup_ctl{semestercount3:02d}_rptDers_ctl00_tdDersAdi')
            semestercount3 += 1
        except NoSuchElementException:
            break

    while semestercount < semestercount3:
        try:
            driver.find_element(By.ID, f'rptGrup_ctl{semestercount:02d}_rptDers_ctl{test2:02d}_tdDersAdi')
            test2 += 1
            derssayisi += 1
        except NoSuchElementException:
            test2 = 0
            semestercount += 1

    dersadidizi = [None] * derssayisi 
    devamsizlikdizi = [None] * derssayisi
    yilicidizi = [None] * derssayisi
    finaldizi = [None] * derssayisi
    basarinotudizi = [None] * derssayisi
    butunlemedizi = [None] * derssayisi
    harfnotudizi = [None] * derssayisi
    sinifortalamasidizi = [None] * derssayisi
    ilkdersadi = [None] * derssayisi 
    ilkdevamsizlik = [None] * derssayisi
    ilkyilici = [None] * derssayisi
    ilkfinal = [None] * derssayisi
    ilkbutunleme = [None] * derssayisi
    ilksinifortalamasi = [None] * derssayisi 
    ilksefer = 1

    while True:        
        driver.get(grade_url)  
        time.sleep(3)
        current_data = get_grades(driver)
        ilksefer = 0        
        if current_data != last_data and driver.title == "Not Görüntüleme":
            driver.get(grade_url)
            get_grades(driver)            
            time.sleep(2)        
            sayac = 0
            semestercount = 0
            semestercount2 = 0
            while semestercount < semestercount3:
                try:                    
                    if devamsizlikdizi[sayac] != ilkdevamsizlik[sayac]:
                        send_pushbullet_notification(f"{dersadidizi[sayac]} adlı derste devam durumun değişti.",f"Yeni veri: {devamsizlikdizi[sayac]}")
                        ilkdevamsizlik[sayac] = devamsizlikdizi[sayac]
                    elif yilicidizi[sayac] != ilkyilici[sayac]:
                        send_pushbullet_notification(f"{dersadidizi[sayac]} adlı dersin yıl içi ortalaması değişti.",f"Yeni veri: {yilicidizi[sayac]}")
                        ilkyilici[sayac] = yilicidizi[sayac]
                    elif finaldizi[sayac] != ilkfinal[sayac]:
                        send_pushbullet_notification(f"{dersadidizi[sayac]} adlı dersin final notu değişti.",f"Yeni veri: {finaldizi[sayac]}")
                        ilkfinal[sayac] = finaldizi[sayac]
                    elif butunlemedizi[sayac] != ilkbutunleme[sayac]:
                        send_pushbullet_notification(f"{dersadidizi[sayac]} adlı dersin bütünleme notu değişti.",f"Yeni veri: {butunlemedizi[sayac]}")
                        ilkbutunleme[sayac] = butunlemedizi[sayac]
                    elif sinifortalamasidizi[sayac] != ilksinifortalamasi[sayac]:
                        send_pushbullet_notification(f"{dersadidizi[sayac]} adlı dersin sınıf ortalaması değişti.",f"{sinifortalamasidizi[sayac]} olan ortalama {ilksinifortalamasi[sayac]} olarak değişti.")
                        ilksinifortalamasi[sayac] = sinifortalamasidizi[sayac]
                    elif dersadidizi[sayac] != ilkdersadi[sayac]:
                        send_pushbullet_notification("Ders programın değişti.",f"Yeni ilk ders:{dersadidizi[sayac]}")
                        ilkdersadi[sayac] = dersadidizi[sayac]
                    sayac += 1
                    semestercount2 += 1                    
                except:
                    semestercount += 1     
                    semestercount2 = 0                
            filename = datetime.datetime.now().strftime('%d-%m-%Y-%H-%M-%S') + '-grades.csv'
            save_to_csv(current_data, filename)
            last_data = current_data
        else:
            print("Sayfada",datetime.datetime.now().strftime("%H:%M"), "tarihinde bir fark yok.")
        time.sleep(random.randint(540, 570)) 

        if time.time() - start_time > 1439:
            print(datetime.datetime.now().strftime("%H:%M"),"saatinde tekrar oturum açılıyor.")
            login(driver, username, password)
            driver.get(grade_url)
            time.sleep(3)
            start_time = time.time()

start()