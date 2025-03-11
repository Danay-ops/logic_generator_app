import pandas as pd

def parse_excel(file):
    script = pd.read_excel(file)
    print("Загруженные колонки:", list(script.columns))

    script.drop(columns=['Prompt_name', 'Prompt_text', 'Pattern', 'Setter'], inplace=True)
    script['Unit_name'] = script['Unit_name'].ffill()
    
    # Удаляем строки, где Unit_name содержит "<...>"
    script = script[~script['Unit_name'].astype(str).str.contains(r"<.*>", regex=True)]


    script = script.dropna(subset=['Entity'])
    script = script.dropna(subset=['GoTo'])
    return script.groupby('Unit_name')




# def parse_excel(file):
#     # Загружаем данные, не обращая внимание на названия колонок
#     script = pd.read_excel(file, header=0)

#     # Получаем название первого листа
#     sheet_name = pd.ExcelFile(file).sheet_names[0]

#     # Присваиваем стандартные названия колонкам по их порядку (индексу)
#     expected_columns = ["Unit_name", "Prompt_name", "Prompt_text", "Pattern", "Entity", "GoTo", "Setter", "Remark"]
#     column_mapping = {
#     script.columns[i]: expected_columns[i] 
#     for i in range(min(len(script.columns), len(expected_columns)))  # Ограничиваем по минимуму
# }


#     # Переименовываем колонки
#     script.rename(columns=column_mapping, inplace=True)

#     # Заполняем Unit_name
#     script["Unit_name"] = script["Unit_name"].ffill()

#     # Удаляем строки без Entity или GoTo
#     script = script.dropna(subset=["Entity", "GoTo"])

#     # Группируем по Unit_name
#     grouped = script.groupby("Unit_name")

#     return grouped

def get_sheet_name(file):
    """Возвращает название первого листа в Excel-файле."""
    return pd.ExcelFile(file).sheet_names[0]