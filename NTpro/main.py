from prompt_toolkit import prompt
import datetime
from prompt_toolkit.completion import WordCompleter
from check_correctly import *
from bank import *

commands_completer = WordCompleter(
    ['deposit', 'withdraw', 'show_bank_statement', 'quit', 'client', 'amount', 'description', 'since', 'till'])
CLIENTS_SESSIONS = {}

print('Service started !\n')


def splitting(command):
    dict = {'main_command': re.split(' ', command)[0], 'date': datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")}
    all_flags = re.split('--', command)[1:4]
    for flag in all_flags:
        dict[re.split('=', flag)[0]] = re.split('=', flag)[1].replace('"','').strip()
    return dict


def main():
    while True:
        full_command = prompt('> ', completer=commands_completer)

        # Проверяем команду на корректность синтаксиса
        if full_command == 'quit':
            break
        if not Is_it_right_command(re.split(' ', full_command)[0]):
            print('Такой команды нет, повторите ещё раз\n')
            continue
        if not Is_there_right_options(full_command):
            print('Ошибка')
            continue

        # Разбиваем строку
        split_command = splitting(full_command)

        # Работаем со счётом клиента
        client = split_command['client'].replace(' ','1')
        date = split_command['date']
        main_command = split_command['main_command']

        # Создаём счёт, если он не был раньше создан
        if client not in CLIENTS_SESSIONS:
            client_account = Bank(client)
            CLIENTS_SESSIONS[client] = client_account
        else:
            for key in CLIENTS_SESSIONS:
                if client == key:
                    client_account = CLIENTS_SESSIONS[client]

        # Если запросили депозит
        if main_command == 'deposit':
            client_account.deposit(date, split_command['description'], float(split_command['amount']))
            print(main_command, ' operation was successful\n')

        # Если запросили вывод
        elif main_command == 'withdraw':
            client_account.withdrawals(date, split_command['description'], float(split_command['amount']))
            print(main_command, ' operation was successful\n')

        # Если запросили показать состояние счёта
        elif main_command == 'show_bank_statement':
            client_account.give_me_report(split_command['since'],split_command['till'])


if __name__ == '__main__':
    main()
