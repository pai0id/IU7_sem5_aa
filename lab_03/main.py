from alg import *
from prettytable import PrettyTable
import plotly as plt
import plotly.io as pio
from random import shuffle

NUM = 8114
if NUM >> 2 % 10 == 0:
    N = NUM % 1000
else:
    N = (NUM >> 2) % 10 * (NUM % 10) + (NUM >> 1) % 10
N += NUM // 8
print(f"Array size: {N}")

testSize = 1000

array = [i for i in range(1, testSize + 1)]

# Поиск в пустом массиве
if SimpleSearch([], 2)[0] != -1:
    print("Error on empty array with SimpleSearch!")
    exit(1)

if BinarySearch([], 2)[0] != -1:
    print("Error on empty array with BinarySearch!")
    exit(1)

print("Empty array test passed!")

# Поиск несуществующего элемента
if SimpleSearch(array, testSize + 1000)[0] != -1:
    print("Error on not existing element with SimpleSearch!")
    exit(1)

if BinarySearch([], testSize + 1000)[0] != -1:
    print("Error on not existing element with BinarySearch!")
    exit(1)

print("Not existing element test passed!")

# Поиск всех элементов массива
arrcp = array.copy()
shuffle(arrcp)
for el in arrcp:
    index, _ = SimpleSearch(array, el)
    if index != array.index(el):
        print(f"Error on element {el} with SimpleSearch!")
        break
    index, _ = BinarySearch(array, el)
    if index != array.index(el):
        print(f"Error on element {el} with BinarySearch!")
        break
else:
    print("All positive tests passed!")

array = [i for i in range(N)]
index = [0 for i in range(N + 1)]
comparisonCounts = [0 for i in range(N + 1)]

for i in range(-1, N):
    index[i + 1], comparisonCounts[i + 1] = SimpleSearch(array, i)

table = PrettyTable()
table.field_names = ["Индекс", "Количество сравнений"]
for i, c in zip(index, comparisonCounts):
    table.add_row((i, c))

print(table)

graph = plt.graph_objs.Figure()
graph.add_bar(x=[str(el) for el in index], y=comparisonCounts, marker_color="#00FFFF")
graph.update_layout(xaxis_title="Индекс элемента", yaxis_title="Количество сравнений")
graph.update_layout(title='Гистограмма полного перебора')
pio.write_image(graph, "./Report/images/LScomp.png", scale=5, width=1076, height=450)
graph.show()

array = [i for i in range(N)]
index = [0 for i in range(N + 1)]
comparisonCounts = [0 for i in range(N + 1)]

for i in range(-1, N):
    index[i + 1], comparisonCounts[i + 1] = BinarySearch(array, i)

table = PrettyTable()
table.field_names = ["Индекс", "Количество сравнений"]
for i, c in zip(index, comparisonCounts):
    table.add_row((i, c))

print(table)

graph = plt.graph_objs.Figure()
graph.add_bar(x=[str(el) for el in index], y=comparisonCounts, marker_color='#DC143C')
graph.update_layout(xaxis_title="Индекс элемента", yaxis_title="Количество сравнений")
graph.update_layout(title='Гистограмма бинарного поиска, отсортированная по индексам')
pio.write_image(graph, "./Report/images/BScomp.png", scale=5, width=1076, height=450)
graph.show()


index, comparisonCounts = zip(*sorted(zip(index, comparisonCounts), key=lambda x: x[1]))
graph = plt.graph_objs.Figure()
graph.add_bar(x=[str(el) for el in index], y=comparisonCounts, marker_color='#32CD32')
graph.update_layout(xaxis_title="Индекс элемента", yaxis_title="Количество сравнений")
graph.update_layout(xaxis={'categoryorder': 'total ascending'})
graph.update_layout(title='Гистограмма бинарного поиска, отсортированная по сравнениям')
pio.write_image(graph, "./Report/images/BScompasc.png", scale=5, width=1076, height=450)
graph.show()

