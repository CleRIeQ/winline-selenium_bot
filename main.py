from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import NoSuchElementException, StaleElementReferenceException, \
    TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
import datetime
import re
import random
import time
import keyboard

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("window-size=1200x600")
driver = webdriver.Chrome('chromedriver.exe', options=options)
PATH = "/Users/yourPath/Desktop/chromedriver"

bid_type = ""
is_it_loggined = 0
basketball_bids = [50, 100, 200, 450, 1000, 2300, 4900, 10500, 22800, 49000]
hokkey_bids = [50, 100, 200, 450, 1000, 2300, 4900, 10500, 22500, 48000]
bid_score = 0  # номер элемента в списке
match_count = 0  # число доступных матчей
coefficient = 0  # коэффицент ставки
ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
bot_disable = 0
account_login = ""
account_password = ""
game_for_bids = ""
new_or_last_var = 0
is_info_already_getted = 0
already_started_matches = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
table_title_p_p = ""
ethernet_bug_fix = False
own_bid_choice = 0
main_count = 1.87
start_chet = 1
pari_in_the_game = False


def increase():
    global bot_disable
    print("Нажата Ctrl + Z")

    bot_disable += 1


def next_bid_timer():
    seconds = random.randint(7, 10)
    time.sleep(seconds)
    print("Таймер до новой ставки закончен")


def get_info():
    global account_password, account_login, game_for_bids, new_or_last_var, is_info_already_getted, bid_score, \
        own_bid_choice, basketball_bids, bid_type, main_count, start_chet

    print("Настраиваем бота")
    if is_info_already_getted:
        return 0

    is_info_already_getted = True
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
            bid_type = "нечет"
            break
        else:
            print("Такого номера нет, попробуйте опять.")
            continue

    print("Выберите: Сумма ставок по новой - 1, продолжить с последней ставки - 2, вписать сумму в ручную - 3")
    new_or_last_var = int(input("Введите цифру: "))

    if new_or_last_var == 2:
        start_chet = 0

    if new_or_last_var == 3:
        if game_num == 1:
            start_chet = 0

            bd_type = int(input("Первая ставка на ЧЕТ/НЕЧЕТ (1-чет | 2-нечет: "))
            if bd_type == 1:
                bid_type = "чет"
            elif bd_type == 2:
                bid_type = "нечет"

            strategy = int(input("Стратегия 1 - обычная, 2 - рискованная: "))
            if strategy == 1:
                print("выберите -> 1-50, 2-100, 3-200, 4-450, 5-1000, 6-2300, 7-4900, 8-10500, 9-22800, 10-49000")
                basketball_bids = [50, 100, 200, 450, 1000, 2300, 4900, 10500, 22800, 49000]
            elif strategy == 2:
                print("выберите -> 1-50, 2-150, 3-400, 4-1000, 5-2500, 6-6800, 7-16000, 8-38000 ")
                basketball_bids = [50, 150, 400, 1000, 2500, 6800, 16000, 38000]
                main_count = 1.85

        else:
            print("выберите -> 1-50, 2-100, 3-200, 4-450, 5-1000, 6-2300, 7-4900, 8-10500, 9-22800, 10-48000")
        value = int(input("Число: "))
        bid_score += value - 1
        own_bid_choice = 1
    print(bid_score, basketball_bids[bid_score])


def new_or_last():
    global bid_score
    global new_or_last_var

    if new_or_last_var == 2:
        new_or_last_var = 0
        print("Продолжаем с последней ставки")

        bid = driver.find_element(By.XPATH,
                                  "/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[2]/wlb"
                                  "-bet-history/div/div[1]/table/tbody[1]/tr/td[6]/div/span")

        try:
            start_bid_sum = driver.find_element(By.XPATH,
                                                "/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/"
                                                "div[2]/wlb-bet-history/div/div[1]/table/tbody[1]/tr/td[5]/div[1]/span")
        except NoSuchElementException:
            start_bid_sum = driver.find_element(By.XPATH,
                                                "/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div"
                                                "/div[2]/wlb-bet-history/div/div[1]/table/tbody[1]/tr/td[5]/div/span")

        print("new or last bid text:", bid.text)

        if str(bid.text) == "В игре":

            if game_for_bids == "баскетбол":
                for index, element in enumerate(basketball_bids):
                    if start_bid_sum.text == str(element):
                        bid_score = index

            if game_for_bids == "хоккей":
                for index, element in enumerate(hokkey_bids):
                    if start_bid_sum.text == str(element):
                        bid_score = index
            return 505

        if "-" not in str(bid.text) and str(bid.text) != "0":
            bid_score = 0
            print("new or last bid text:", bid.text)

        else:

            if game_for_bids == "баскетбол":
                for index, element in enumerate(basketball_bids):
                    if start_bid_sum.text == str(element):
                        bid_score = index + 1

            if game_for_bids == "хоккей":
                for index, element in enumerate(hokkey_bids):
                    if start_bid_sum.text == str(element):
                        bid_score = index + 1

        print("Сумма начальной ставки:", start_bid_sum.text)


def show_games(game):
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


def open_site(url):
    time.sleep(3)
    driver.get(url)


def login_auth():
    global is_it_loggined

    if is_it_loggined > 0:
        return 0
    is_it_loggined += 1
    try:

        WebDriverWait(driver, 10, 1).until(lambda x: x.find_element(By.XPATH,
                                                                    "/html/body/div[2]/header/wlb-top-menu/div"
                                                                    "/div[2]/wlb-login-component"
                                                                    "/div/div/a[1]").is_displayed())
        login_button = driver.find_element(By.XPATH,
                                           "/html/body/div[2]/header/wlb-top-menu/div"
                                           "/div[2]/wlb-login-component/div/div/a[1]")
        login_button.click()
        driver.execute_script("window.scrollTo(0, 50)")
        WebDriverWait(driver, 10, 1).until(lambda x: x.find_element(By.XPATH, "/html/body/div[2]/header/wlb-"
                                                                              "top-menu/div/div[2]/wlb-login-component"
                                                                              "/div/form/ul/li[3]"))
        login = driver.find_element(By.XPATH,
                                    "/html/body/div[2]/header/wlb-top-menu/div/div[2]"
                                    "/wlb-login-component/div/form/ul/li[3]")
        login.click()
        WebDriverWait(driver, 10, 1).until(lambda x: x.find_element(By.NAME, "login").is_displayed())
        login_input = driver.find_element(By.NAME, "login")
        login_input.send_keys(str(account_login))
        WebDriverWait(driver, 10, 1).until(lambda x: x.find_element(By.NAME, "passw").is_displayed())
        password_input = driver.find_element(By.NAME, "passw")
        password_input.send_keys(str(account_password))
        WebDriverWait(driver, 10, 1).until(lambda x: x.find_element(By.XPATH,
                                                                    "/html/body/div[2]/header/wlb-top-menu/div/"
                                                                    "div[2]/wlb-login-component/div/form"
                                                                    "/button").is_displayed())
        authorize = driver.find_element(By.XPATH,
                                        "/html/body/div[2]/header/wlb-top-menu/div/div[2]"
                                        "/wlb-login-component/div/form/button")
        authorize.click()
    except NoSuchElementException:
        driver.refresh()
    print("Авторизовались")


def count_of_games(game):
    global match_count

    if game == "баскетбол":
        time.sleep(2)
        for c in range(100, 0, -1):
            try:
                if driver.find_element(By.XPATH,
                                       f"/html/body/div[2]/div[2]/div/div[1]/div[1]"
                                       f"/wlb-events-list/div/div[3]/div/div[{c}]"):
                    match_count = c
                    print("Обнаружены все доступные матчи")
                    break
            except NoSuchElementException:
                pass

    if game == "хоккей":
        time.sleep(2)
        for t in range(100, 0, -1):
            try:
                if driver.find_element(By.XPATH,
                                       f"/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-events-list/div/div[3]"
                                       f"/div/div[{t}]/wlb-events-list-item/section/div"):
                    match_count = t
                    print("Обнаружены все доступные матчи")
                    break
            except NoSuchElementException:
                pass


def open_my_bids():
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 0)")

    try:
        WebDriverWait(driver, 10, 1).until(lambda x: x.find_element(By.LINK_TEXT, "Личный кабинет"))
        user_profile = driver.find_element(By.LINK_TEXT, "Личный кабинет")
        user_profile.click()
    except (NoSuchElementException, WebDriverException):
        try:
            user_profile = driver.find_element(By.XPATH, "/html/body/div[2]/header/wlb-top-menu/div/div"
                                                         "[2]/wlb-login-component/div/div[1]/a")
            user_profile.click()
        except (NoSuchElementException, WebDriverException):
            try:
                time.sleep(1)
                give = driver.find_element(By.XPATH, '//*[@id="Uoshoasieboh4fae"]/ng-component'
                                                     '/mat-dialog-content/div/a')
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
    global bid_score
    global bid_type
    global ethernet_bug_fix
    global pari_in_the_game
    b = 0
    print("Проверка результатов матча")
    time.sleep(5)

    bid_type = bid_type.lower()

    while True:
        if b == 48:
            b = 0
            driver.refresh()
            open_my_bids()

        WebDriverWait(driver, 60, ignored_exceptions=ignored_exceptions).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH,
                 "/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[2]/wlb-bet-history"
                 "/div/div[1]/table/tbody[1]/tr/td[6]/div/span")))

        if bid_score >= 5:
            print("bid score > 5")
            bid = driver.find_element(By.XPATH,
                                      "/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[2]"
                                      "/wlb-bet-history/div/div[1]/table/tbody[1]/tr/td[6]/div/span")
            try:
                bid_type_link = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div"
                                                              "[1]/wlb-personal-account/div"
                                                              "/div[2]/wlb-bet-history/div/div[1]/table/tbody[1]"
                                                              "/tr/td[2]/div/div[4]").text
            except NoSuchElementException:
                try:
                    bid_type_link = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div[1]"
                                                                  "/wlb-personal-account"
                                                                  "/div/div[2]/wlb-bet-history/div/div[1]"
                                                                  "/table/tbody[1]/tr/td[2]/div/div[3]").text
                except NoSuchElementException:
                    try:
                        bid_type_link = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div[1]"
                                                                      "/wlb-personal-account/div/div[2]/wlb-bet-history"
                                                                      "/div/div[1]/table/tbody[1]/tr/td[2]"
                                                                      "/div/div[2]").text

                    except NoSuchElementException:
                        print("error4")
                        bid_type_link = "Чет"

            if str(bid.text) == "В игре":
                print("В игре")
                time.sleep(5)
                b += 1
                ethernet_bug_fix = True
                continue

            if "-" not in str(bid.text) and str(bid.text) != "0":
                bid_score = 0
                ethernet_bug_fix = False
                pari_in_the_game = False
                print("check bid results bid score: ", bid_score)

                if bid_type_link == "Чет":
                    bid_type = "нечет"
                else:
                    bid_type = "чет"

                if bot_disable > 0:
                    print('Ctrl + Z / Ctrl + Q Была нажата')
                    driver.close()
                    driver.quit()
                else:
                    next_bid_timer()
                    break

            else:
                pari_in_the_game = False
                bid_score += 1
                ethernet_bug_fix = False
                if bid_score == 10:
                    driver.quit()
                next_bid_timer()
                break

        else:
            try:
                first_part_results = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div[1]"
                                                                   "/wlb-personal-account/div/div[2]/wlb-bet-history"
                                                                   "/div/div[1]/table/tbody[1]/tr/td[4]"
                                                                   "/div/div/span").text

                if "Через" in str(first_part_results) or "1Ч" in str(first_part_results) or "1П" in \
                        str(first_part_results):

                    time.sleep(5)
                    b += 1
                    ethernet_bug_fix = True
                    continue
                elif "Пер" in str(first_part_results):
                    print("Обнаружен Пер")
                    print(str(first_part_results))
                    spec_index1 = 3
                    spec_index2 = 4

                elif "2Ч" in str(first_part_results) or "3Ч" in str(first_part_results) or "2П" in \
                        str(first_part_results) or "3П" in str(first_part_results) or "4Ч" in str(first_part_results) \
                        or "4П" in str(first_part_results):

                    print("Elif1")
                    print(str(first_part_results))
                    spec_index1 = 5
                    spec_index2 = 6

                elif "-:-" in str(first_part_results):
                    print("Elif2")
                    time.sleep(5)
                    b += 1
                    ethernet_bug_fix = True
                    continue

                elif "(" not in str(first_part_results) and ":" in str(first_part_results):
                    if str(first_part_results) != "0:0":
                        print("Elif3")
                        print(bid_type)
                        print(str(first_part_results))
                        spec_index1 = 0
                        spec_index2 = 1
                    else:
                        print("wf")
                        time.sleep(5)
                        b += 1
                        ethernet_bug_fix = True
                        continue
                else:
                    print("error1")
                    try:
                        print('error1.1')
                        driver.find_element(By.XPATH,
                                            "/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div"
                                            "/div[2]/wlb-bet-history/div/div[1]/table/tbody[20]/tr/td[4]/div/div"
                                            "/span/div")

                        print(str(first_part_results))
                        spec_index1 = 0
                        spec_index2 = 1
                        b += 1
                        ethernet_bug_fix = True
                        time.sleep(5)
                    except NoSuchElementException:
                        print('error1.2')
                        time.sleep(5)
                        b += 1
                        ethernet_bug_fix = True
                        continue

            except NoSuchElementException:
                print("Результат пустой на данный момент")
                time.sleep(5)
                b += 1
                ethernet_bug_fix = True
                continue
            try:
                res_nums = [int(s) for s in re.findall(r'-?\d+\.?\d*', first_part_results)]
                total = int(res_nums[spec_index1]) + int(res_nums[spec_index2])
            except IndexError:
                print("Index Error")
                time.sleep(5)
                b += 1
                ethernet_bug_fix = True
                continue

            print(total, int(res_nums[spec_index1]), int(res_nums[spec_index2]), total % 2)
            if total % 2 == 0:
                game_result = "чет"
                print("результат четный")
            else:
                game_result = "нечет"
                print("результат не четный")
            if bid_type == game_result:
                print("выйгрыш")
                print(bid_type, "0", game_result)
                ethernet_bug_fix = False
                pari_in_the_game = False
                print("Изменяем bid score!1.1")
                bid_score = 0
                print(bid_score, "bid score")
                try:
                    bid_type_link = driver.find_element(By.XPATH,
                                                        "/html/body/div[2]/div[2]/div/div[1]/div[1]"
                                                        "/wlb-personal-account/div/div[2]/wlb-bet-history"
                                                        "/div/div[1]/table/tbody[1]/tr/td[2]/div/div[4]")
                except NoSuchElementException:
                    try:
                        bid_type_link = driver.find_element(By.XPATH,
                                                            "/html/body/div[2]/div[2]/div/div[1]/div[1]"
                                                            "/wlb-personal-account/div/div[2]/wlb-bet-history/div"
                                                            "/div[1]/table/tbody[1]/tr/td[2]/div/div[3]")
                    except NoSuchElementException:
                        try:
                            bid_type_link = driver.find_element(By.XPATH,
                                                                "/html/body/div[2]/div[2]/div/div[1]/div[1]"
                                                                "/wlb-personal-account/div/div[2]/wlb-bet-history/div"
                                                                "/div[1]/table/tbody[1]/tr/td[2]/div/div[2]")

                        except NoSuchElementException:
                            bid_type_link = "Чет"
                            print("error2")

                if bid_type_link.text == "Чет":
                    bid_type = "нечет"
                else:
                    bid_type = "чет"

                print(bid_type, "Bid_Type")

                if bot_disable > 0:
                    print('Ctrl + Z / Ctrl + Q Была нажата')
                    driver.close()
                    driver.quit()
                else:
                    next_bid_timer()
                    break

            else:
                print("проигрыш")
                print(bid_type, game_result)
                print("Изменяем bid score!2")
                print("bid_score", bid_score)
                bid_score += 1
                pari_in_the_game = False
                print(bid_score, "changed")
                ethernet_bug_fix = False
                if bid_score == 10:
                    driver.quit()
                next_bid_timer()
                break


def get_bid_type_table():
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
                                    "/html/body/div[2]/div[2]/div/div[2]/div/div/div[1]/div[1]/div"
                                    "/div[2]/div[2]/div/div[3]/div[1]/div[2]/input")
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
    time.sleep(3)  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    try:
        WebDriverWait(driver, 14, ignored_exceptions=ignored_exceptions).until(
            expected_conditions.presence_of_element_located((By.LINK_TEXT, '«Мои пари»')))

        pop_up = driver.find_element(By.LINK_TEXT, '«Мои пари»')
        pop_up.click()
        return 1

    except (NoSuchElementException, TimeoutException):
        WebDriverWait(driver, 30, 1).until(lambda x: x.find_element(By.XPATH, '//*[@id="popup-clear-coupon"]'
                                                                              '/div[5]').is_displayed())
        message = driver.find_element(By.XPATH, '//*[@id="popup-clear-coupon"]/div[5]').text
        print(message)
        try:
            nums = [float(s) for s in re.findall(r'-?\d+\.?\d*', message)]
            print(nums)
            if nums[1] >= 1.88:
                print("confirm")
                WebDriverWait(driver, 30, 1).until(lambda x: x.find_element(By.XPATH, '//*[@id="popup-clear-coupon"]'
                                                                                      '/div[6]/div[2]'
                                                                                      '/span').is_displayed())
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
        except IndexError:
            return 3


def now_matches_page_open():
    print("now match_ open ")
    WebDriverWait(driver, 30, 1).until(lambda x: x.find_element(By.XPATH, "//span[text()='Сейчас']").is_displayed())
    in_game = driver.find_element(By.XPATH, "//span[text()='Сейчас']")
    in_game.click()
    try:
        show_games(game=game_for_bids)
    except (NoSuchElementException, TimeoutException):
        print("Нет онлайн матчей")
        return 0
    time.sleep(2)


def already_started_match_bid():
    global bid_type
    global coefficient
    global bid_score
    global match_count
    global already_started_matches
    global table_title_p_p
    global pari_in_the_game

    d = datetime.datetime.now()
    date1 = datetime.datetime.strptime(str(d), "%Y-%m-%d %H:%M:%S.%f")
    allowed_periods = [" 20", "1П 19", "1П 18", "1П 17", "1П 16", "1П 15", "1П 14", "1П 13"]
    bad_countries = ["ЛИГА ПРО, 3 Х 10"]
    bid_type = "нечет"
    good_games = []

    finded = now_matches_page_open()
    if finded == 0:
        return 5

    live_pari = driver.find_elements(By.CSS_SELECTOR, "[title='На данное событие принимаются Live-пари']")
    print(live_pari)

    for online in live_pari:
        print(online)
        match_info = online.find_element(By.XPATH, "..")

        match_period = match_info.find_element(By.XPATH, "./div[1]")

        match_title = match_info.find_element(By.XPATH, "./div[3]/a/h2/div/span[1]")
        have_allowed_period = False

        for period in allowed_periods:
            print(match_period.text)
            print(period)
            if str(match_period.text).find(period) >= 0:
                print("Допустимый период")
                have_allowed_period = True
                break
            else:
                print("Недопустимый период")

        if have_allowed_period:
            good_games.append(match_title.text)

    while True:
        print(good_games, "gg")

        finded = now_matches_page_open()
        if finded == 0:
            return 5

        if len(good_games) == 0:
            return 5

        for l in good_games:
            print(l)
            bad_league_finded = False
            f_match_with_title = driver.find_element(By.XPATH, f"//span[text()='{l}']")
            f_match_with_title.click()
            time.sleep(2)
            try:
                country = driver.find_element(By.XPATH, '//*[@id="sticky-header-top"]/wlb-market-book-header'
                                                        '/div[2]/div').text

                for sent in bad_countries:
                    print(sent)
                    print(str(country).find(sent))
                    if str(country).find(sent) == -1:
                        print("Лига подходит")
                    else:
                        bad_league_finded = True

                if bad_league_finded:
                    if bid_score <= 5:
                        print(str(country), "Страна не подходит")
                        good_games.remove(l)
                        now_matches_page_open()
                        break

            except NoSuchElementException:
                print("Не найдена панель с лигами")

            date2 = datetime.datetime.now()
            delta = (date1 - date2).total_seconds()
            delta = abs(delta)

            print(int(delta), " delta")
            if int(delta) >= 900:
                return 0

            try:
                time.sleep(2)
                get_bid_type_table()
            except NoSuchElementException:
                print("нет таблицы")
                now_matches_page_open()
                good_games.remove(l)
                time.sleep(1)
                break

            try:
                try:
                    time.sleep(2)
                    part = table_title_p_p.find_element(By.CSS_SELECTOR, "[title='1 период']")
                    part_parent = part.find_element(By.XPATH, "..")
                    part_parent_parent = part_parent.find_element(By.XPATH, "..")

                except NoSuchElementException:
                    print("Нет первого периода")
                    good_games.remove(l)
                    now_matches_page_open()
                    break
                button = part_parent_parent.find_element(By.XPATH, "./div[3]/div")
                coefficient = part_parent_parent.find_element(By.XPATH, "./div[3]/div/span[4]")
                print("Кнопка и коэффицент")
            except NoSuchElementException:
                print("Не могу найти кнопку нечет.")
                now_matches_page_open()
                continue

            if "locked" in button.get_attribute("class"):
                print("кнопка не активна")
                good_games.remove(l)
                now_matches_page_open()
                continue

            try:
                print("Проверяем коэфиценты")
                time.sleep(2)
                print(coefficient.text)

                if float(coefficient.text) >= 1.88:
                    button.click()
                    try:
                        accept_result = accept_bid(game=game_for_bids)
                        if accept_result == 0:
                            print("Не подошло  новое значение таблицы")
                            now_matches_page_open()
                            continue
                        elif accept_result == 1:
                            time.sleep(3)
                            print("check bid res")
                            pari_in_the_game = True
                            return 1
                        elif accept_result == 3:
                            print("Винлайн отверг ставку")
                            good_games.remove(l)
                            now_matches_page_open()
                            continue
                    except NoSuchElementException:
                        print("Не могу найти поле ввода или кнопку Принять")
                        now_matches_page_open()
                        continue
                else:
                    print("Маленький коэфицент")
                    now_matches_page_open()
                    continue

            except ValueError:
                print("couldn't convert string to float")


def get_all_games(game):
    print("1")
    WebDriverWait(driver, 30, 1).until(lambda x: x.find_element(By.XPATH, "//span[text()='Ближайшие']").is_displayed())
    nearest = driver.find_element(By.XPATH, "//span[text()='Ближайшие']")
    print("2")
    nearest.click()

    if game == "баскетбол":

        while True:
            try:
                WebDriverWait(driver, 30, 1).until(
                    lambda x: x.find_element(By.XPATH, '//*[@id="sticky-header-bottom"]/div/div[1]').is_displayed())
                panel = driver.find_element(By.XPATH, '//*[@id="sticky-header-bottom"]/div/div[1]')
                WebDriverWait(panel, 30, 1).until(
                    lambda x: x.find_element(By.CSS_SELECTOR, '[title="Баскетбол"]').is_displayed())
                basketball = panel.find_element(By.CSS_SELECTOR, '[title="Баскетбол"]')
                break
            except (NoSuchElementException, TimeoutException):
                continue

        if "filter-active" not in basketball.get_attribute("class"):
            basketball.click()
            time.sleep(2)

        driver.execute_script("window.scrollTo(0, 2337)")

        count_of_games(game=game)

        driver.execute_script("window.scrollTo(0, 0)")

    if game == "хоккей":

        while True:
            try:
                WebDriverWait(driver, 30, 1).until(
                    lambda x: x.find_element(By.XPATH, '//*[@id="sticky-header-bottom"]/div/div[1]').is_displayed())
                panel = driver.find_element(By.XPATH, '//*[@id="sticky-header-bottom"]/div/div[1]')
                WebDriverWait(panel, 30, 1).until(
                    lambda x: x.find_element(By.CSS_SELECTOR, '[title="Хоккей"]').is_displayed())
                hokkey = panel.find_element(By.CSS_SELECTOR, '[title="Хоккей"]')
                break
            except (NoSuchElementException, TimeoutException):
                continue

        if "filter-active" not in hokkey.get_attribute("class"):
            hokkey.click()
            time.sleep(2)

        driver.execute_script("window.scrollTo(0, 2337)")
        count_of_games(game="хоккей")

        driver.execute_script("window.scrollTo(0, 0)")

    print("Получены все доступные игры")


def get_last_bid_type():
    global bid_type
    global basketball_bids
    global hokkey_bids
    global bid_score
    global ethernet_bug_fix
    global own_bid_choice
    global start_chet
    print("get last bd type")
    print(bid_score, "bd score")

    open_my_bids()

    new_or_last()

    if own_bid_choice == 1:
        own_bid_choice = 0
        return 0

    bid = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div"
                                        "/div[2]/wlb-bet-history/div/div[1]/table/tbody[1]/tr/td[6]/div/span")

    print(bid.text, "bid text")
    print(ethernet_bug_fix, "ethernet bug fix")

    if (str(bid.text) == "В игре" or ethernet_bug_fix) and pari_in_the_game:
        print("get last, ethernet bg fix in game")
        try:
            bid_type = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account"
                                                     "/div/div[2]/wlb-bet-history/div/div[1]/table/tbody[1]/tr"
                                                     "/td[2]/div/div[4]").text

        except NoSuchElementException:
            try:
                bid_type = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div[1]"
                                                         "/wlb-personal-account/"
                                                         "div/div[2]/wlb-bet-history/div/div[1]/table/tbody[1]/tr/"
                                                         "td[2]/div/div[3]").text
            except NoSuchElementException:
                try:
                    bid_type = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div[1]"
                                                             "/wlb-personal-account/div/div[2]/wlb-bet-history/div"
                                                             "/div[1]/table/tbody[1]/tr/td[2]/div/div[2]").text

                except NoSuchElementException:
                    print("error4")
                    bid_type = "чет"
        return 1
    if start_chet == 1:
        start_chet = 0
        bid_type = "чет"
        return 15

    if not pari_in_the_game:
        return 66

    try:
        bid_type_link = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[1]/div[1]"
                                                      "/wlb-personal-account/div/div[2]/wlb-bet-history"
                                                      "/div/div[1]/table/tbody[1]/tr/td[2]/div/div[4]")

    except NoSuchElementException:
        try:
            bid_type_link = driver.find_element(By.XPATH,
                                                "/html/body/div[2]/div[2]/div/div[1]/div[1]"
                                                "/wlb-personal-account/div/div[2]/wlb-bet-history/div/div"
                                                "[1]/table/tbody[1]/tr/td[2]/div/div[3]")
        except NoSuchElementException:
            try:
                bid_type_link = driver.find_element(By.XPATH,
                                                    "/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account"
                                                    "/div/div[2]/wlb-bet-history/div/div[1]/table/tbody[1]"
                                                    "/tr/td[2]/div/div[2]")

            except NoSuchElementException:
                bid_type_link = "0"
    print(bid.text)

    if "-" not in str(bid.text) and str(bid.text) != "0":
        print(bid_score, "bd score")
        print("Изменяем bid score!6asd")
        bid_score = 0
        print(bid_score, "bd scoreasd")

        if bid_type_link.text == "Чет":
            bid_type = "нечет"
        else:
            bid_type = "чет"

    else:
        if bid_type_link.text == "Чет":
            bid_type = "чет"
        else:
            bid_type = "нечет"


def next_matches():
    global already_started_matches

    try:
        for v in range(0, 11):
            try:
                already_started_matches[v] = driver.find_element(By.XPATH, f"/html/body/div[2]/div[2]/div/"
                                                                           f"div[1]/div[1]/wlb-events-list/div"
                                                                           f"/div[3]/div/div"
                                                                           f"[{v + 1}]/wlb-events-list-item/section"
                                                                           f"/div/div[1]/div"
                                                                           f"[2]/a/h2/span[1]").text
            except NoSuchElementException:
                already_started_matches[v] = driver.find_element(By.XPATH, f"/html/body/div[2]/div[2]/div"
                                                                           f"/div[1]/div[1]/wlb-events-list/div"
                                                                           f"/div[3]/div/div[{v + 1}]"
                                                                           f"/wlb-events-list-item/section/div/div"
                                                                           f"[1]/div[2]/a/h2/div/span[1]").text

    except NoSuchElementException:
        return 0


def do_bid():
    global coefficient
    global bid_score
    global bid_type
    global match_count
    global pari_in_the_game
    print("do bid")

    get_all_games(game=game_for_bids)
    time.sleep(1)
    try:
        delete_bid = driver.find_element(By.CSS_SELECTOR, '[title="Удалить событие из купона"]')
        delete_bid.click()
    except NoSuchElementException:
        print("Нет купонов")
    for i in range(1, match_count + 2):
        try:

            WebDriverWait(driver, 3, 1).until(
                lambda x: x.find_element(By.XPATH, f"/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-events-list"
                                                   f"/div/div[3]/div/div[{str(i)}]/wlb-events-list-item/section/div"
                                                   f"/div[1]/div[2]/a").is_displayed())
            game_match = driver.find_element(By.XPATH,
                                             f"/html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-events-list/div/div[3]"
                                             f"/div/div[{str(i)}]/wlb-events-list-item/section/div/div[1]/div[2]/a")
            print(game_match.text)
            if game_for_bids == "хоккей":
                next_matches()
        except (NoSuchElementException, TimeoutException):

            if i >= match_count + 1:
                i = 1
            get_all_games(game=game_for_bids)
            continue
        game_match.click()
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 3350)")
        time.sleep(2)

        try:
            get_bid_type_table()
            time.sleep(2)
        except NoSuchElementException:
            print("нет таблицы")
            get_all_games(game_for_bids)
            continue
        if game_for_bids == "баскетбол":
            try:
                league = driver.find_element(By.XPATH,
                                             '//*[@id="sticky-header-top"]/wlb-market-book-header/div[2]/div').text
                print(str(league))

                sentences = ["1551651"]

                bad_league_finded = False

                for word in sentences:
                    print(word)
                    print(str(league).find(word))
                    if str(league).find(word) == -1:
                        print("Лига подходит")
                    else:
                        bad_league_finded = True

                if bad_league_finded:
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
                    button = part_parent_parent.find_element(By.XPATH, "./div[2]/div")
                    coefficient = part_parent_parent.find_element(By.XPATH, "./div[2]/div/span[4]")
                    print("кнопка и коэффицент")
                    print(coefficient.text)
                else:
                    button = part_parent_parent.find_element(By.XPATH, "./div[3]/div")
                    coefficient = part_parent_parent.find_element(By.XPATH, "./div[3]/div/span[4]")
                    print("кнопка и коэффицент")
                    print(coefficient.text)

            except NoSuchElementException:
                print("Не могу найти кнопку")
                get_all_games(game_for_bids)
                continue

            if "locked" in button.get_attribute("class"):
                print("кнопка не активна")
                get_all_games(game_for_bids)
                continue

            driver.execute_script("window.scrollTo(0, 0)")

            try:
                if float(coefficient.text) >= main_count:
                    button.click()
                    try:
                        accept_result = accept_bid(game=game_for_bids)
                        if accept_result == 0:
                            print("Не подошло  новое значение таблицы")

                            get_all_games(game_for_bids)
                            continue
                        elif accept_result == 1:
                            time.sleep(3)
                            pari_in_the_game = True
                            print("check bid res")
                        elif accept_result == 3:
                            print("Винлайн отверг ставку")
                            now_matches_page_open()
                            i -= 1
                            continue
                    except NoSuchElementException:
                        print("Не могу найти поле ввода или кнопку Принять")
                        get_all_games(game_for_bids)
                        continue
                    break

                else:
                    print("Не подходящий коэфицент")
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

                sentences = ["ЛИГА ПРО, 3 Х 10"]

                bad_league_finded = False

                for word in sentences:
                    print(word)
                    print(str(country).find(word))
                    if str(country).find(word) == -1:
                        print("Лига подходит")
                    else:
                        bad_league_finded = True

                if bad_league_finded:
                    if bid_score <= 4:
                        print(str(country), "лига не подходит")
                        get_all_games(game_for_bids)
                        continue

            except NoSuchElementException:
                print("Нет Панели с лигами")

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
                coefficient = part_parent_parent.find_element(By.XPATH, "./div[3]/div/span[4]")
            except NoSuchElementException:
                print("Не могу найти кнопку нечет.")
                get_all_games(game_for_bids)
                continue

            if "locked" in button.get_attribute("class"):
                print("кнопка не активна")
                get_all_games(game_for_bids)
                continue

            driver.execute_script("window.scrollTo(0, 0)")

            try:
                print("Проверяем коэфиценты")
                time.sleep(2)
                print(coefficient.text)

                if float(coefficient.text) >= 1.88:
                    button.click()
                    try:
                        accept_result = accept_bid(game=game_for_bids)
                        if accept_result == 0:
                            print("Не подошло  новое значение таблицы")
                            get_all_games(game_for_bids)
                            continue
                        elif accept_result == 1:
                            time.sleep(3)
                            print("check bid res")
                            pari_in_the_game = True
                        elif accept_result == 3:
                            print("Винлайн отверг ставку")
                            now_matches_page_open()
                            i -= 1
                            continue
                    except NoSuchElementException:
                        print("Не могу найти поле ввода или кнопку Принять")
                        driver.close()
                        driver.quit()

                    return 0
                else:
                    print("Маленький коэфицент")
                    get_all_games(game_for_bids)
                    continue

            except ValueError:
                print("couldn't convert string to float")
                get_all_games(game_for_bids)
                continue

        if i > match_count:
            i = 0
            print("Закончились игры 2")
            continue
        else:
            time.sleep(5)


def parent_func():
    time.sleep(3)
    get_info()
    open_site("https://winline.ru/")
    print(bid_score)
    time.sleep(1)
    login_auth()
    time.sleep(2)
    glbt = get_last_bid_type()
    if glbt == 1:
        check_bid_result()
    if game_for_bids == "хоккей":
        alsmb = already_started_match_bid()
        if alsmb == 1:
            return 0
    do_bid()


if __name__ == '__main__':
    while True:
        try:
            parent_func()
        except (TimeoutException, WebDriverException):
            time.sleep(1)
            print("Потеря соединения")
            continue

# -:- 0:0
# время начала - "через минута значок - /html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/di
# v/div[2]/wlb-bet-history/div/div[1]/table/tbody[1]/tr/td[4]/div/div/span Через 3'
# значок /html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[2]/wlb-
# bet-history/div/div[1]/table/tbody[1]/tr/td[4]/div/a
# пустота /html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[2]/wlb-
# bet-history/div/div[1]/table/tbody[1]/tr/td[4]/div/div
# результат 1ч - /html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div
# [2]/wlb-bet-history/div/div[1]/table/tbody[1]/tr/td[4]/div/div/span | 1Ч 07:57 5:2 (5:2) -
# скобочки идут на новой строке
# бывает вот так : 1Ч 06-30 12:4 (12:4) | после 30 - все остальное на новой строке  (на
# новую если двузначное число ((сравни)))
# значок в игре - /html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[2]
# /wlb-bet-history/div/div[1]/table/tbody[1]/tr/td[4]/div/a
# перерыв  /html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[2]/wlb-
# bet-history/div/div[1]/table/tbody[1]/tr/td[4]/div/div/span Пер.1 27:12 (27:12) - начало скобочек на след строке
# 2Ч 09:58 27:12 (27:12 - 0:0) начиная с 27 новая строка
# /html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[2]/wlb-bet-history
# /div/div[1]/table/tbody[1]/tr/td[4]/div/div/span - конечный результат  27:12
# /html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[2]/wlb-bet-history
# /div/div[1]/table/tbody[20]/tr/td[4]/div/div/span
# /html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[2]/wlb-bet-history
# /div/div[1]/table/tbody[20]/tr/td[4]/div/div/span/div
# /html/body/div[2]/div[2]/div/div[1]/div[1]/wlb-personal-account/div/div[2]/wlb-bet-history
# /div/div[1]/table/tbody[1]/tr/td[4]/div/a
# https://chrome.google.com/webstore/detail/free-vpn-proxy-and-ad-blo/hipncndjamdcmphkgngojegjblibadbe?hl=ru

# //*[@id="popup-clear-coupon"]/div[5] - текст
# //*[@id="popup-clear-coupon"]/div[2] - надпись сверху
# //*[@id="popup-clear-coupon"]/div[6]/div[1]/span - отмена
# //*[@id="popup-clear-coupon"]/div[6]/div[2]/span
