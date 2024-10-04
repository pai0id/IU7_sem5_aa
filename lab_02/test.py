import utime
import urandom
import uos
from matrix import *

def generate_random_matrix(size):
    return [[urandom.randint(0, 10) for _ in range(size)] for _ in range(size)]

def measure_time(func, A, B):
    start_time = utime.ticks_ms()
    func(A, B)
    end_time = utime.ticks_ms()
    return utime.ticks_diff(end_time, start_time)

def average_execution_time(func, size):
    total_time = 0
    for _ in range(100):
        A = generate_random_matrix(size)
        B = generate_random_matrix(size)
        total_time += measure_time(func, A, B)
    return total_time / 100

def run():
    # file_name = "res.csv"
    
    # if file_name in uos.listdir():
    #     uos.remove(file_name)
    
    # with open(file_name, "w") as file:
        # file.write("Matrix Size,Standard Vinograd Time (ms),Optimized Vinograd Time (ms)\n")
        
    for size in range(1, 101):
        print(f"Проводим тесты для матриц размера {size}x{size}...")

        std = average_execution_time(Multiply, size)
        vinStd = average_execution_time(VinogradMultiply, size)
        vinOpt = average_execution_time(OptimVinogradMultiply, size)
        
        print(f"{std},{vinStd},{vinOpt}\n")
        # print(f"Размер {size}x{size}: стандартная версия {avg_time_standard} мс, оптимизированная версия {avg_time_optimized} мс")
