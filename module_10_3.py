from threading import Thread, Lock
from random import randint
from time import sleep


class Bank:
    def __init__(self):
        self.balance = 0
        self.lock = Lock()

    def deposit(self):
        for _ in range(100):
            lot = randint(50, 500)
            self.balance += lot
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()
            print(f"Пополнение: {lot}. Баланс: {self.balance}")
            sleep(0.001)

    def take(self):
        for _ in range(100):
            lot = randint(50, 500)
            print(f"Запрос на {lot}")
            if self.balance >= lot:
                self.balance -= lot
                print(f"Снятие: {lot}. Баланс: {self.balance}")
            else:
                print(f"Запрос отклонён, недостаточно средств")
                self.lock.acquire()
            sleep(0.001)


bk = Bank()

# Т.к. методы принимают self, в потоки нужно передать сам объект класса Bank
th1 = Thread(target=Bank.deposit, args=(bk,))
th2 = Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')
