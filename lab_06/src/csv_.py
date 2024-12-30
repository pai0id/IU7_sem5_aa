import pandas as pd

def read_distance_matrix_from_csv(file_path):
    df = pd.read_csv(file_path, header=None)
    
    distance_matrix = df.values
    
    return distance_matrix

if __name__ == "__main__":
    file_path = 'mtr.csv'
    distance_matrix = read_distance_matrix_from_csv(file_path)
    print("Считанная матрица расстояний:")
    print(distance_matrix)
