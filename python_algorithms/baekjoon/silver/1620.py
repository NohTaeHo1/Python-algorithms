import sys


def main():
    n, m = map(int, sys.stdin.readline().split())
    poketmon = {}
    for i in range(n):
        input = sys.stdin.readline().strip()
        poketmon[f'{i+1}'] = input
        poketmon[input] = i+1

    for i in range(m):
        print(f'{poketmon[sys.stdin.readline().strip()]}')

if __name__ == '__main__':
    main()