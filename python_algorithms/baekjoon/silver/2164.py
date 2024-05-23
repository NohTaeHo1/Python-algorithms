import sys
from collections import deque


def main():

    n = int(sys.stdin.readline().strip())
    cards = deque(range(1, n+1))

    while len(cards) > 1:
        cards.popleft()
        cards.append(cards.popleft())

    print(cards.pop())


if __name__ == '__main__':
    main()
