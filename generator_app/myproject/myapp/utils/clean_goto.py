import re
def clean_goto(goto):
    d = {}
    res = []
    # Разбираем speaker
    speaker_items = goto.replace(' ', '').split('->')[-1].split('/')
    
    # Форматируем все элементы, кроме первого
    formatted_speaker = ", ".join(f"{s.strip()}" for s in speaker_items[1:])
    
    # Если есть дополнительные элементы после первого, добавляем их в строку
    if formatted_speaker:
        d['speaker'] = (speaker_items[0], ", ".join(f"'{p.strip()}'" for p in formatted_speaker.replace('<', '').replace('>', '').split('+')))
    else:
        d['speaker'] = (speaker_items[0], None)  # Если второго элемента нет
        
    if len(goto.split('->')) == 1:
        return d
    
    for go in goto.split('->')[:-1]:
        # Формируем строку с кавычками вокруг элементов
        if '/' in go:
            go = go.split('/')[-1]
        promts = ", ".join(f"'{p.strip()}'" for p in go.replace('<', '').replace('>', '').split('+'))
        res.append([promts])  # Оборачиваем строку в список
    
    d['goto'] = res  # Просто присваиваем res, а не оборачиваем в еще один список
    
    return d

def clean_goto_with_if(goto):
    # Регулярка для нахождения всех IF-условий
    pattern = r"(?i)\b(IF|if|Если)\b\s+([\w\s=]+(?:\s*(?:OR|AND|&&|ОR|\|{2})\s*[\w\s=]+)*)"

    # Регулярка для условий вида "ключ = значение"
    condition_pattern = r"\b\w+\s*=\s*\w+\b"

    # Регулярка для поиска логических операторов (OR, AND и их вариаций)
    logical_pattern = r"\b(?:OR|AND|&&|ОR|\|{2})\b"
    main_dic = {}
    all_labels = []  # Плоский список для всех меток и операторов
    # print(goto.split('GOTO'))
    for text in goto.split('GOTO'):
        # Находим все if-условия
        matches = re.findall(pattern, text)



        for match in matches:
            condition_part = match[1]  # Вторая группа содержит метки
            labels = re.findall(condition_pattern, condition_part)  # Ищем все "ключ = значение"
            logical_operators = re.findall(logical_pattern, condition_part)  # Ищем логические операторы
            
            # Разбиваем строку по логическим операторам
            tokens = re.split(logical_pattern, condition_part)

            for i, token in enumerate(tokens):
                token = token.strip()
                if token:
                    all_labels.append(token)  # Добавляем метку
                if i < len(logical_operators):  # Добавляем оператор после метки (кроме последнего)
                    all_labels.append(logical_operators[i])

    return all_labels  # Выводим плоский список всех меток и операторов
