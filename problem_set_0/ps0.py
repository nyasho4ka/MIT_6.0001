import numpy


def main():
    x = int(input("Enter number x: "))
    y = int(input("Enter number y: "))
    print("x^y = {0}".format(x**y))
    print("log(x) = {0}".format(numpy.log2(x)))


if __name__ == '__main__':
    main()
