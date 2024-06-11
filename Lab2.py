import numpy as np

# Текст с изменениями для 5 лабы

def generate_matrix(n, m):
    """
    Генерирует прямоугольную матрицу размером n x m с произвольными целыми числами.
    n: Количество строк в матрице.
    m: Количество столбцов в матрице.
    """
    return np.random.randint(10, size=(n, m))

def process_matrix(matrix, l):
    """
    Обрабатывает элементы прямоугольной матрицы matrix, имеющей N строк и M столбцов.
    Просуммировывает элементы каждой строки матрицы с соответствующими элементами L-й строки.
    matrix: Исходная матрица.
    l: Номер строки, с которой будут происходить суммирования.
    """
    matrix_copy = np.copy(matrix)
    for i in range(matrix.shape[0]):
        if i == l:
            continue
        matrix_copy[i, :] += matrix[l, :]
    return matrix_copy

def save_to_file(filename, matrix):
    """
    Сохраняет матрицу в файл с указанным именем.
    """
    np.savetxt(filename, matrix, fmt='%d')

def main():
    # Генерируем матрицу размером 5 x 4
    matrix = generate_matrix(5, 4)
    print("Исходная матрица:")
    print(matrix)

    # Обрабатываем матрицу, просуммировав элементы каждой строки с соответствующими элементами 3-й строки
    processed_matrix = process_matrix(matrix, 3)
    print("Обработанная матрица:")
    print(processed_matrix)

    # Сохраняем исходную и обработанную матрицы в файлы
    save_to_file("input_matrix.txt", matrix)
    save_to_file("output_matrix.txt", processed_matrix)

if __name__ == "__main__":
    main()
