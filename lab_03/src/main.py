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

array = [i for i in range(N)]
index = [0 for i in range(N + 1)]
comparisonCounts = [0 for i in range(N + 1)]

for i in range(-1, N):
    index[i + 1], comparisonCounts[i + 1] = FindElem(array, i)

table = PrettyTable()
table.field_names = ["Индекс", "Количество сравнений"]
for i, c in zip(index, comparisonCounts):
    table.add_row((i, c))

#print(table)

graph = plt.graph_objs.Figure()
graph.add_bar(x=[str(el) for el in index], y=comparisonCounts, marker_color="#00FFFF")
graph.update_layout(xaxis_title="Индекс элемента", yaxis_title="Количество сравнений")
graph.update_layout(title='Гистограмма полного перебора')
pio.write_image(graph, "lin.png", scale=5, width=1076, height=450)
graph.show()

array = [i for i in range(N)]
index = [0 for i in range(N + 1)]
comparisonCounts = [0 for i in range(N + 1)]

for i in range(-1, N):
    index[i + 1], comparisonCounts[i + 1] = BinFindElem(array, i)

table = PrettyTable()
table.field_names = ["Индекс", "Количество сравнений"]
for i, c in zip(index, comparisonCounts):
    table.add_row((i, c))

#print(table)

graph = plt.graph_objs.Figure()
graph.add_bar(x=[str(el) for el in index], y=comparisonCounts, marker_color='#DC143C')
graph.update_layout(xaxis_title="Индекс элемента", yaxis_title="Количество сравнений")
graph.update_layout(title='Гистограмма бинарного поиска, отсортированная по индексам')
pio.write_image(graph, "binid.png", scale=5, width=1076, height=450)
graph.show()


index, comparisonCounts = zip(*sorted(zip(index, comparisonCounts), key=lambda x: x[1]))
graph = plt.graph_objs.Figure()
graph.add_bar(x=[str(el) for el in index], y=comparisonCounts, marker_color='#32CD32')
graph.update_layout(xaxis_title="Индекс элемента", yaxis_title="Количество сравнений")
graph.update_layout(xaxis={'categoryorder': 'total ascending'})
graph.update_layout(title='Гистограмма бинарного поиска, отсортированная по сравнениям')
pio.write_image(graph, "bincmp.png", scale=5, width=1076, height=450)
graph.show()

