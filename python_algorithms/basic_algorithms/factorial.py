def fact(n):
    if n <= 1:
        return 1
    return n*fact(n-1)


def sigma(n):
    if n <= 1:
        return 1

    return n+sigma(n-1)

if __name__ == '__main__':
    a = sigma(5)
    print(a)