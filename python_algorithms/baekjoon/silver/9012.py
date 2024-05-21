
test_case = int(input())

for j in range(test_case):
    vps = input()

    for i in range(len(vps)):
        if vps.find('()') != -1:
            vps = vps.replace('()', '', 1)
        else:
            break

    if len(vps) == 0:
        print('YES')
    else:
        print('NO')

