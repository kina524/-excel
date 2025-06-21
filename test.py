import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path


def analyze_data_excel(path):
    try:
        if not path.exists():
            print("Файл не найден.")
            return None
        try:
            data = pd.read_excel(path)
            df = pd.DataFrame(data)
            return df
        except Exception as ex:
            print(f"Ошибка при чтении файла: {ex}")
            return None

    except Exception as ex:
        print(f"Произошла ошибка: {ex}")
        return None
      
def plot_data(df):
    print("Доступные столбцы:", list(df.columns))
    x = input("Введите название столбца X: ").strip()
    y = input("Введите название столбца Y: ").strip()
    if x not in df.columns:
        print(f"Столбец '{x}' не найден в данных")
        return
    if y not in df.columns:
        print(f"Столбец '{y}' не найден в данных")
        return
    if df[x].isnull().any() or df[y].isnull().any():
        print("Внимание: некоторые значения в выбранных столбцах пусты (NaN)")

    plt.plot(df[x], df[y], marker="o", label=y)
    plt.title(input("Введите название графика: "))
    plt.xlabel(x)
    plt.ylabel(y)
    plt.legend()

    save_graph = input("Хотите сохранить график? (да/нет): ").strip().lower()
    if save_graph == "да":
        filename = input("Введите имя файла для сохранения (например, graph.png): ")
        plt.savefig(filename)
        print(f"График сохранен как {filename}")
    
    plt.show()

def main():
    path = Path(input("Путь: "))
    df = analyze_data_excel(path)
    if df is not None and not df.empty:
        plot_data(df)
    else:
        print("Не удалось загрузить данные для построения графика")

if __name__ == "__main__":
    main()
