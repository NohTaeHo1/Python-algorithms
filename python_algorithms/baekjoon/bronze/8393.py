import sys


def sigma(n):
    if n == 1:
        return 1
    return n + sigma(n-1)

def sigma2(n):
    sum = 0
    for i in range(n+1):
        sum += i
    return sum


if __name__ == '__main__':
    user_input = int(sys.stdin.readline().strip())
    print(sigma2(user_input))
