test_case = int(input())

for i in range(test_case):
    case = int(input())
    if case == 1 or case == 2:
        print(f'Pairs for {case}:')
        continue
    a = (case//2 if case%2 !=0 else case//2 -1)

    pair = []
    for j in range(a):
        pair.append(f'{j+1} {case-(j+1)}')

    print(f'Pairs for {case}: ' + ', '.join(pair))
