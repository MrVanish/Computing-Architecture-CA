from MyInt import *


param = int(input(' 1-Сложение \n 2-Умножение  \n 3-Деление \n Ваш выбор : '))

try:
    if param == 1:
        try:
            a = MyInt(int(input('Первое число : ')), debug=True)
            b = MyInt(int(input('Второе число : ')), debug=True)
        except ValueError:
            print('Введите числу ,а не строку !')
            sys.exit()

        print()
        print(f'{int(a)} -> {a}')
        print(f'{int(b)} -> {b}')
        print()

        try:
            print('Сложение :')
            addition = a.add(b)
            print('Результат :')
            print(addition)
            print(int(addition))
        except OverflowError:
            print('Произошло переполнение !')

        print()

        try:
            print('Вычитание :')
            subtraction = a - b
            print('Результат :')
            print(subtraction)
            print(int(subtraction))
        except OverflowError:
            print('Произошло переполнение !')

    elif param == 2:
        try:
            a = MyInt(int(input('Первое число : ')), debug=True)
            b = MyInt(int(input('Второе число : ')), debug=True)
        except ValueError:
            print('Введите числу ,а не строку !')
            sys.exit()

        print()
        print(f'{int(a)} -> {a}')
        print(f'{int(b)} -> {b}')
        print()

        mult = a * b
        print()
        print("Результат :")
        print(mult)
        print(int(mult))
    elif param == 3:

        try:
            a = MyInt(int(input('Первое число : ')), debug=True)
            b = MyInt(int(input('Второе число : ')), debug=True)
        except ValueError:
            print('Введите числу ,а не строку !')
            sys.exit()

        print()
        print(f'{int(a)} -> {a}')
        print(f'{int(b)} -> {b}')
        print()

        mult = a / b

        print()
        print('Результат :')
        print(f"{mult} -> {int(mult)}")

except Exception as e:
    print(e)