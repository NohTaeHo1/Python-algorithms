import sys

test_case = int(sys.stdin.readline().strip())
numbers = set()


def add(n):
    numbers.add(n)


def remove(n):
    if n in numbers:
        numbers.remove(n)


def check(n):
    if n in numbers:
        print('1')
    else:
        print('0')


def toggle(n):
    if n in numbers:
        numbers.remove(n)
    else:
        numbers.add(n)


def all():
    numbers.clear()
    for i in range(20):
        numbers.add(i + 1)


def empty():
    numbers.clear()


def main():
    for i in range(test_case):
        m = sys.stdin.readline().strip()
        if m != 'all' and m != 'empty':
            m, n = m.split()
            n = int(n)

        if m == 'add':
            add(n)
        elif m == 'remove':
            remove(n)
        elif m == 'check':
            check(n)
        elif m == 'toggle':
            toggle(n)
        elif m == 'all':
            all()
        elif m == 'empty':
            empty()


if __name__ == '__main__':
    main()
