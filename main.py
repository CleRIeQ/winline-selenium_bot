import re

from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import NoSuchElementException, StaleElementReferenceException, \
    TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import random
import time
import keyboard
import datetime

klk = 0
options = webdriver.ChromeOptions()
ua = UserAgent().chrome
options.add_argument(f"user-agent={ua}")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("window-size=1200x600")
driver = webdriver.Chrome('chromedriver.exe', options=options)

PATH = "/Users/yourPath/Desktop/chromedriver"
bid_type = ""
basketball_bids = [50, 150, 400, 1000, 2500, 6800, 16000, 38000] #basketball_bids = [50, 100, 200, 450, 1000, 2300, 4900, 10500, 22800, 49000
hokkey_bids = [50, 100, 200, 450, 1000, 2300, 4900, 10500, 22500, 48000]  #
hokkey_bank = 90000
basketball_bank = 91000
bid_score = 0
match = 0
checker = 0
count = 0
i = 0
result = "N/G"
ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
numOfCheck = 0
today_date = datetime.date.today()
account_login = ""
account_password = ""
game_for_bids = ""
new_or_last_var = 0
numxz = 0
already_started_matches = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
table_title_p_p = ""
point = 0
ethernet_bug_fix = 0
own_bid_choice = 0


# служебные функции


def increase():
    global numOfCheck

    numOfCheck += 1
# /html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[1]/div/a[1]

def next_bid_timer():

    seconds = random.randint(7, 15)
    time.sleep(seconds)
    print("Таймер до новой ставки закончен")


def get_info():
    global account_password, account_login, game_for_bids, new_or_last_var, numxz, bid_score, own_bid_choice

    if numxz > 0:
        return 0

    numxz += 1
    account_login = input("Логин: ")
    account_password = input("Пароль: ")
    keyboard.add_hotkey('Ctrl + Z', lambda: increase())
    keyboard.add_hotkey('Ctrl + Q', lambda: driver.quit())

    while True:
        print("Введите цифру для выбора игры \n 1 - баскетбол, 2 - хоккей")
        game_num = int(input("Номер игры: "))
        if game_num == 1:
            game_for_bids = "баскетбол"
            break
        elif game_num == 2:
            game_for_bids = "хоккей"
            break
        else:
            print("Такого номера нет, попробуйте опять.")
            continue

    print("Выберите: Сумма ставок по новой - 1, продолжить с последней ставки - 2, вписать сумму в ручную - 3")
    new_or_last_var = int(input("Введите цифру: "))

    if new_or_last_var == 3:
        if game_num == 1:
            print("выберите -> 50, 150, 400, 1000, 2500, 6800, 16000, 38000 ") # 1-50, 2-100, 3-200, 4-450, 5-1000, 6-2300, 7-4900, 8-10500, 9-22800, 10-49000
        else:
            print("выберите -> 1-50, 2-100, 3-200, 4-450, 5-1000, 6-2300, 7-4900, 8-10500, 9-22800, 10-48000")
        value = int(input("Число: "))
        bid_score += value - 1
        own_bid_choice = 1


#Пари не принято
# Принять
def new_or_last():
    global game_for_bids
    global bid_score

    if new_or_last_var == 2:
        print("new_or_last_var==2")

        try:
            start_bid_sum = driver.find_element(By.XPATH,
                                                "/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[2]/wlb-bet-history/div/div[1]/table/tbody[1]/tr/td[5]/div[1]/span")
        except NoSuchElementException:
            start_bid_sum = driver.find_element(By.XPATH,
                                                "/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[2]/wlb-bet-history/div/div[1]/table/tbody[2]/tr/td[5]/div/span")

        print(start_bid_sum.text, "start bid sum text")
        if game_for_bids == "баскетбол":
            for index, element in enumerate(basketball_bids):
                if start_bid_sum.text == str(element):
                    bid_score = index + 1 # ?

        if game_for_bids == "хоккей":
            for index, element in enumerate(hokkey_bids):
                if start_bid_sum.text == str(element):
                    bid_score = index + 1


def show_games(game):
    global checker
    global point


    if game == "баскетбол":

        WebDriverWait(driver, 30, 1).until(
            lambda x: x.find_element(By.XPATH, '//*[@id="sticky-header-bottom"]/div/div[1]').is_displayed())
        panel = driver.find_element(By.XPATH, '//*[@id="sticky-header-bottom"]/div/div[1]')
        WebDriverWait(panel, 30, 1).until(
            lambda x: x.find_element(By.CSS_SELECTOR, '[title="Баскетбол"]').is_displayed())
        basketball = panel.find_element(By.CSS_SELECTOR, '[title="Баскетбол"]')
        if "filter-active" not in basketball.get_attribute("class"):
            basketball.click()
            time.sleep(2)


    driver.execute_script("window.scrollTo(0, 50)")
    driver.execute_script("window.scrollTo(0, 0)")

    if game == "хоккей":

        WebDriverWait(driver, 10, 1).until(
            lambda x: x.find_element(By.XPATH, '//*[@id="sticky-header-bottom"]/div/div[1]').is_displayed())
        panel = driver.find_element(By.XPATH, '//*[@id="sticky-header-bottom"]/div/div[1]')
        WebDriverWait(panel, 10, 1).until(
            lambda x: x.find_element(By.CSS_SELECTOR, '[title="Хоккей"]').is_displayed())
        hokkey = panel.find_element(By.CSS_SELECTOR, '[title="Хоккей"]')
        if "filter-active" not in hokkey.get_attribute("class"):
            hokkey.click()
            time.sleep(2)

        driver.execute_script("window.scrollTo(0, 50)")
        driver.execute_script("window.scrollTo(0, 0)")


# Основные функции


def open_site(url):
    time.sleep(3)
    driver.get(url)


def login_auth():
    global klk

    if klk > 0:
        return 0
    klk += 1
    try:

        WebDriverWait(driver, 10, 1).until(lambda x: x.find_element(By.XPATH,
                                                                    "/html/body/div[2]/header/wlb-top-menu/div/div[2]/wlb-login-component/div/div/a[1]").is_displayed())
        login_button = driver.find_element(By.XPATH,
                                           "/html/body/div[2]/header/wlb-top-menu/div/div[2]/wlb-login-component/div/div/a[1]")
        login_button.click()
        driver.execute_script("window.scrollTo(0, 50)")
        WebDriverWait(driver, 10, 1).until(lambda x: x.find_element(By.XPATH,
                                                                    "/html/body/div[2]/header/wlb-top-menu/div/div[2]/wlb-login-component/div/form/ul/li[3]").is_displayed())
        login = driver.find_element(By.XPATH,
                                    "/html/body/div[2]/header/wlb-top-menu/div/div[2]/wlb-login-component/div/form/ul/li[3]")
        login.click()
        WebDriverWait(driver, 10, 1).until(lambda x: x.find_element(By.NAME, "login").is_displayed())
        login_input = driver.find_element(By.NAME, "login")
        login_input.send_keys(str(account_login))
        WebDriverWait(driver, 10, 1).until(lambda x: x.find_element(By.NAME, "passw").is_displayed())
        password_input = driver.find_element(By.NAME, "passw")
        password_input.send_keys(str(account_password))
        WebDriverWait(driver, 10, 1).until(lambda x: x.find_element(By.XPATH,
                                                                    "/html/body/div[2]/header/wlb-top-menu/div/div[2]/wlb-login-component/div/form/button").is_displayed())
        authorize = driver.find_element(By.XPATH,
                                        "/html/body/div[2]/header/wlb-top-menu/div/div[2]/wlb-login-component/div/form/button")
        authorize.click()
    except NoSuchElementException:
        driver.refresh()
    print("Авторизовались")


def count_of_games(game):
    global match

    if game == "баскетбол":
        time.sleep(2)
        for c in range(100, 0, -1):
            try:
                if driver.find_element(By.XPATH,
                                       f"/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-events-list/div/div[3]/div/div[{c}]"):
                    match = c
                    print(match)
                    print("Обнаружены все доступные матчи")
                    break
            except NoSuchElementException:
                some = 1

    if game == "хоккей":
        time.sleep(2)
        for t in range(100, 0, -1):
            try:
                if driver.find_element(By.XPATH,
                                       f"/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-events-list/div/div[3]/div/div[{t}]/wlb-events-list-item/section/div"):
                    match = t
                    print(match)
                    print("Обнаружены все доступные матчи")
                    break
            except NoSuchElementException:
                some = 1


def open_my_bids():
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 0)")

    try:
        WebDriverWait(driver, 10, 1).until(lambda x: x.find_element(By.LINK_TEXT, "Личный кабинет"))
        user_profile = driver.find_element(By.LINK_TEXT, "Личный кабинет")
        user_profile.click()
    except (NoSuchElementException, WebDriverException):
        try:
            user_profile = driver.find_element(By.XPATH, "/html/body/div[2]/header/wlb-top-menu/div/div[2]/wlb-login-component/div/div[1]/a")
            user_profile.click()
        except (NoSuchElementException, WebDriverException):
            try:
                time.sleep(1)
                give = driver.find_element(By.XPATH, '//*[@id="Uoshoasieboh4fae"]/ng-component/mat-dialog-content/div/a')
                give.click()
                time.sleep(0.5)
                user_profile = driver.find_element(By.LINK_TEXT, "Личный кабинет")
                user_profile.click()
            except NoSuchElementException:
                driver.refresh()
                time.sleep(3)

    time.sleep(2)

    driver.execute_script("window.scrollTo(0, 0)")

    my_bids = driver.find_element(By.LINK_TEXT, "Мои пари")
    my_bids.click()
    time.sleep(2)


def check_bid_result():
    global numOfCheck
    global result
    global bid_score
    global bid_type
    global game_for_bids
    global ethernet_bug_fix
    b = 0
    print("зашло в check bid res")
    time.sleep(5)

    while True:
        if b == 48:
            b = 0
            driver.refresh()
            open_my_bids()

        WebDriverWait(driver, 60, ignored_exceptions=ignored_exceptions).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH,
                 "/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[2]/wlb-bet-history/div/div[1]/table/tbody[1]/tr/td[6]/div/span")))
        bid = driver.find_element(By.XPATH,
                                  "/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[2]/wlb-bet-history/div/div[1]/table/tbody[1]/tr/td[6]/div/span")
        if str(bid.text) == "В игре":
            time.sleep(5)
            b += 1
            ethernet_bug_fix = 1
            continue
        else:
            if "-" in str(bid.text):
                result = "проигрыш"
                print("проигрыш")
                bid_score += 1
                ethernet_bug_fix = 0
                if bid_score == 10:
                    driver.quit()

                next_bid_timer()
                if game_for_bids == "хоккей":
                    already_started_match_bid(game_for_bids)
                do_bid(game=game_for_bids)
            elif str(bid.text) == "0":
                result = "возврат"
                ethernet_bug_fix = 0
                next_bid_timer()
                if game_for_bids == "хоккей":
                    already_started_match_bid(game_for_bids)
                do_bid(game=game_for_bids)
            else:
                print("выйгрыш")
                result = "выйгрыш"
                ethernet_bug_fix = 0
                bid_score = 0

                try:
                    bid_type_link = driver.find_element(By.XPATH,
                                                        "/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[2]/wlb-bet-history/div/div[1]/table/tbody[1]/tr/td[2]/div/div[4]")
                except NoSuchElementException:
                    try:
                        bid_type_link = driver.find_element(By.XPATH,
                                                            "/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[2]/wlb-bet-history/div/div[1]/table/tbody[1]/tr/td[2]/div/div[3]")
                    except NoSuchElementException:
                        try:
                            bid_type_link = driver.find_element(By.XPATH,
                                                                "/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[2]/wlb-bet-history/div/div[1]/table/tbody[1]/tr/td[2]/div/div[2]")

                        except NoSuchElementException:
                            bid_type_link = "0"
                            print("Bid_type_link last Except")

                if bid_type_link.text == "Чет":
                    bid_type = "нечет"
                else:
                    bid_type = "чет"

                if numOfCheck > 0:
                    print('Ctrl + Z / Ctrl + Q Была нажата')
                    driver.close()
                    driver.quit()
                else:
                    next_bid_timer()
                    if game_for_bids == "хоккей":
                        already_started_match_bid(game_for_bids)
                    do_bid(game=game_for_bids)


def get_bid_type_table():
    global checker
    global table_title_p_p

    driver.execute_script("window.scrollTo(0, 1000)")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, 500)")

    table_title = driver.find_element(By.XPATH, "//span[text()='Чет/Нечет']")
    table_title_p = table_title.find_element(By.XPATH, "..")
    table_title_p_p = table_title_p.find_element(By.XPATH, "..")
    print("Получение таблицы Чет/Нечет завершено")


def accept_bid(game):
    sum_input = driver.find_element(By.XPATH,
                                    "/html/body/div[2]/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div/div[3]/div[1]/div[2]/input")
    sum_input.click()
    time.sleep(3)

    sum_input.clear()
    time.sleep(5)
    if game == "баскетбол":
        sum_input.send_keys(str(basketball_bids[bid_score]))
    else:
        sum_input.send_keys(str(hokkey_bids[bid_score]))
    time.sleep(2)
    ## //*[@id="popup-clear-coupon"]/div[5] - текст
#//*[@id="popup-clear-coupon"]/div[2] - надпись сверху
# #//*[@id="popup-clear-coupon"]/div[6]/div[1]/span - отмена

    accept = driver.find_element(By.XPATH, "//button[text()='Принять']")
    accept.click()
    time.sleep(7)  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    try:
        WebDriverWait(driver, 14, ignored_exceptions=ignored_exceptions).until(
            expected_conditions.presence_of_element_located((By.LINK_TEXT, '«Мои пари»')))

        pop_up = driver.find_element(By.LINK_TEXT, '«Мои пари»')
        pop_up.click()
        return 1

    except NoSuchElementException:
        print("jd")
        message = driver.find_element(By.XPATH, '//*[@id="popup-clear-coupon"]/div[5]').text
        print(message)
        nums = [float(s) for s in re.findall(r'-?\d+\.?\d*', message)]
        print(nums)
        if nums[1] >= 1.88:
            print("confirm")
            WebDriverWait(driver, 7, ignored_exceptions=ignored_exceptions).until(
                expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="popup-clear-coupon"]/div[6]/div[2]/span')))
            print("confirm1")
            confirm = driver.find_element(By.XPATH, '//*[@id="popup-clear-coupon"]/div[6]/div[2]/span')
            confirm.click()

            time.sleep(2)
            print("confrim3")
            WebDriverWait(driver, 7, ignored_exceptions=ignored_exceptions).until(
                expected_conditions.presence_of_element_located((By.LINK_TEXT, '«Мои пари»')))
            pop_up = driver.find_element(By.LINK_TEXT, '«Мои пари»')
            pop_up.click()
            return 1
        else:
            print("reject")
            WebDriverWait(driver, 7, ignored_exceptions=ignored_exceptions).until(
                expected_conditions.presence_of_element_located(
                    (By.XPATH, '//*[@id="popup-clear-coupon"]/div[6]/div[1]/span')))
            reject = driver.find_element(By.XPATH, '//*[@id="popup-clear-coupon"]/div[6]/div[1]/span')
            print("reject1")
            reject.click()
            print("Новый коэф не подходит")
            return 0


def now_matches_page_open():
    WebDriverWait(driver, 30, 1).until(lambda x: x.find_element(By.XPATH, "//span[text()='Сейчас']").is_displayed())
    in_game = driver.find_element(By.XPATH, "//span[text()='Сейчас']")
    in_game.click()
    try:
        show_games(game=game_for_bids)
    except (NoSuchElementException, TimeoutException):
        print("Нет онлайн матчей")
        return 0
    time.sleep(2)


def already_started_match_bid(game):
    global bid_type
    global count
    global checker
    global bid_score
    global match
    global ignored_exceptions
    global already_started_matches
    global table_title_p_p

    d = datetime.datetime.now()
    date1 = datetime.datetime.strptime(str(d), "%Y-%m-%d %H:%M:%S.%f")

    while True:
        # Витязь

        now_matches_page_open()
        print("Проверка - есть ли запомненные матчи")
        if already_started_matches[0] == "" and already_started_matches[1] == "" and already_started_matches[
            2] == "" and already_started_matches[3] == "" and already_started_matches[4] == "" and \
                already_started_matches[5] == "" and already_started_matches[6] == "" and already_started_matches[
            7] == "" and already_started_matches[8] == "" and already_started_matches[9] == "" and \
                already_started_matches[10] == "":
            print("Запомненных матчей нет.")
            return 0
        print("Проверка матчей")
        for index, z in enumerate(already_started_matches):
            print(z)

            date2 = datetime.datetime.now()
            delta = (date1 - date2).total_seconds()
            delta = abs(delta)

            print(int(delta), " delta")
            if int(delta) >= 900:
                return 0
            print(str(z))
            try:
                if str(z) == "":
                    print("матч отсутсвует")
                    continue
                else:
                    match_now = driver.find_element(By.XPATH, f"//span[text()='{str(z)}']")
                    print(z)
                    print(match_now.text)
            except NoSuchElementException:
                print("матч Не найден")
                already_started_matches[index] = ""
                now_matches_page_open()
                continue
            try:
                period = match_now.find_element(By.XPATH, "..")
                period = period.find_element(By.XPATH, "..")
                period = period.find_element(By.XPATH, "..")
                period = period.find_element(By.XPATH, "..")
                period = period.find_element(By.XPATH, "..")
                #period = period.find_element(By.XPATH, "..")
                print("asd")
                period = period.find_element(By.XPATH, "./div[1]").text
                print("654")
                nums = [int(s) for s in re.findall(r'-?\d+\.?\d*', period)]
                print(nums)
                if len(nums) != 0:

                    if nums[0] == 2 or nums[0] == 3:
                        print(already_started_matches[index], "Первый период закончился")
                        already_started_matches[index] = ""
                        now_matches_page_open()
                        continue
                    else:
                        if len(nums) >= 2:
                            if nums[1] >= 13:
                                time.sleep(2)
                                match_now.click()
                                time.sleep(3)

                                if game == "хоккей":

                                    bid_type = "нечет"

                                    try:
                                        country = driver.find_element(By.XPATH,
                                                                      '//*[@id="sticky-header-top"]/wlb-market-book-header/div[2]/div').text
                                        if "НОВАЯ ЗЕЛАНДИЯ" in str(country) or "НОРВЕГИЯ" and "ЭЛИТСЕРИЯ" in str(country) or "КАЗАХСТАН" and "ВЫСШАЯ ЛИГА" in str(country) or "ЛИГА ПРО, 3 Х 10" in str(country):

                                            if bid_score <= 4:
                                                print(str(country), "Страна не подходит")
                                                already_started_matches[index] = ""
                                                now_matches_page_open()
                                                continue
                                    except NoSuchElementException:
                                        print("ok")

                                    try:
                                        time.sleep(2)
                                        get_bid_type_table()
                                    except NoSuchElementException:
                                        print("нет таблицы")
                                        checker += 1
                                        now_matches_page_open()
                                        continue

                                    time.sleep(1)

                                    try:
                                        try:
                                            time.sleep(2)
                                            part = table_title_p_p.find_element(By.CSS_SELECTOR, "[title='1 период']")
                                            part_parent = part.find_element(By.XPATH, "..")
                                            part_parent_parent = part_parent.find_element(By.XPATH, "..")

                                        except NoSuchElementException:
                                            print("Нет первого периода")
                                            now_matches_page_open()
                                            continue
                                        button = part_parent_parent.find_element(By.XPATH, "./div[3]/div")
                                        count = part_parent_parent.find_element(By.XPATH, "./div[3]/div/span[4]")
                                        print("Кнопка и коэффицент")
                                    except NoSuchElementException:
                                        print("Не могу найти кнопку нечет.")
                                        checker += 1
                                        now_matches_page_open()
                                        continue

                                    if "locked" in button.get_attribute("class"):
                                        print("кнопка не активна")
                                        checker += 1
                                        now_matches_page_open()
                                        continue

                                    driver.execute_script("window.scrollTo(0, 0)")
                                    try:
                                        print("Проверяем коэфиценты")
                                        time.sleep(2)
                                        print(count.text)
                                        if float(count.text) >= 1.88:  # 1.88
                                            button.click()
                                            try:
                                                print("ac_bid_try")
                                                accept_result = accept_bid(game=game_for_bids)
                                                if accept_result == 0:
                                                    print("Не подошло  новое значение таблицы")
                                                    checker += 1
                                                    now_matches_page_open()
                                                    continue
                                                elif accept_result == 1:
                                                    time.sleep(3)
                                                    print("check bid res")
                                                    get_last_bid_type()
                                            except NoSuchElementException:
                                                print("Не могу найти поле ввода или кнопку Принять")
                                                driver.close()
                                                driver.quit()

                                            return 0
                                        else:
                                            print("Маленький коэфицент")
                                            checker += 1
                                            now_matches_page_open()
                                            continue

                                    except ValueError:
                                        print("couldn't convert string to float")

                                else:
                                    return 0
                else:
                    print("не обозначен период, пока пропустим")
                    now_matches_page_open()
                    continue

            except NoSuchElementException:
                print("Не нашли надпись с периодом.. ")
                now_matches_page_open()
                continue




def get_all_games(game):
    global checker

    WebDriverWait(driver, 30, 1).until(lambda x: x.find_element(By.XPATH, "//span[text()='Ближайшие']").is_displayed())
    nearest = driver.find_element(By.XPATH, "//span[text()='Ближайшие']")
    nearest.click()

    if game == "баскетбол":

        WebDriverWait(driver, 30, 1).until(
            lambda x: x.find_element(By.XPATH, '//*[@id="sticky-header-bottom"]/div/div[1]').is_displayed())
        panel = driver.find_element(By.XPATH, '//*[@id="sticky-header-bottom"]/div/div[1]')
        WebDriverWait(panel, 30, 1).until(
            lambda x: x.find_element(By.CSS_SELECTOR, '[title="Баскетбол"]').is_displayed())
        basketball = panel.find_element(By.CSS_SELECTOR, '[title="Баскетбол"]')
        if "filter-active" not in basketball.get_attribute("class"):
            basketball.click()
            time.sleep(2)

        driver.execute_script("window.scrollTo(0, 2337)")

        count_of_games(game=game)

        driver.execute_script("window.scrollTo(0, 0)")

    if game == "хоккей":

        WebDriverWait(driver, 30, 1).until(
            lambda x: x.find_element(By.XPATH, '//*[@id="sticky-header-bottom"]/div/div[1]').is_displayed())
        panel = driver.find_element(By.XPATH, '//*[@id="sticky-header-bottom"]/div/div[1]')
        WebDriverWait(panel, 30, 1).until(
            lambda x: x.find_element(By.CSS_SELECTOR, '[title="Хоккей"]').is_displayed())
        hokkey = panel.find_element(By.CSS_SELECTOR, '[title="Хоккей"]')
        if "filter-active" not in hokkey.get_attribute("class"):
            hokkey.click()
            time.sleep(2)

        driver.execute_script("window.scrollTo(0, 2337)")

        count_of_games(game="хоккей")

        driver.execute_script("window.scrollTo(0, 0)")

    print("Получены все доступные игры")


def get_last_bid_type():
    global result
    global bid_type
    global basketball_bids
    global hokkey_bids
    global bid_score
    global new_or_last_var
    global ethernet_bug_fix
    global own_bid_choice
    print(bid_score, "bd score")

    open_my_bids()

    new_or_last()

    if own_bid_choice == 1:
        own_bid_choice = 0
        if game_for_bids == "хоккей":
            already_started_match_bid(game_for_bids)
        do_bid(game_for_bids)


    bid = driver.find_element(By.XPATH,
                              "/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[2]/wlb-bet-history/div/div[1]/table/tbody[1]/tr/td[6]/div/span")
                                #  /html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[2]/wlb-bet-history/div/div[1]/table/tbody[1]/tr/td[2]/div/div[2]
                            #/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[2]/wlb-bet-history/div/div[1]/table/tbody[4]/tr/td[6]/div/span

    print(bid.text, "bdtex")
    print(ethernet_bug_fix, "ethbf")
    if str(bid.text) == "В игре" or ethernet_bug_fix == 1:
        check_bid_result()

        return 0

    try:
        bid_type_link = driver.find_element(By.XPATH,
                                            "/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[2]/wlb-bet-history/div/div[1]/table/tbody[1]/tr/td[2]/div/div[4]")
    except NoSuchElementException:
        try:
            bid_type_link = driver.find_element(By.XPATH,
                                                "/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[2]/wlb-bet-history/div/div[1]/table/tbody[1]/tr/td[2]/div/div[3]")
        except NoSuchElementException:
            try:
                bid_type_link = driver.find_element(By.XPATH,
                                                    "/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[2]/wlb-bet-history/div/div[1]/table/tbody[1]/tr/td[2]/div/div[2]")

            except NoSuchElementException:
                bid_type_link = "0"
    print(bid.text)
    if "-" not in str(bid.text) and str(bid.text) != "0":
        print('ggg')
        print(bid_score, "bd score")
        bid_score = 0
        print(bid_score, "bd score")

        if bid_type_link.text == "Чет":
            bid_type = "нечет"
        else:
            bid_type = "чет"

    else:
        if bid_type_link.text == "Чет":
            bid_type = "чет"           # ???
        else:
            bid_type = "нечет"

    if game_for_bids == "хоккей":
        already_started_match_bid(game_for_bids)


def next_matches():
    global i
    global already_started_matches

    try:
        for v in range(0, 11):
            try:
                already_started_matches[v] = driver.find_element(By.XPATH,
                                                    f"/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-events-list/div/div[3]/div/div[{v+1}]/wlb-events-list-item/section/div/div[1]/div[2]/a/h2/span[1]").text
            except NoSuchElementException:
                already_started_matches[v] = driver.find_element(By.XPATH,
                                              f"/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-events-list/div/div[3]/div/div[{v+1}]/wlb-events-list-item/section/div/div[1]/div[2]/a/h2/div/span[1]").text

    except NoSuchElementException:
        return 0


def do_bid(game):
    global count
    global checker
    global bid_score
    global bid_type
    global match
    global ignored_exceptions
    global i
    global second_match

    get_all_games(game=game_for_bids)

    for i in range(1, match + 2):
        try:
            WebDriverWait(driver, 3, 1).until(
                lambda x: x.find_element(By.XPATH, f"/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-events-list/div/div[3]/div/div[{i}]/wlb-events-list-item/section/div/div[1]/div[2]/a").is_displayed())
            game_match = driver.find_element(By.XPATH,
                                             f"/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-events-list/div/div[3]/div/div[{i}]/wlb-events-list-item/section/div/div[1]/div[2]/a")
            if game_for_bids == "хоккей":
                next_matches()
        except (NoSuchElementException, TimeoutException):
            if i >= match + 1:
                i = 1
            get_all_games(game=game_for_bids)
            continue

        game_match.click()
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, 3350)")
        time.sleep(2)

        try:
            get_bid_type_table()
            time.sleep(2)
        except NoSuchElementException:
            print("нет таблицы")
            checker += 1
            get_all_games(game_for_bids)
            continue
        if game_for_bids == "баскетбол":
            try:
                league = driver.find_element(By.XPATH,
                                             '//*[@id="sticky-header-top"]/wlb-market-book-header/div[2]/div').text
                print(str(league))
                if "МЕКСИКА" and "ЛИГА LNBP" in str(league) or "БЕЛОРУСИЯ" and "СКАЙ ЛИГА" in str(league) or "НОРВЕГИЯ" and "ВЫСШАЯ ЛИГА" in str(league) or "ДАНИЯ" and "ВЫСШАЯ ЛИГА" in str(league):
                    if bid_score <= 4:
                        print(str(league), "лига не подходит")
                        get_all_games(game_for_bids)
                        continue
            except NoSuchElementException:
                print("ok")

            try:
                try:
                    time.sleep(2)
                    part = table_title_p_p.find_element(By.CSS_SELECTOR, "[title='1 четверть']")
                    part_parent = part.find_element(By.XPATH, "..")
                    part_parent_parent = part_parent.find_element(By.XPATH, "..")

                except NoSuchElementException:
                    print("Нет первой четверти")
                    get_all_games(game_for_bids)
                    continue
                if bid_type == "чет":
                    #try:
                    button = part_parent_parent.find_element(By.XPATH, "./div[2]/div")
                    count = part_parent_parent.find_element(By.XPATH, "./div[2]/div/span[4]")
                    print("кнопка и коэффицент")
                    print(count.text)
                    checker += 1
                else:
                    button = part_parent_parent.find_element(By.XPATH, "./div[3]/div")
                    count = part_parent_parent.find_element(By.XPATH, "./div[3]/div/span[4]")
                    print("кнопка и коэффицент")
                    checker += 1
                    print(count.text)

            except NoSuchElementException:
                print("Не могу найти кнопку")
                checker += 1
                get_all_games(game_for_bids)
                continue

            if "locked" in button.get_attribute("class"):
                print("кнопка не активна")
                checker += 1
                get_all_games(game_for_bids)
                continue

            driver.execute_script("window.scrollTo(0, 0)")

            try:
                if float(count.text) >= 1.85: # временно 1.87
                    button.click()
                    try:
                        print('test')
                        accept_bid(game=game_for_bids)
                    except NoSuchElementException:
                        print("Не могу найти поле ввода или кнопку Принять")
                        driver.close()
                        driver.quit()
                    break

                else:
                    print("Не подходящий коэфицент")
                    checker += 1
                    get_all_games(game_for_bids)
                    continue

            except ValueError:
                print("couldn't convert string to float")
                get_all_games(game_for_bids)
                continue

        # another game

        if game_for_bids == "хоккей":
            try:
                country = driver.find_element(By.XPATH,
                                             '//*[@id="sticky-header-top"]/wlb-market-book-header/div[2]/div').text
                if "НОВАЯ ЗЕЛАНДИЯ" in str(country) or "НОРВЕГИЯ" and "ЭЛИТСЕРИЯ" in str(country) or "КАЗАХСТАН" and "ВЫСШАЯ ЛИГА" in str(country) or "ЛИГА ПРО, 3 Х 10" in str(country):
                    if bid_score <=4:
                        print(str(country), "Страна не подходит")
                        continue
            except NoSuchElementException:
                print("ok")

            bid_type = "нечет"

            time.sleep(1)
            try:
                try:
                    time.sleep(2)
                    part = table_title_p_p.find_element(By.CSS_SELECTOR, "[title='1 период']")
                    part_parent = part.find_element(By.XPATH, "..")
                    part_parent_parent = part_parent.find_element(By.XPATH, "..")

                except NoSuchElementException:
                    print("Нет первого периода")
                    get_all_games(game_for_bids)
                    continue

                button = part_parent_parent.find_element(By.XPATH, "./div[3]/div")
                count = part_parent_parent.find_element(By.XPATH, "./div[3]/div/span[4]")
                print("Кнопка и коэффицент")
            except NoSuchElementException:
                print("Не могу найти кнопку нечет.")
                checker += 1
                get_all_games(game_for_bids)
                continue

            if "locked" in button.get_attribute("class"):
                print("кнопка не активна")
                checker += 1
                get_all_games(game_for_bids)
                continue

            driver.execute_script("window.scrollTo(0, 0)")
            try:
                print("Проверяем коэфиценты")
                time.sleep(2)
                print(count.text)
                if float(count.text) >= 1.88: #.188
                    button.click()
                    try:
                        accept_bid(game=game_for_bids)
                    except NoSuchElementException:
                        print("Не могу найти поле ввода или кнопку Принять")
                        driver.close()
                        driver.quit()

                    return 0
                else:
                    print("Маленький коэфицент")
                    checker += 1
                    get_all_games(game_for_bids)
                    continue

            except ValueError:
                print("couldn't convert string to float")
                get_all_games(game_for_bids)
                continue

        if i > match:
            print("Закончились игры")
            driver.close()
            driver.quit()
        else:
            time.sleep(5)
            check_bid_result()


def parent_func():
    time.sleep(3)
    get_info()
    open_site("https://winline.ru/")
    print(bid_score)
    time.sleep(1)
    login_auth()
    time.sleep(2)
    get_last_bid_type()
    do_bid(str(game_for_bids))


if __name__ == '__main__':
    while True:
        try:
            parent_func()
        except (TimeoutException, WebDriverException):
            time.sleep(1)
            print("Потеря соединения")
            continue
