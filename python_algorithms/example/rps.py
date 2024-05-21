from example.utils import myRandom


class RPS:

    def __init__(self) -> None:
        print(f'utils.py myRandom() 를 이용하여 가위바위보 객체를 생성합니다')

    def play(self):
        c = myRandom(1, 4)
        p = input('가위, 바위, 보 중 하나를 선택하세요 : ')
#       가위 1 바위 2 보 3
        rps = ['가위', '바위', '보']

        if p == rps[c-1]:
            print(f'본인 : {p}  컴퓨터 : {rps[c-1]}  결과 : 당신은 비겼습니다.')
        elif p == rps[c-2]:
            print(f'본인 : {p}  컴퓨터 : {rps[c - 1]}  결과 : 당신은 졌습니다.')
        elif p == rps[c-3]:
            print(f'본인 : {p}  컴퓨터 : {rps[c - 1]}  결과 : 당신은 이겼습니다.')

def main():
    RPS().play()

if __name__ == '__main__':
    main()