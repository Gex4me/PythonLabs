import os
import csv
import chardet


# Класс для работы с файлами в директории
class FileManager:
    def __init__(self, directory_path):
        # Инициализация объекта с путем к директории и получение списка файлов
        self.directory_path = directory_path
        self.files = self._get_files()

    def _get_files(self):
        # Приватный метод для получения списка файлов в директории
        try:
            files_and_dirs = os.listdir(self.directory_path)
            files = [f for f in files_and_dirs if os.path.isfile(os.path.join(self.directory_path, f))]
            return files
        except Exception as e:
            # Обработка ошибок при получении списка файлов
            print(f"Ошибка при получении списка файлов: {e}")
            return []

    def __len__(self):
        # Перегрузка операции получения длины объекта
        return len(self.files)

    def __repr__(self):
        # Перегрузка операции строкового представления объекта
        return f"FileManager({self.directory_path})"

    def __iter__(self):
        # Перегрузка операции итерации
        self._index = 0
        return self

    def __next__(self):
        # Перегрузка операции получения следующего элемента при итерации
        if self._index < len(self.files):
            result = self.files[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration

    def __getitem__(self, index):
        # Перегрузка операции доступа к элементам коллекции по индексу
        return self.files[index]

    @staticmethod
    def detect_file_encoding(file_path):
        # Статический метод для определения кодировки файла
        with open(file_path, 'rb') as file:
            raw_data = file.read()
        result = chardet.detect(raw_data)
        return result['encoding']


# Класс для работы с данными CSV файла
class CSVData:
    def __init__(self, file_path):
        # Инициализация объекта с путем к файлу CSV
        self.file_path = file_path
        self.encoding = FileManager.detect_file_encoding(file_path)  # Определение кодировки файла
        self.data = self._read_data()  # Чтение данных из CSV файла

    def _read_data(self):
        # Приватный метод для чтения данных из CSV файла
        data = []
        try:
            with open(self.file_path, mode='r', encoding=self.encoding) as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=';')
                for row in csv_reader:
                    data.append(row)
        except Exception as e:
            # Обработка ошибок при чтении файла CSV
            print(f"Ошибка при чтении файла CSV: {e}")
        return data

    def __repr__(self):
        # Перегрузка операции строкового представления объекта
        return f"CSVData({self.file_path})"

    def __getitem__(self, index):
        # Перегрузка операции доступа к элементам коллекции по индексу
        return self.data[index]

    def __iter__(self):
        # Перегрузка операции итерации
        self._index = 0
        return self

    def __next__(self):
        # Перегрузка операции получения следующего элемента при итерации
        if self._index < len(self.data):
            result = self.data[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration

    @staticmethod
    def sort_data_by_string_field(data, field_name):
        # Статический метод для сортировки данных по строковому полю
        try:
            return sorted(data, key=lambda x: x[field_name])
        except KeyError:
            # Обработка ошибок, если поле не найдено
            print(f"Поле {field_name} не найдено в данных.")
            return data

    @staticmethod
    def sort_data_by_numeric_field(data, field_name):
        # Статический метод для сортировки данных по числовому полю
        try:
            return sorted(data, key=lambda x: int(x[field_name]), reverse=True)
        except KeyError:
            # Обработка ошибок, если поле не найдено
            print(f"Поле {field_name} не найдено в данных.")
        except ValueError:
            # Обработка ошибок, если поле не является числовым
            print(f"Поле {field_name} не является числовым.")
        return data

    @staticmethod
    def filter_data_by_criteria(data, field_name, criteria):
        # Статический метод для фильтрации данных по критерию
        try:
            return [item for item in data if int(item[field_name]) > criteria]
        except KeyError:
            # Обработка ошибок, если поле не найдено
            print(f"Поле {field_name} не найдено в данных.")
        except ValueError:
            # Обработка ошибок, если поле не является числовым
            print(f"Поле {field_name} не является числовым.")
        return data

    def save_data(self, data):
        # Метод для сохранения данных в файл CSV
        try:
            if not data:
                print("Нет данных для сохранения.")
                return

            fieldnames = data[0].keys()
            with open(self.file_path, mode='w', encoding=self.encoding, newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
                writer.writeheader()
                writer.writerows(data)
        except Exception as e:
            # Обработка ошибок при сохранении файла CSV
            print(f"Ошибка при сохранении файла CSV: {e}")

    def __setattr__(self, key, value):
        # Перегрузка операции установки атрибутов объекта
        # Разрешение только для определенных атрибутов
        if key in ['file_path', 'encoding', 'data']:
            self.__dict__[key] = value
        else:
            raise AttributeError(f"Attribute '{key}' is not allowed to be set")


# Класс для обработки данных
class DataProcessor:
    def __init__(self, csv_data):
        # Инициализация объекта с данными CSV
        self.csv_data = csv_data

    def process_data(self, option, criteria=None):
        # Метод для обработки данных в зависимости от выбора
        if option == '1':
            # Сортировка данных по количеству лайков
            return CSVData.sort_data_by_numeric_field(self.csv_data.data, 'Количество лайков')
        elif option == '2':
            # Сортировка данных по нику автора
            return CSVData.sort_data_by_string_field(self.csv_data.data, 'Ник автора')
        elif option == '3':
            # Фильтрация данных по количеству лайков с заданным критерием
            return CSVData.filter_data_by_criteria(self.csv_data.data, 'Количество лайков', criteria)
        else:
            print("Некорректный выбор.")
            return self.csv_data.data

    @staticmethod
    def data_generator(data):
        # Статический метод для создания генератора данных
        for item in data:
            yield item


def main():
    directory_path = input("Введите путь к директории: ")
    file_manager = FileManager(directory_path)

    print(f"Количество файлов в директории: {len(file_manager)}")

    if len(file_manager) == 0:
        print("В данной директории нет файлов.")
        return

    print("Файлы в директории:")
    for i, file in enumerate(file_manager):
        print(f"{i + 1}. {file}")

    try:
        file_index = int(input(f"Выберите файл (1-{len(file_manager)}): ")) - 1
        if file_index < 0 or file_index >= len(file_manager):
            print("Неверный выбор файла.")
            return
    except ValueError:
        print("Неверный ввод.")
        return

    file_path = os.path.join(directory_path, file_manager[file_index])
    csv_data = CSVData(file_path)
    processor = DataProcessor(csv_data)

    print("\nВыберите тип обработки данных:")
    print("1. Сортировка по количеству лайков")
    print("2. Сортировка по нику автора")
    print("3. Фильтр по количеству лайков")

    choice = input("Введите номер обработки: ")

    if choice == '3':
        criteria_value = int(input("Введите количество лайков для фильтрации: "))
        processed_data = processor.process_data(choice, criteria_value)
    else:
        processed_data = processor.process_data(choice)

    for item in processor.data_generator(processed_data):
        print(item)

    save_changes = input("Хотите сохранить обработанные данные обратно в файл? (yes/no): ").lower()
    if save_changes == 'yes':
        csv_data.save_data(processed_data)
        print("Изменения успешно сохранены.")
    else:
        print("Изменения не сохранены.")


if __name__ == "__main__":
    main()
