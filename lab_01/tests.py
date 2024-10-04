from time import process_time_ns as time_ns
from random import choice, seed
import matplotlib.pyplot as plt 
import tracemalloc
import string
from alg1 import *
from alg2 import *
from alg3 import *

TIMES = 100
MAX_SIZE = 8

def getRndStr(size):
    letters = string.ascii_lowercase
    return "".join(choice(letters) for _ in range(size))

def getLevTimeNs(f, size):    
    res = 0
    seed(1337)

    for _ in range(TIMES):
        s1 = getRndStr(size)
        s2 = getRndStr(size)

        st = time_ns()
        f(s1, s2)
        end = time_ns()

        res += (end - st)

    return res / TIMES

def getLevSize(f, size):    
    res = 0
    seed(1337)

    for _ in range(TIMES):
        s1 = getRndStr(size)
        s2 = getRndStr(size)

        tracemalloc.start()
        f(s1, s2)
        res += tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()

    return res / TIMES

def testAlgsSize(i):
    alg1 = []
    alg2 = []
    alg3 = []
    x = []
    for size in range(2, MAX_SIZE + 1):
        print(f'Size: {size}')
        x.append(size)
        if i == 1:
            alg1.append(getLevSize(reqLev, size))
            alg2.append(getLevSize(memLev, size))
        else:
            alg3.append(getLevSize(dLev, size))

    if i == 1:
        plt.plot(x, alg1, label='alg1', color='blue')
        plt.plot(x, alg2, label='alg2', color='green')
    else:
        plt.plot(x, alg3, label='alg3', color='red')

    print(alg1, alg2, alg3)

    plt.xlabel('Размер строки')
    plt.ylabel('Память')

    plt.grid(True)
    plt.legend()

def testAlgsTime(i):
    alg1 = []
    alg2 = []
    alg3 = []
    x = []
    for size in range(2, MAX_SIZE + 1):
        print(f'Size: {size}')
        x.append(size)
        if i == 1:
            alg1.append(getLevTimeNs(reqLev, size))
            alg2.append(getLevTimeNs(memLev, size))
        else:
            alg3.append(getLevTimeNs(dLev, size))

    if i == 1:
        plt.plot(x, alg1, label='alg1', color='blue')
        plt.plot(x, alg2, label='alg2', color='green')
    else:
        plt.plot(x, alg3, label='alg3', color='red')

    print(alg1, alg2, alg3)

    plt.xlabel('Размер строки')
    plt.ylabel('Время, нс')

    plt.grid(True)
    plt.legend()

if __name__ == "__main__":
    testAlgsTime(1)
    testAlgsSize(1)
    testAlgsTime(2)
    testAlgsSize(2)
    plt.show()
