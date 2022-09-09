def get_info():
    global account_login
    global account_password
    global game_for_bids
    global new_or_last_var
    global numxz

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