
def main():
    vowels = ['a', 'e', 'i', 'o', 'u']

    flag = True

    while(flag):
        test_case = input()
        index = []
        if not any(i in test_case for i in vowels):
            print(f'<{test_case}> is not acceptable')
            continue

        index = [test_case.find(i) for i in test_case if i in vowels]

        for i in range(len(test_case)):
            m = test_case[i]
            if m in vowels:
                if test_case[i+1] in vowels:
                    if test_case[i+2] in vowels:
                        print(f'<{test_case}> is not acceptable')
                        flag = False

            else:
                if not (test_case[i+1] in vowels):
                    if not (test_case[i+2] in vowels):
                        print(f'<{test_case}> is not acceptable')
                        flag = False

        for i in test_case:
            if test_case[i] == test_case[i+1]:
                if not (test_case[i] == 'w' or test_case[i]=='o'):
                    print(f'<{test_case}> is not acceptable')
                    flag = False

        print(f'<{test_case}> is not acceptable')



