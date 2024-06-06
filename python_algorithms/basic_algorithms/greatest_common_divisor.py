def gcd(a, b):
    i = min(a, b)
    while True:
        if a % i == 0 and b % i == 0:
            return i
        i = i - 1


# a와 b의 최대공약수는 b와 a%b의 최대 공약수와 같다. + 어떤수와 0의 최대 공약수는 자기 자신이다.
def euclid(a, b):
    if b == 0:
        return a
    return euclid(b, a % b)


def pibonacci(n):
    if n <= 1:
        return n
    return pibonacci(n-1)+pibonacci(n-2)


if __name__ == '__main__':
    print(gcd(81, 27))
