from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from PIL import Image, ImageTk
import time
import tkinter as tk
import re
from Browser.browser_set import create_driver
import sys
import yaml

sys.setrecursionlimit(190000)
with open('.yaml', 'r') as config_file:
    config= yaml.safe_load(config_file)

groupp = config['group']

chet_count = 0

def skrinLoader(driver):
    driver.save_screenshot("screenshot.png")

#Основная функиця дла мониторинга группы
def Analiz(driver,const):
    try:
        target_element = driver.find_element(By.CSS_SELECTOR, '.message-date-group.first-message-date-group')
    except:
        time.sleep(2)
        print('Ошибка получения послед. сообщения. Сморите скриншот')
        
        driver.save_screenshot("last_bad.png")
        return Analiz(driver,const)

   

    current_elements = target_element.find_elements(By.XPATH, './*')
    current_count = len(current_elements)
    if const < current_count:
        last_added_element = current_elements[-1]  # Получаем последний элемент

        text_post = last_added_element.text

        patterns = config['stop_list']

        #поиск по стоп листу
        combined_pattern = '|'.join(patterns)
        matches_stop = re.findall(combined_pattern, text_post)
        matches_groupp = re.findall(r'@(\w+)', text_post)

        if(matches_stop !=  [] ):
            print('Пропускаем')
            time.sleep(1)
            Analiz(driver, current_count)
        else:
        # Модуль подписки на группу
            for group in matches_groupp:
                try:
                    last_added_element.find_element("xpath", f"//a[@class='text-entity-link' and text()='@{group}']").click()
                except:
                    print(f'Не найдена группа @{group} , повторный поиск...')
                    try:
                        time.sleep(1)
                        driver.find_element("css selector", f'a[href="{groupp}"]').click()
                        time.sleep(2)
                        last_added_element.find_element("xpath", f"//a[@class='text-entity-link' and text()='@{group}']").click()
                    except:
                        print(f'Не найдена группа @{group} , работа комплеска прервана смотрите скрин с ошибкой')
                        driver.save_screenshot("last_bad.png")
                        return

                time.sleep(5)
                try:
                    driver.find_element(By.CSS_SELECTOR, ".header-tools .Button.tiny.primary.fluid").click()
                    time.sleep(1)
                    print(f'Подписались на @{group}')
                    driver.find_element("css selector", f'a[href="{groupp}"]').click()
                    driver.find_element("css selector", f'a[href="{groupp}"]').click()
                except:
                    print(f'Уже подписаны на @{group}')
                    time.sleep(1)
                    driver.find_element("css selector", f'a[href="{groupp}"]').click()
                    driver.find_element("css selector", f'a[href="{groupp}"]').click()
                    time.sleep(1)
        
        #МОДУЛЬ РАБОТЫ С WEB-приложением
        time.sleep(5)
        try:
            last_added_element.find_element(By.CSS_SELECTOR, 'div.InlineButtons div.row button.Button.tiny.primary.has-ripple').click()
        except:
            last_added_element.find_element("xpath", f"//a[@class='text-entity-link' and text()='@{group}']").click()
            time.sleep(1)
            print('Ошибка запуска веб приложения! Попытка 2')
            time.sleep(2)
            try:
                 last_added_element.find_element(By.CSS_SELECTOR, 'div.InlineButtons div.row button.Button.tiny.primary.has-ripple').click()
            except:
                print('Ошибка запуска веб приложения! ')
                return
            driver.save_screenshot("last_bad.png")
            return
        time.sleep(7)
        try:
            driver.find_element(By.CSS_SELECTOR, 'button.Button.confirm-dialog-button.default.primary.text').click()
        except:
            pass
        time.sleep(5)
        try:
            driver.find_element(By.XPATH, "//button[text()='Enter Giveaway']").click()
            time.sleep(1)
            try:
                driver.find_element(By.XPATH, "//button[@aria-label='Close']").click()
            except:
                pass
        except:
            print('Ошибка регистрации в раздаче!Смотрите скрин')
            driver.save_screenshot("last_bad.png")
            try:
                driver.find_element(By.XPATH, "//button[@aria-label='Close']").click()
            except:
                pass

    time.sleep(1)
    driver.find_element("css selector", f'a[href="{groupp}"]').click()
    skrinLoader(driver)
    return Analiz(driver, current_count)

#модуль авторизации с переходом в группу
def aut(driver):
    skrinLoader(driver)
    try:   
        driver.find_element("id", "auth-qr-form")
    except :
        print("Авторизация прошла успешнo!")
        root.destroy()
        time.sleep(4)
        try:
            element = driver.find_element("css selector", f'a[href="{groupp}"]')
            element.click()
        except:
            print('Ошибка группа не найдена!!!Повторяем поиск')
            time.sleep(4)
            try:
                element = driver.find_element("css selector", f'a[href="{groupp}"]')
                element.click()
            except:
                print('Ошибка группа не найдена!!!')
                skrinLoader(driver)
                return

        time.sleep(1)
        element.click()
        time.sleep(3)
        Analiz(driver,0)


       
    new_image = Image.open("screenshot.png")

    new_photo = ImageTk.PhotoImage(new_image)

    # Обновляем изображение в метке
    label.config(image=new_photo)
    label.image = new_photo  # Сохраняем ссылку на изображение

    # Запускаем функцию снова через 5000 мс (5 секунд)
    root.after(500, lambda: aut(driver))

root = tk.Tk()
root.title("Авторизация")
width = 450  # Ширина окна
height = 600  # Высота окна
root.geometry(f"{width}x{height}")

driver = create_driver()

time.sleep(4)
skrinLoader(driver)



# Загружаем начальное изображение
image = Image.open("screenshot.png")

photo = ImageTk.PhotoImage(image)

# Создаем метку для отображения изображения
label = tk.Label(root, image=photo)
label.image = photo  # Сохраняем ссылку на изображение
label.pack()

# Запускаем первую проверку сразу
aut(driver)

root.mainloop()

# Закрытие браузера
driver.quit()
