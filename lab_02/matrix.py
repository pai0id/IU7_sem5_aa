def Multiply(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    if cols_A != rows_B:
        raise ValueError("Cannot multiply matrices: incompatible dimensions")

    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]

    return result

def VinogradMultiply(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    if cols_A != rows_B:
        raise ValueError("Невозможно перемножить матрицы: некорректные размеры")

    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    mulH = [0] * rows_A
    for i in range(rows_A):
        for j in range(0, cols_A // 2):
            mulH[i] = mulH[i] + A[i][2 * j] * A[i][2 * j + 1]

    mulV = [0] * cols_B
    for i in range(cols_B):
        for j in range(0, rows_B // 2):
            mulV[i] = mulV[i] + B[2 * j][i] * B[2 * j + 1][i]

    for i in range(rows_A):
        for j in range(cols_B):
            result[i][j] = -mulH[i] - mulV[j]
            for k in range(0, cols_A // 2):
                result[i][j] = result[i][j] + (A[i][2 * k] + B[2 * k + 1][j]) * (A[i][2 * k + 1] + B[2 * k][j])

    if cols_A % 2 == 1:
        for i in range(rows_A):
            for j in range(cols_B):
                result[i][j] = result[i][j] + A[i][cols_A - 1] * B[cols_A - 1][j]

    return result

# двоичный сдвиг вместо умножения на 2; 
# введение декремента при вычислении вспомогательных массивов; 
# вынос начальной итерации из каждого внешнего цикла;
def OptimVinogradMultiply(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    if cols_A != rows_B:
        raise ValueError("Невозможно перемножить матрицы: некорректные размеры")

    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    mulH = [0] * rows_A
    for i in range(rows_A):
        j = cols_A >> 1
        while j > 0:
            j -= 1
            mulH[i] += A[i][j << 1] * A[i][(j << 1) + 1]

    mulV = [0] * cols_B
    for i in range(cols_B):
        j = rows_B >> 1
        while j > 0:
            j -= 1
            mulV[i] += B[j << 1][i] * B[(j << 1) + 1][i]

    for i in range(rows_A):
        for j in range(cols_B):
            temp = -mulH[i] - mulV[j]
            k = cols_A >> 1
            while k > 0:
                k -= 1
                temp += (A[i][k << 1] + B[(k << 1) + 1][j]) * (A[i][(k << 1) + 1] + B[k << 1][j])
            result[i][j] = temp

    if cols_A % 2 == 1:
        last_col = cols_A - 1
        for i in range(rows_A):
            for j in range(cols_B):
                result[i][j] += A[i][last_col] * B[last_col][j]

    return result

def InputMatrix(rows, cols):
    matrix = []
    print(f"Enter the elements of the {rows}x{cols} matrix row by row:")
    for i in range(rows):
        row = []
        for j in range(cols):
            element = int(input(f"Element [{i+1}][{j+1}]: "))
            row.append(element)
        matrix.append(row)
    return matrix


