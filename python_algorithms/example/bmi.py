from example.utils import Member, myRandom


class BMI():

    def __init__(self) -> None:
        # BMI = 체중/키제곱
        print('''utils.py / Members(), myRandom() 를 이용하여 BMI 지수를 구하는 계산기를 작성합니다.''')

    def information(self):
        this = Member()
        this.name = input("당신의 이름은? ")
        this.height = myRandom(150, 200)
        this.weight = myRandom(40, 100)
        pre_bmi = (this.weight / ((this.height/100) ** 2))
        bmi = '비만' if pre_bmi > 25 else '과체중' if pre_bmi > 23 else '정상' if pre_bmi > 18.5 else '저체중'
        # ~18.5 저체중 ~23 정상 ~ 25 과체중 ~ 비만
        print(f'이름: {this.name}  BMI수치: {(this.weight / ((this.height/100) ** 2)):.2f}  BMI: {bmi}')

def main():
    BMI().information()

if __name__ == '__main__':
    main()
