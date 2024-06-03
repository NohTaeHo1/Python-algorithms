import sys


def main():
    n, m = sys.stdin.readline().strip().split()
    n_human = set([])
    m_human = set([])
    for i in range(int(n)):
        j = sys.stdin.readline().strip()
        n_human.add(j)

    for i in range(int(m)):
        j = sys.stdin.readline().strip()
        m_human.add(j)

    a_human = sorted(list(n_human.intersection(m_human)))

    print(len(a_human))

    for i in a_human:
        print(i)


if __name__ == '__main__':
    main()
