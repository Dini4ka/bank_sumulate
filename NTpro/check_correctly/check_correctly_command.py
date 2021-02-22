import re
import datetime


def Is_it_right_command(command_name):
    commands = ['deposit', 'withdraw', 'show_bank_statement', 'quit']
    if command_name not in commands:
        return False
    else:
        return True


def Money_check(command_name):
    for option in command_name.split('--'):
        if 'amount' in option:
            money = option.split('=')[1]
            try:
                money = float(money)
            except:
                print('введите корректную сумму')
                return False
            if money < 0:
                print('сумма не может быть отрицательной или равной нулю')
                return False

    return True

def Date_check(command_name):
    till = ''
    since = ''

    command_name = command_name.replace('\n', ' ')

    for option in command_name.split('--'):
        if 'till' in option:
            till = option.split('=')[1].replace('"', '').strip()
        if 'since' in option:
            since = option.split('=')[1].replace('"', '').strip()

    print(till)
    print(since)

    if since > till:
        print('неправильный промежуток дат')
        return False
    try:
        datetime.datetime.strptime(since, "%Y-%m-%d %H:%M:%S")
        datetime.datetime.strptime(till, "%Y-%m-%d %H:%M:%S")
    except:
        print("неправильный формат времени")
        return False

    return True


def Is_there_right_options(command_name):
    is_it_right = True
    options = ['client', 'amount', 'description']
    options_for_show = ['client', 'since', 'till']
    main_command = re.split(' ', command_name)[0]
    if main_command == 'deposit' or main_command == 'withdraw':
        count = 0
        for option in re.split('--', command_name):
            if re.split('=', option)[0] not in options:
                continue
            count += 1
        if count != 3:
            print('вы неправильно ввели опции и/или указали не все необходимые опции')
            return False
        is_it_right = Money_check(command_name)
        return is_it_right
    if main_command == 'show_bank_statement':
        count = 0
        for option in re.split('--', command_name):
            if re.split('=', option)[0] not in options_for_show:
                continue
            count += 1
        if count != 3:
            print('вы неправильно ввели опции и/или указали не все необходимые опции')
            return False
        is_it_right = Date_check(command_name)
        return is_it_right
