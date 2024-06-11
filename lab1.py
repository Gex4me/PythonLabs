import random


# Изменения для 5 лабы

# Изменения для ветки new_feature

def get_list_from_user(n):
    # Запрос элементов списка от пользователя
    print(f"Введите {n} элементов списка, разделенных пробелом, и нажмите enter")
    elements = input().split()
    # Преобразуем строки в числа + проверка
    for i in range(n):
        try:
            elements[i] = int(elements[i])
        except ValueError:
            print(f"Элемент списка с индексом {i} не является числом. Попробуйте еще раз.")
            return get_list_from_user(n)
    return elements


def get_list_auto(n):
    # функция для автоматической генерации списока из n элементов
    return [random.randint(1, 100) for _ in range(n)]


def remove_even_after_max_no_std(lst):
    # Эта функция удалит четные элементы из списка, которые находятся после максимального элемента, не используя стандартные функции
    # Найдем максимальный элемент и его индекс
    max_elem = lst[0]
    max_index = 0
    for i in range(1, len(lst)):
        if lst[i] > max_elem:
            max_elem = lst[i]
            max_index = i
    # Создадим новый список, удалив четные элементы после максимального
    new_lst = []  # Создадим пустой список
    for i in range(len(lst)):  # Перебор всех элементов в списке
        if i <= max_index or (i > max_index and lst[i] % 2 != 0):  # Если элемент до максимального или нечетный после максимального, добавим его в новый список
            new_lst.append(lst[i])
    return new_lst


def remove_even_after_max_std(lst):
    # Эта функция удалит четные элементы из списка, которые находятся после максимального элемента, используя стандартные функции
    max_index = lst.index(max(lst))  # Найдем индекс максимального элемента
    new_lst = lst[:max_index+1] + [x for x in lst[max_index+1:] if x%2]  # Создадим новый список, удалив четные элементы после максимального
    return new_lst

# Тут нужен новый комментарий для 4 Лабы


def main():
    # Вход в программу
    print("Выберите, как вы хотите ввести элементы списка:")
    print("1. Вручную")
    print("2. Автоматически")
    choice = input()
    if choice == "1":
        n = int(input("Введите количество элементов списка: "))
        lst = get_list_from_user(n)
    elif choice == "2":
        n = int(input("Введите количество элементов списка: "))
        lst = get_list_auto(n)
    else:
        print("Неверный выбор. Попробуйте еще раз.")
        return main()
    print("Исходный список: ", lst)
    # Выбор метода удаления четных элементов после max
    print("Выберите метод удаления четных элементов после максимального:")
    print("1. Без стандартных функций")
    print("2. Со стандартными функциями")
    method_choice = input()
    if method_choice == "1":
        # вызов функции удаления четных элементов после max без стандартных функций и вывод результата
        lst_no_std = remove_even_after_max_no_std(lst)
        print("Список после удаления четных чисел после максимального (без использованием стандартных функций): ", lst_no_std)
    elif method_choice == "2":
        # вызов функции удаления четных элементов после max со стандартными функциями и вывод результата
        lst_std = remove_even_after_max_std(lst)
        print("Список после удаления четных чисел после максимального (с использованием стандартных функций): ", lst_std)
    else:
        print("Неверный выбор. Попробуйте еще раз.")
        return main()

    print("Что-то для ветки 4 лабы")

if __name__ == "__main__":
    main()
