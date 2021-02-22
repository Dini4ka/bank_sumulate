import sqlite3
from prettytable import PrettyTable


class Bank:

    def __init__(self, client):

        self.dict = {'deposits': float(0), 'withdrawals': float(0), 'balance': float(0)}
        self.client = client
        self.conn = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES |
                                                             sqlite3.PARSE_COLNAMES)
        self.cursor = self.conn.cursor()
        # Создание таблицы
        self.cursor.execute(f"""CREATE TABLE {self.client}
                          (id INTEGER PRIMARY KEY,Date TEXT, Description text, 
                          Withdrawals FLOAT,
                          Deposits FLOAT, 
                          Balance FLOAT default 0)
                                        """)

    def __getitem__(self, atr):
        return self.dict[atr]

    def deposit(self, date, description, deposit):

        records = len(self.cursor.execute(f'select  * from {self.client}').fetchall())
        self.dict['balance'] += deposit

        result = [records, date, description, '', str(float(deposit)) + '$', str(self.dict['balance']) + '$']
        self.cursor.execute(f"""INSERT INTO {self.client}
                                VALUES(?,?,?,?,?,?)""", result)
        self.conn.commit()

    def withdrawals(self, date, description, withdrawals):
        records = len(self.cursor.execute(f'select  * from {self.client}').fetchall())

        if self.dict['balance'] < withdrawals:
            print(f'Сумма вывода превышает ваш баланс на данный момент: {self.dict["balance"]}$')
        else:
            self.dict['balance'] -= withdrawals

            result = [records, date, description, str(float(withdrawals)) + '$', '', str(self.dict['balance']) + '$']
            self.cursor.execute(f"""INSERT INTO {self.client}
                                            VALUES(?,?,?,?,?,?)""", result)
            self.conn.commit()

    def give_me_report(self, since, till):

        try:
            # Смотрим первую дату транзакции
            first_date = self.cursor.execute(f"SELECT Date  FROM {self.client} WHERE id = 0").fetchone()[0]
            if first_date > since and first_date > till:
                print('За этот период не было транзакций\n')
                return 0
        except:
            print('у пользователя не было ни одной транзакции')
            return 0

        # Считаем кол-во депозитов за этот срок
        deposits = self.cursor.execute(f"SELECT Deposits  FROM {self.client} WHERE Date BETWEEN (?) AND (?)",
                                       (since, till)).fetchall()
        deposits_int = 0
        for deposit in deposits:
            if deposit == ('',):
                continue
            deposits_int += float(deposit[0][:-1])

        # Считаем кол-во выводов за этот срок
        withdrawals = self.cursor.execute(f"SELECT Withdrawals  FROM {self.client} WHERE Date BETWEEN (?) AND (?)",
                                          (since, till)).fetchall()
        withdrawals_int = 0
        for withdrawal in withdrawals:
            if withdrawal == ('',):
                continue
            withdrawals_int += float(withdrawal[0][:-1])

        # Определяем баланс до всех транзакций
        prev_id = self.cursor.execute(f"SELECT id  FROM {self.client} WHERE Date BETWEEN (?) AND (?) LIMIT 1",
                                      (since, till)).fetchone()
        if int(prev_id[0]) == 0:
            prev_balance_int = str(float(0)) + '$'
        else:
            prev_balance = self.cursor.execute(f"SELECT Balance  FROM {self.client} "
                                               f"WHERE id LIKE {prev_id[0] - 1}").fetchone()
            prev_balance_int = prev_balance[0]

        # Забираем из БД все записи за текующий срок
        cur = self.cursor.execute(
            f"SELECT Date,Description,Withdrawals,Deposits,Balance  FROM {self.client} WHERE Date BETWEEN (?) AND (?) "
            f"GROUP BY Date",
            (since, till)).fetchall()

        # Создаём таблицу и задаём стили
        x = PrettyTable()
        x.field_names = ["Date", "Description", "Withdrawals", "Deposits", "Balance"]
        x.align["Withdrawals"] = x.align["Deposits"] = x.align["Balance"] = 'r'
        x.align["Description"] = 'l'

        # Строка с балансом до всех транзакций
        x.add_row(['', 'Previous balance', '',
                   '', prev_balance_int])

        # Заносим в таблицу записи из БД
        x.add_rows(cur)

        # Добавляем строку с отчётом
        x.add_row(['', 'Totals', str(float(withdrawals_int)) + '$',
                   str(float(deposits_int)) + '$', str(self.dict['balance']) + '$'])

        print(x)
        print('\n')

