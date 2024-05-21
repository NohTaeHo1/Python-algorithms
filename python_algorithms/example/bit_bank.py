import random

from example.utils import myRandom


class BitBank:

    def __init__(self):
        self.name: str
        self.account_number: str
        self.money: int

        print('''
            [요구사항(RFP)]
            은행이름은 비트은행이다.
            입금자 이름(name), 계좌번호(account_number), 금액(money) 속성값으로 계좌를 생성한다.
            계좌번호는 3자리-2자리-6자리 형태로 랜덤하게 생성된다.
            예를들면 123-12-123456 이다.
            금액은 100 ~ 999 사이로 랜덤하게 입금된다. (단위는 만단위로 암묵적으로 판단한다)
            ''')

    @property
    def name(self) -> str: return self._name

    @name.setter
    def name(self, name): self._name = name

    @property
    def account_number(self) -> str: return self._account_number

    @account_number.setter
    def account_number(self, account_number): self._account_number = account_number

    @property
    def money(self) -> str: return self._money

    @money.setter
    def money(self, money): self._money = money

    def create_account(self):
        self.name = input('이름: ')
        self.account_number = str(f'{myRandom(0, 1000):03}') + '-' + str(f'{myRandom(0, 99):02}') + '-' + str(
            f'{myRandom(0, 999999):06}')
        self.money = myRandom(100, 900)

        print("이름: %s, 계좌번호: %s, 금액: %d " % (self.name, self.account_number, self.money))


def main():
    while True:
        menu = input('0-종료  1. 계좌개설 : ')
        if menu == '0':
            break
        if menu == '1':
            BitBank().create_account()


if __name__ == '__main__':
    main()
