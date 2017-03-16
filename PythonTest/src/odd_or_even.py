#  http://qiita.com/Usek/items/fba0991e224a1cdea274

def odd_or_even():
    print("")
    for i in range(1,6):
        if i % 2 != 0:
            print("{0} is odd".format(i))
        else:
            print("{0} is even".format(i))

if __name__ == "__main__":
    odd_or_even()
