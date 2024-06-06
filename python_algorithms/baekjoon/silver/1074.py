import sys


def remain(row, column):
    if (row % 2 + 1) == 1:
        if (column % 2 + 1) == 1:
            return 1
        else:
            return 2
    else:
        if (column % 2 + 1) == 1:
            return 3
        else:
            return 4


if __name__ == '__main__':
    n, r, c = map(int, sys.stdin.readline().strip().split())
    print(n, r, c)
    a = remain(r, c)
    print(a)
    b = (r / 2 + r % 2 - 1) * (4 * n) + (c / 2 + c % 2 - 1) * 4

    print(a + b)
