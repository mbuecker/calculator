from colorama import Fore
from colorama import Style
from calculator import calc

p = calc.calculator("")

testformeln = [
    [3.141592653589793, "pi"],
    [4, "sqrt(4*4)"],
    [5, "(2+8)/2)"],
    [5, "5"],
    [2, "10/(2+3)"],
    [2, "(2+8)/(2+3)"],
    [3, "(2*(1+2))/2"],
    [16, "4*4"],
    [0, "5/0"],
    [8, "4+4"],
    [20, "4+4*+4"],
    [20, "4*4+4"],
    [12, "4+4+4"],
    [20, "20/10*10"],
    [-8, "20/10-10"],
    [25, "5/*4+5"],
    [25, "a=5*4+5"],
    [50, "b=a*2"],
    [25, "a"]
]


def test_parser():
    for formel in testformeln:
        p.setformel(formel[1])
        result = p.parse()
        print(formel[0], "=", formel[1], "=", result, end='')

        if result == formel[0]:
            print(f"{Fore.GREEN} ==> OK{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED} ====> failed{Style.RESET_ALL}")

        if p.errorFlag:
            print(f"{Fore.RED}", end='')
            p.printerror()
            print(f"{Style.RESET_ALL}", end='')


if __name__ == '__main__':

    while True:
        line = input("calculate: ")
        if line == "quit":
            break
        elif line == "":
            print( "type ? or help")
            continue
        elif line == "test":
            test_parser()
            continue

        p.setformel(line)
        erg = p.parse()

        if p.errorFlag:
            print(f"{Fore.RED}", end='')
            p.printerror()
            print(f"{Style.RESET_ALL}", end='')
        else:
            print(erg)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
