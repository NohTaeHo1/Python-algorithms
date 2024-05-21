class Contract:
    members = {}

    def add(self) -> {}:
        name = input('이름 입력: ').title()
        phone = input('전화번호 입력: ')
        self.members[name] = phone
        print('----------')
        print(f'*****{name} 입력 완료*****')
        print(f'{name}:', phone)
        print('----------')
        return

    def find(self):
        name = input('검색할 이름 입력: ').title()
        phone = self.members.get(name, '존재하지 않습니다.')
        print('----------')
        print(f'{name}:', phone)
        print('----------')

    def update(self):
        name = input('수정할 이름 입력: ').title()
        if name not in self.members.keys():  # members.keys(): key만 추출하기
            print('----------')
            print(f'{name} 회원은 존재하지 않습니다.')
            print('----------')
        else:
            phone = input('새로운 전화번호 입력: ')
            self.members[name] = phone
            print('----------')
            print(f"*****{name} 수정 완료*****")
            print(f'{name}:', phone)
            print('----------')

    def delete(self):
        name = input('삭제할 이름 입력: ').title()
        if name not in self.members.keys():
            print('----------')
            print(f'{name} 회원은 존재하지 않습니다.')
            print('----------')
        else:
            ask = input(f"{name} 회원을 정말로 삭제할까요?(y): ").lower()
            if ask == 'y':
                del self.members[name]
                print('----------')
                print(f"*****{name} 삭제 완료*****")
                print('----------')
            else:
                print('----------')
                print(f'{name} 회원을 삭제하지 않았습니다.')
                print('----------')

    def list(self):
        print('----------')
        for k, v in self.members.items():  # members.items(): key, value 추출하기
            print(f'{k}: {v}')
        print('----------')

    @staticmethod
    def exit():
        print('----------')
        print('프로그램을 종료합니다.')
        print('----------')


def main():
    while True:
        this = Contract()
        menu = input('회원정보 추가(a), 검색(f), 수정(u), 삭제(d), 목록(s), 종료(x): ')

        if menu == 'a':
            this.add()
        elif menu == 'f':
            this.find()
        elif menu == 'u':
            this.update()
        elif menu == 'd':
            this.delete()
        elif menu == 's':
            this.list()
        elif menu == 'x':
            exit()
            break


if __name__ == "__main__":
    main()
