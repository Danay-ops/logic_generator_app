from openpyxl import load_workbook
from .parser import get_sheet_name

def process_excel(file_path):
    """Обрабатывает Excel-файл и возвращает результат в виде строки"""
    sheet_name = get_sheet_name(file_path)  # Получаем название листа
    book = load_workbook(filename=file_path)
    sheet = book[sheet_name]

    result = []  # Список для хранения вывода

    def ver_2(sheet):
        start = 2
        end = 773
        for item in range(start, end):
            reg = (sheet['E' + str(item)].value)
            reg_a = (sheet['A' + str(item)].value)
            if reg_a:
                list_word = []
                if item > start + 1 and len(list_word) == 0:
                    result.append('    "interruption"')
                    result.append(']')
                    if reg_a != 'hello_unit':
                        interruption(sheet, start_for_interruption, item)
                if reg_a != 'hangup_unit':
                    start_for_interruption = item
                    result.append(f'\n{reg_a}_entities_list = [')
            if reg and reg not in ['<DEFAULT>', '<NULL>']:
                reg_list = reg.split()
                for word in reg_list:
                    if word not in ['or', 'OR', '&&', '<NULL>']:
                        word_result_list = word.split('=')
                        word_result = word_result_list[0]
                        if word_result not in list_word:
                            list_word.append(word_result)
                            result.append(f'    "{word_result}",')

    def interruption(sheet, start, end):
        for item in range(start, end):
            reg = (sheet['E' + str(item)].value)
            reg_A = (sheet['A' + str(item)].value)
            if reg_A:
                list_word_interruption = []
                result.append(f'\n{reg_A}_interruption_entities_list = [')
            if reg and reg not in ['<DEFAULT>', '<NULL>']:
                reg_list = reg.split()
                for word in reg_list:
                    if word not in ['or', 'OR', '&&', '<NULL>']:
                        word_result_list = word.split('=')
                        word_result = word_result_list[0]
                        if word_result not in list_word_interruption:
                            list_word_interruption.append(word_result)
                            if word_result not in ['confirm', 'hello_confirm']:
                                result.append(f'    "{word_result}",')

        result.append('    "interruption"')
        result.append(']')

    ver_2(sheet)
    return "\n".join(result)  # Возвращаем строку с результатом
