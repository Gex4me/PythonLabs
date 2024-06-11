import os
import csv
import chardet


def count_files_in_directory(directory_path):
    """
    Возвращает количество файлов в указанной директории и список файлов в этой директории.
    """
    try:
        files_and_dirs = os.listdir(directory_path)
        files = [f for f in files_and_dirs if os.path.isfile(os.path.join(directory_path, f))]
        return len(files), files
    except Exception as e:
        print(f"Ошибка при подсчете файлов в директории: {e}")
        return 0, []


def detect_file_encoding(file_path):
    """
    Определение кодировки файла
    """
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    result = chardet.detect(raw_data)
    return result['encoding']


def read_data_from_csv(file_path, encoding):
    """
    Считывание данных из файла CSV и возврат их в виде списка словарей.
    """
    data = []
    try:
        with open(file_path, mode='r', encoding=encoding) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=';')
            for row in csv_reader:
                data.append(row)
    except Exception as e:
        print(f"Ошибка при чтении файла CSV: {e}")
    return data


def sort_data_by_string_field(data, field_name):
    """
    Сортировка данных по строковому полю
    """
    try:
        return sorted(data, key=lambda x: x[field_name])
    except KeyError:
        print(f"Поле {field_name} не найдено в данных.")
        return data


def sort_data_by_numeric_field(data, field_name):
    """
    Сортировка данных по численному полю
    """
    try:
        return sorted(data, key=lambda x: int(x[field_name]), reverse=True)
    except KeyError:
        print(f"Поле {field_name} не найдено в данных.")
    except ValueError:
        print(f"Поле {field_name} не является числовым.")
    return data


def filter_data_by_criteria(data, field_name, criteria):
    try:
        return [item for item in data if int(item[field_name]) > criteria]
    except KeyError:
        print(f"Поле {field_name} не найдено в данных.")
    except ValueError:
        print(f"Поле {field_name} не является числовым.")
    return data


def save_data_to_csv(file_path, data, encoding):
    try:
        if not data:
            print("Нет данных для сохранения.")
            return

        fieldnames = data[0].keys()
        with open(file_path, mode='w', encoding=encoding, newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            writer.writerows(data)
    except Exception as e:
        print(f"Ошибка при сохранении файла CSV: {e}")


def main():
    directory_path = input("Введите путь к директории: ")

    # Подсчет файлов в директории
    file_count, files = count_files_in_directory(directory_path)
    print(f"Количество файлов в директории: {file_count}")

    if file_count == 0:
        print("В данной директории нет файлов.")
        return

    print("Файлы в директории:")
    for i, file in enumerate(files):
        print(f"{i + 1}. {file}")

    try:
        file_index = int(input(f"Выберите файл (1-{file_count}): ")) - 1
        if file_index < 0 or file_index >= file_count:
            print("Неверный выбор файла.")
            return
    except ValueError:
        print("Неверный ввод.")
        return

    file_path = os.path.join(directory_path, files[file_index])

    # Определение кодировки файла
    encoding = detect_file_encoding(file_path)
    print(f"Определенная кодировка файла: {encoding}")

    # Чтение данных из выбранного CSV файла
    data = read_data_from_csv(file_path, encoding)

    if not data:
        print("Не удалось прочитать данные из файла.")
        return

    # Выбор типа сортировки
    print("\nВыберите тип сортировки:")
    print("1. Сортировка по количеству лайков")
    print("2. Сортировка по нику автора")
    print("3. Фильтр по количеству лайков")

    choice = input("Введите номер сортировки: ")

    if choice == '1':
        sorted_data = sort_data_by_numeric_field(data, 'Количество лайков')
        print("\nОтсортированно по Количеству лайков:")
    elif choice == '2':
        sorted_data = sort_data_by_string_field(data, 'Ник автора')
        print("\nОтсортированно по Нику автора:")
    elif choice == '3':
        criteria_value = int(input("Введите количество лайков для фильтрации: "))
        sorted_data = filter_data_by_criteria(data, 'Количество лайков', criteria_value)
        print(f"\nОтфильтрованно по критерию лайков > {criteria_value}")
    else:
        print("Некорректный выбор.")
        return

    for item in sorted_data:
        print(item)

    # Предложение сохранить изменения
    save_changes = input("Хотите сохранить отсортированные данные обратно в файл? (yes/no): ").lower()
    if save_changes == 'yes':
        save_data_to_csv(file_path, sorted_data, encoding)
        print("Изменения успешно сохранены.")
    else:
        print("Изменения не сохранены.")


if __name__ == "__main__":
    main()

