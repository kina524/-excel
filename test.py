import logging
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from typing import Optional

# Настройка логирования
logging.basicConfig(
    filename='data_analysis.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Установка данных
class DataLoader:
    formats = ['.xlsx', '.csv']

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.data: Optional[pd.DataFrame] = None

    def load(self) -> bool:
        if not self.file_path.exists():
            logging.error("Файл не найден.")
            print("Ошибка: Файл не найден.")
            return False

        if self.file_path.suffix not in self.formats:
            logging.error(f"Неподдерживаемый формат файла: {self.file_path.suffix}")
            print(f"Поддерживаемые форматы: {', '.join(self.formats)}")
            return False

        try:
            if self.file_path.suffix == ".xlsx":
                self.data = pd.read_excel(self.file_path)
            elif self.file_path.suffix == ".csv":
                self.data = pd.read_csv(self.file_path)

            logging.info("Данные успешно загружены.")
            print("Данные успешно загружены.")
            return True

        except Exception as ex:
            logging.error(f"Ошибка при чтении файла: {ex}")
            print(f"Ошибка при чтении файла: {ex}")
            return False

# Визуализация данных
class DataVisualizer:
    def __init__(self, data: pd.DataFrame):
        self.data = data
    @staticmethod
    def _validate_column(data: pd.DataFrame, column: str) -> bool:
        if column not in data.columns:
            logging.error(f"Столбец '{column}' не найден в данных.")
            print(f"Ошибка: Столбец '{column}' не найден в данных.")
            return False

        if not pd.api.types.is_numeric_dtype(data[column]):
            logging.error(f"Столбец '{column}' должен быть числовым.")
            print(f"Ошибка: Столбец '{column}' должен быть числовым.")
            return False

        return True

    def plot(self):
        print("Доступные столбцы:", list(self.data.columns))
        x = input("Введите название столбца X: ").strip()
        y = input("Введите название столбца Y: ").strip()

        # Проверка столбцов
        if not (self._validate_column(self.data, x) and self._validate_column(self.data, y)):
            return

        # Обработка пропущенных значений
        if self.data[x].isnull().any() or self.data[y].isnull().any():
            logging.warning("Обнаружены пропущенные значения. Удаляю строки.")
            print("Внимание: Обнаружены пропущенные значения. Удаляю строки.")
            self.data = self.data.dropna(subset=[x, y])

        # Построение графика
        plt.plot(self.data[x], self.data[y], marker="o", label=y)
        plt.title(input("Введите название графика: "))
        plt.xlabel(x)
        plt.ylabel(y)
        plt.legend()

        # Сохранение графика
        save_graph = input("Хотите сохранить график? (да/нет): ").strip().lower()
        if save_graph == "да":
            filename = input("Введите имя файла для сохранения (например, graph.png): ").strip()
            if not filename.endswith(('.png', '.jpg', '.jpeg', '.pdf')):
                filename += '.png'  # Добавляем расширение по умолчанию
            plt.savefig(filename)
            logging.info(f"График сохранен как {filename}")
            print(f"График сохранен как {filename}")

        plt.show()

# Основа
class DataAnalysisApp:
    def __init__(self):
        self.data_loader: Optional[DataLoader] = None
        self.data_visualizer: Optional[DataVisualizer] = None

    def run(self):
        try:
            file_path = input("Введите путь к файлу: ").strip()
            if not file_path:
                logging.error("Пользователь ввел пустой путь.")
                print("Ошибка: Путь не может быть пустым.")
                return

            # Загрузка данных
            self.data_loader = DataLoader(file_path)
            if not self.data_loader.load():
                return

            # Визуализация данных
            self.data_visualizer = DataVisualizer(self.data_loader.data)
            self.data_visualizer.plot()

        except Exception as ex:
            logging.error(f"Ошибка: {ex}")
            print(f"Ошибка: {ex}")


if __name__ == "__main__":
    app = DataAnalysisApp()
    app.run()
