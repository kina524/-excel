import logging
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

# Настройка логгирования
logging.basicConfig(
    filename='data_analysis.log',  # Файл для записи логов
    level=logging.INFO,           # Уровень логгирования (INFO или выше)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Формат записи
)

def analyze_data(path):
    # Загружает данные из файла (поддерживаются форматы .xlsx и .csv).
    try:
        if not path.exists():
            logging.error("Файл не найден.")
            print("Файл не найден.")
            return None

        if path.suffix == ".xlsx":
            logging.info(f"Попытка загрузить Excel-файл: {path}")
            data = pd.read_excel(path)
        elif path.suffix == ".csv":
            logging.info(f"Попытка загрузить CSV-файл: {path}")
            data = pd.read_csv(path)
        else:
            logging.error(f"Неподдерживаемый формат файла: {path.suffix}")
            print(f"Поддерживаемые форматы: .xlsx и .csv")
            return None

        df = pd.DataFrame(data)
        logging.info("Данные успешно загружены.")
        return df

    except Exception as ex:
        logging.error(f"Ошибка при чтении файла: {ex}")
        print(f"Ошибка при чтении файла: {ex}")
        return None

def plot_data(df):
    # Строит график на основе выбранных столбцов.
    try:
        logging.info("Начало построения графика.")
        print("Доступные столбцы:", list(df.columns))
        
        x = input("Введите название столбца X: ").strip()
        y = input("Введите название столбца Y: ").strip()

        # Проверка существования столбцов
        if x not in df.columns:
            logging.error(f"Столбец '{x}' не найден в данных.")
            print(f"Столбец '{x}' не найден в данных.")
            return
        if y not in df.columns:
            logging.error(f"Столбец '{y}' не найден в данных.")
            print(f"Столбец '{y}' не найден в данных.")
            return

        # Проверка на наличие пропущенных значений
        if df[x].isnull().any() or df[y].isnull().any():
            logging.warning("Найдены пропущенные значения в выбранных столбцах.")
            print("Внимание: некоторые значения в выбранных столбцах пусты (NaN).")

        # Построение графика
        plt.plot(df[x], df[y], marker="o", label=y)
        plt.title(input("Введите название графика: "))
        plt.xlabel(x)
        plt.ylabel(y)
        plt.legend()
        plt.show()

        # Сохранение графика
        save_graph = input("Хотите сохранить график? (да/нет): ").strip().lower()
        if save_graph == "да":
            filename = input("Введите имя файла для сохранения (например, graph.png): ")
            plt.savefig(filename)
            logging.info(f"График сохранен как {filename}.")
            print(f"График сохранен как {filename}.")
        
        logging.info("График успешно построен.")
    
    except Exception as ex:
        logging.error(f"Ошибка при построении графика: {ex}")
        print(f"Ошибка при построении графика: {ex}")

def main():
    # Основная функция программы.
    try:
        logging.info("Запуск программы.")
        path = Path(input("Введите путь к файлу: "))
        df = analyze_data(path)
        
        if df is not None and not df.empty:
            plot_data(df)
        else:
            logging.error("Не удалось загрузить данные для построения графика.")
            print("Не удалось загрузить данные для построения графика.")
        
        logging.info("Программа завершена.")
    
    except Exception as ex:
        logging.critical(f"Критическая ошибка в основной программе: {ex}")
        print(f"Произошла критическая ошибка: {ex}")

if __name__ == "__main__":
    main()
