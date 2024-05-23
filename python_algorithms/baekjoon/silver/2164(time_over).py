import sys


def main():

    cards = list(range(1, int(sys.stdin.readline().strip())))
    for i in range(len(cards)):
        cards.append(i + 1)

    while len(cards) != 1:
        remove(cards)
        two_card_move(cards)

    print(cards.pop(0))


def remove(cards):
    cards.pop(0)


def two_card_move(cards):
    cards.append(cards.pop(0))


if __name__ == '__main__':
    main()
