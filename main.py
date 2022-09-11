from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import NoSuchElementException, ElementNotVisibleException, StaleElementReferenceException, \
    TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import random
import time
import keyboard
import datetime

options = webdriver.ChromeOptions()
ua = UserAgent().chrome
options.add_argument(f"user-agent={ua}")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("window-size=1200x600")
driver = webdriver.Chrome('chromedriver.exe', options=options)

PATH = "/Users/yourPath/Desktop/chromedriver"
bid_type = ""
basketball_bids = [50, 100, 200, 450, 1000, 2300, 4900, 10500, 22500, 49000]
hokkey_bids = [50, 100, 200, 450, 1000, 2300, 4900, 10500, 22500, 48000]
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
second_match = "Перт"
table_title_p_p = ""

# служебные функции


def increase():
    global numOfCheck

    numOfCheck += 1


def next_bid_timer():
    seconds = random.randint(25, 70)
    time.sleep(seconds)
    print("Таймер до новой ставки закончен")


def get_info():
    global account_password, account_login, game_for_bids, new_or_last_var, numxz

    if numxz > 0:
        return 0

    numxz += 1
    account_login = input("Логин: ")
    account_password = input("Пароль: ")

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

    print("Выберите: Сумма ставок по новой - 1, продолжить с последней ставки - 2 ")
    new_or_last_var = int(input("Введите цифру: "))


def new_or_last():
    global game_for_bids
    global bid_score

    if new_or_last_var == 2:

        try:
            start_bid_sum = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[2]/wlb-bet-history/div/div[1]/table/tbody[1]/tr/td[5]/div[1]/span")
        except NoSuchElementException:
            start_bid_sum = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[2]/wlb-bet-history/div/div[1]/table/tbody[2]/tr/td[5]/div/span")

        if game_for_bids == "баскетбол":
            for index, element in enumerate(basketball_bids):
                if start_bid_sum.text == str(element):
                    bid_score = index+1

        if game_for_bids == "хоккей":
            for index, element in enumerate(hokkey_bids):
                if start_bid_sum.text == str(element):
                    bid_score = index+1


def show_games(game):
    global checker

    if game == "баскетбол":

        if checker == 0:
            checker += 1

            WebDriverWait(driver, 30, 1).until(lambda x: x.find_element(By.XPATH, '//*[@id="sticky-header-bottom"]/div/div[1]').is_displayed())
            panel = driver.find_element(By.XPATH, '//*[@id="sticky-header-bottom"]/div/div[1]')
            WebDriverWait(panel, 30, 1).until(lambda x: x.find_element(By.CSS_SELECTOR, '[title="Баскетбол"]').is_displayed())
            basketball = panel.find_element(By.CSS_SELECTOR, '[title="Баскетбол"]')
            basketball.click()
            time.sleep(2)

        driver.execute_script("window.scrollTo(0, 50)")
        driver.execute_script("window.scrollTo(0, 0)")

    if game == "хоккей":
        if checker == 0:
            checker += 1

            WebDriverWait(driver, 30, 1).until(lambda x: x.find_element(By.XPATH, '//*[@id="sticky-header-bottom"]/div/div[1]').is_displayed())
            panel = driver.find_element(By.XPATH, '//*[@id="sticky-header-bottom"]/div/div[1]')
            WebDriverWait(panel, 30, 1).until(lambda x: x.find_element(By.CSS_SELECTOR, '[title="Хоккей"]').is_displayed())
            hokkey = panel.find_element(By.CSS_SELECTOR, '[title="Хоккей"]')
            hokkey.click()
            time.sleep(2)

            driver.execute_script("window.scrollTo(0, 50)")
            driver.execute_script("window.scrollTo(0, 0)")

# Основные функции


def open_site(url):
    time.sleep(3)
    keyboard.add_hotkey('Ctrl + Z', lambda: increase())
    keyboard.add_hotkey('Ctrl + Q', lambda: driver.quit())
    time.sleep(1)
    driver.get(url)


def login_auth():

    try:
        WebDriverWait(driver, 30, 1).until(lambda x: x.find_element(By.XPATH, "/html/body/div[2]/header/wlb-top-menu/div/div[2]/wlb-login-component/div/div/a[1]").is_displayed())
        login_button = driver.find_element(By.XPATH, "/html/body/div[2]/header/wlb-top-menu/div/div[2]/wlb-login-component/div/div/a[1]")
        login_button.click()
        driver.execute_script("window.scrollTo(0, 50)")
        WebDriverWait(driver, 30, 1).until(lambda x: x.find_element(By.XPATH, "/html/body/div[2]/header/wlb-top-menu/div/div[2]/wlb-login-component/div/form/ul/li[3]").is_displayed())
        login = driver.find_element(By.XPATH, "/html/body/div[2]/header/wlb-top-menu/div/div[2]/wlb-login-component/div/form/ul/li[3]")
        login.click()
        WebDriverWait(driver, 30, 1).until(lambda x: x.find_element(By.NAME, "login").is_displayed())
        login_input = driver.find_element(By.NAME, "login")
        login_input.send_keys(str(account_login))
        WebDriverWait(driver, 30, 1).until(lambda x: x.find_element(By.NAME, "passw").is_displayed())
        password_input = driver.find_element(By.NAME, "passw")
        password_input.send_keys(str(account_password))
        WebDriverWait(driver, 30, 1).until(lambda x: x.find_element(By.XPATH, "/html/body/div[2]/header/wlb-top-menu/div/div[2]/wlb-login-component/div/form/button").is_displayed())
        authorize = driver.find_element(By.XPATH, "/html/body/div[2]/header/wlb-top-menu/div/div[2]/wlb-login-component/div/form/button")
        authorize.click()
    except NoSuchElementException:
        driver.refresh()
    print("Авторизовались")


def count_of_games(game):
    global match

    if game == "баскетбол":
        time.sleep(2)
        for i in range(100, 0, -1):
            try:
                if driver.find_element(By.XPATH, f"/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-events-list/div/div[3]/div/div[{i}]"):

                    match = i
                    print(match)
                    print("Обнаружены все доступные матчи")
                    break
            except NoSuchElementException:
                print(i, "not find")

    if game == "хоккей":
        time.sleep(2)
        for i in range(100, 0, -1):
            try:
                if driver.find_element(By.XPATH, f"/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-events-list/div/div[3]/div/div[{i}]/wlb-events-list-item/section/div"):
                    match = i
                    print(match)
                    print("Обнаружены все доступные матчи")
                    break
            except NoSuchElementException:
                print(i, "not find") # если нажата ждем победы


def open_my_bids():

    time.sleep(5)

    user_profile = driver.find_element(By.LINK_TEXT, "Личный кабинет")
    user_profile.click()
    time.sleep(2)

    my_bids = driver.find_element(By.LINK_TEXT, "Мои пари")
    my_bids.click()
    time.sleep(2)


def check_bid_result():
    global numOfCheck
    global result
    global bid_score
    global bid_type
    global game_for_bids

    print("зашло в check bid res")

    try:
        try:
            bid = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[2]/wlb-bet-history/div/div[1]/table/tbody[1]/tr/td[6]/div/span")
        except NoSuchElementException:
            driver.refresh()
            open_my_bids()
            bid = driver.find_element(By.XPATH,
                                      "/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[2]/wlb-bet-history/div/div[1]/table/tbody[1]/tr/td[6]/div/span")
    except StaleElementReferenceException:
        driver.refresh()
        open_my_bids()
        bid = driver.find_element(By.XPATH,
                                  "/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[2]/wlb-bet-history/div/div[1]/table/tbody[1]/tr/td[6]/div/span")

    while True:

        driver.refresh()
        open_my_bids()

        WebDriverWait(driver, 60, ignored_exceptions=ignored_exceptions).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[2]/wlb-bet-history/div/div[1]/table/tbody[1]/tr/td[6]/div/span")))
        bid = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[2]/wlb-bet-history/div/div[1]/table/tbody[1]/tr/td[6]/div/span")
        if str(bid.text) == "В игре":
            time.sleep(50)
            continue
        else:
            if "-" in str(bid.text):
                result = "проигрыш"
                print("проигрыш")
                bid_score += 1
                if bid_score == 10:
                    driver.quit()

                next_bid_timer()
                already_started_match_bid(game_for_bids)
                do_bid(game=game_for_bids)
            elif str(bid.text) == "0":
                result = "возврат"
                next_bid_timer()
                already_started_match_bid(game_for_bids)
                do_bid(game=game_for_bids)
            else:
                print("выйгрыш")
                result = "выйгрыш"
                bid_score = 0

                try:
                    bid_type_link = driver.find_element(By.XPATH,
                                                        "/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[2]/wlb-bet-history/div/div[1]/table/tbody[4]/tr/td[2]/div/div[4]")
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

                if bid_type_link.text == "Чет":
                    bid_type = "нечет"
                else:
                    bid_type = "чет"

                if numOfCheck > 0:
                    driver.close()
                    driver.quit()
                else:
                    next_bid_timer()
                    already_started_match_bid(game_for_bids)
                    do_bid(game=game_for_bids)


def get_bid_type_table():
    global checker
    global table_title_p_p

    driver.execute_script("window.scrollTo(0, 1000)")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, 500)")

    table_title = driver.find_element(By.XPATH, "//span[text()='Чет/Нечет']")
    print("first")
    table_title_p = table_title.find_element(By.XPATH, "..")
    print("SEc")
    table_title_p_p = table_title_p.find_element(By.XPATH, "..")
    print("third")


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

    accept = driver.find_element(By.XPATH, "//button[text()='Принять']")
    accept.click()
    time.sleep(15)  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    WebDriverWait(driver, 60, ignored_exceptions=ignored_exceptions).until(
        expected_conditions.presence_of_element_located((By.LINK_TEXT, '«Мои пари»')))

    time.sleep(2)

    pop_up = driver.find_element(By.LINK_TEXT, '«Мои пари»')
    time.sleep(10)
    pop_up.click()


def already_started_match_bid(game):
    global bid_type
    global count
    global checker
    global bid_score
    global match
    global ignored_exceptions
    global i
    global second_match
    global table_title_p_p

    print(second_match)

    WebDriverWait(driver, 30, 1).until(lambda x: x.find_element(By.XPATH, "//span[text()='Сейчас']").is_displayed())
    in_game = driver.find_element(By.XPATH, "//span[text()='Сейчас']")
    in_game.click()

    show_games(game=game_for_bids)

    match_now = driver.find_element(By.XPATH, f"//span[text()='{second_match}']")
    match_now.click()

    if game == "баскетбол":
        try:
            get_bid_type_table()
        except NoSuchElementException:
            print("нет таблицы")
            checker += 1
            return 0
        try:
            first_part = table_title_p_p.find_element(By.XPATH, "./div[5]/div[1]/div/span")
            if bid_type == "чет":
                if first_part.text == "1 четверть":
                    print("some")
                    # /html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-market-book/div[3]/div[3]/div[2]/div[1]/div[9]/wlb-market-book-market/div/div[5]/div[1]/div/span
                    button = table_title_p_p.find_element(By.XPATH, "./div[5]/div[2]/div")
                    count = table_title_p_p.find_element(By.XPATH, "./div[5]/div[2]/div/span[4]")

                else:
                    print("Нет первой четверти!")
                    checker += 1
                    return 0
            else:
                if first_part.text == "1 четверть":
                    print("some")
                    button = table_title_p_p.find_element(By.XPATH, "./div[5]/div[3]/div")
                    count = table_title_p_p.find_element(By.XPATH, "./div[5]/div[3]/div/span[4]")

                else:
                    print("Нет первой четверти!")
                    checker += 1
                    return 0
        except NoSuchElementException:
            print("Не могу найти кнопку")
            return 0

        if "locked" in button.get_attribute("class"):
            print("кнопка не активна")
            checker += 1
            return 0

        driver.execute_script("window.scrollTo(0, 0)")

        try:
            if float(count.text) >= 1.87:
                button.click()
                try:
                    accept_bid(game=game_for_bids)
                except NoSuchElementException:
                    print("Не могу найти поле ввода или кнопку Принять")
                    driver.close()
                    driver.quit()
                return 0

            else:
                print("Не подходящий коэфицент")
                checker += 1
                return 0
        except ValueError:
            print("couldn't convert string to float")
            return 0

    # another game

    if game == "хоккей":

        bid_type = "нечет"

        try:
            get_bid_type_table()
        except NoSuchElementException:
            print("нет таблицы")
            checker += 1
            return 0

        time.sleep(1)
        try:
            first_part = table_title_p_p.find_element(By.XPATH, "./div[5]/div[1]/div/span")
            if first_part.text == "1 четверть":
                button = table_title_p_p.find_element(By.XPATH, "./div[3]/div[3]/div")
                count = table_title_p_p.find_element(By.XPATH, "./div[5]/div[3]/div/span[4]")
            else:
                print("Нет первой четверти!")
                checker += 1
                return 0
        except NoSuchElementException:
            print("Не могу найти кнопку нечет или коэффиценты.")
            driver.close()
            driver.quit()

        if "locked" in button.get_attribute("class"):
            print("кнопка не активна")
            checker += 1
            return 0

        driver.execute_script("window.scrollTo(0, 0)")
        try:
            print("Проверяем коэфиценты")
            time.sleep(2)
            print(count.text)
            if float(count.text) >= 1.9:
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
                return 0

        except ValueError:
            print("couldn't convert string to float")
            return 0

    if i > match:
        print("Закончились игры")
        driver.close()
        driver.quit()
    else:
        time.sleep(5)
        check_bid_result()


def get_all_games(game):
    global checker

    WebDriverWait(driver, 30, 1).until(lambda x: x.find_element(By.XPATH, "//span[text()='Ближайшие']").is_displayed())
    nearest = driver.find_element(By.XPATH, "//span[text()='Ближайшие']")
    nearest.click()

    if game == "баскетбол":
        if checker == 0:
            checker += 1

            WebDriverWait(driver, 30, 1).until(lambda x: x.find_element(By.XPATH, '//*[@id="sticky-header-bottom"]/div/div[1]').is_displayed())
            panel = driver.find_element(By.XPATH, '//*[@id="sticky-header-bottom"]/div/div[1]')
            WebDriverWait(panel, 30, 1).until(lambda x: x.find_element(By.CSS_SELECTOR, '[title="Баскетбол"]').is_displayed())
            basketball = panel.find_element(By.CSS_SELECTOR, '[title="Баскетбол"]')
            basketball.click()
            time.sleep(2)

        driver.execute_script("window.scrollTo(0, 2337)")

        count_of_games(game=game)

        driver.execute_script("window.scrollTo(0, 0)")

    if game == "хоккей":
        if checker == 0:
            checker += 1

            WebDriverWait(driver, 30, 1).until(lambda x: x.find_element(By.XPATH, '//*[@id="sticky-header-bottom"]/div/div[1]').is_displayed())
            panel = driver.find_element(By.XPATH, '//*[@id="sticky-header-bottom"]/div/div[1]')
            WebDriverWait(panel, 30, 1).until(lambda x: x.find_element(By.CSS_SELECTOR, '[title="Хоккей"]').is_displayed())
            hokkey = panel.find_element(By.CSS_SELECTOR, '[title="Хоккей"]')
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

    open_my_bids()

    new_or_last()

    bid = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[2]/wlb-bet-history/div/div[1]/table/tbody[1]/tr/td[6]/div/span")

    if str(bid.text) == "В игре":

        check_bid_result()

        return 0

    try:
        bid_type_link = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[2]/wlb-bet-history/div/div[1]/table/tbody[4]/tr/td[2]/div/div[4]")
    except NoSuchElementException:
        try:
            bid_type_link = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[2]/wlb-bet-history/div/div[1]/table/tbody[1]/tr/td[2]/div/div[3]")
        except NoSuchElementException:
            try:
                bid_type_link = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[2]/wlb-bet-history/div/div[1]/table/tbody[1]/tr/td[2]/div/div[2]")
            except NoSuchElementException:
                bid_type_link = "0"
    if "-" not in str(bid.text) and str(bid.text) != "0":

        bid_score = 0

        if bid_type_link.text == "Чет":
            bid_type = "нечет"
        else:
            bid_type = "чет"

    else:
        if bid_type_link.text == "Чет":
            bid_type = "чет"
        else:
            bid_type = "нечет"

    print(bid_score)
    print(bid.text)
    print(bid_type)


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
            game_match = driver.find_element(By.XPATH,
                                             f"/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-events-list/div/div[3]/div/div[{i}]/wlb-events-list-item/section/div/div[1]/div[2]/a")
            try:
                second_match = driver.find_element(By.XPATH,
                                                   f"/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-events-list/div/div[3]/div/div[{i + 1}]/wlb-events-list-item/section/div/div[1]/div[2]/a/h2/span[1]").text
            except NoSuchElementException:
                try:
                    second_match = driver.find_element(By.XPATH,
                                                       f"/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-events-list/div/div[3]/div/div[{i + 1}]/wlb-events-list-item/section/div/div[1]/div[3]/a/h2/span[1]").text
                except NoSuchElementException:
                    print("N/G second_game")
        except NoSuchElementException:
            try:
                game_match = driver.find_element(By.XPATH,
                                                 f"/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-events-list/div/div[3]/div/div[{i}]/wlb-events-list-item/section/div/div[1]/div[3]/a")
                try:
                    second_match = driver.find_element(By.XPATH,
                                                       f"/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-events-list/div/div[3]/div/div[{i + 1}]/wlb-events-list-item/section/div/div[1]/div[2]/a/h2/span[1]").text
                except NoSuchElementException:
                    try:
                        second_match = driver.find_element(By.XPATH,
                                                           f"/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-events-list/div/div[3]/div/div[{i + 1}]/wlb-events-list-item/section/div/div[1]/div[3]/a/h2/span[1]").text
                    except NoSuchElementException:
                        print("N/G second_game")
            except NoSuchElementException:
                i = 0
                print("Закончились игры. Завершаем работу...")
                driver.close()
                driver.quit()

        print(second_match)

        game_match.click()
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, 3350)")

        try:
            get_bid_type_table()
        except NoSuchElementException:
            print("нет таблицы")
            checker += 1
            get_all_games(game_for_bids)
            continue
        if game_for_bids == "баскетбол":
            try:
                if bid_type == "чет":
                    button = table_title_p_p.find_element(By.XPATH, "./div[5]/div[2]/div")
                    count = table_title_p_p.find_element(By.XPATH, "./div[5]/div[2]/div/span[4]")
                    checker += 1
                else:
                    button = table_title_p_p.find_element(By.XPATH, "./div[5]/div[3]/div")
                    count = table_title_p_p.find_element(By.XPATH, "./div[5]/div[3]/div/span[4]")
                    checker += 1
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
                if float(count.text) >= 1.87:
                    button.click()
                    try:
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

            bid_type = "нечет"

            time.sleep(1)
            try:
                button = table_title_p_p.find_element(By.XPATH, "./div[3]/div[3]/div")
            except NoSuchElementException:
                print("Не могу найти кнопку нечет.")
                driver.close()
                driver.quit()

            if "locked" in button.get_attribute("class"):
                print("кнопка не активна")
                checker += 1
                get_all_games(game_for_bids)
                continue

            try:
                count = table_title_p_p.find_element(By.XPATH, "./div[5]/div[3]/div/span[4]")
            except NoSuchElementException:
                print("нет коэфицентов")
                checker += 1
                get_all_games(game_for_bids)
                continue

            driver.execute_script("window.scrollTo(0, 0)")
            try:
                print("Проверяем коэфиценты")
                time.sleep(2)
                print(count.text)
                if float(count.text) >= 1.9:
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
