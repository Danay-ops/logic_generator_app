from jinja2 import Environment, FileSystemLoader
import pandas as pd
from .parser import parse_excel
from .clean_goto import clean_goto_with_if, clean_goto
from .find_statuses import find_status, find_result
from .parser_entities import process_excel

env = Environment(loader=FileSystemLoader('myapp/templates/scripts'))




def generate_script(file, feature_flags):
    """
    Генерирует код на основе переданного Excel-файла.
    """

    grouped_units = parse_excel(file)
    entities_lists = process_excel(file)

    # Загружаем шаблоны
    unit_template = env.get_template("unit_template.j2")
    speaker_template = env.get_template("speaker_template.j2")
    func_status_template = env.get_template("func_status_template.j2")
    conditions_template = env.get_template("logic_template.j2")
    main_template = env.get_template("main_template.j2")
    set_status_template = env.get_template("status_tmp.j2")
    metka = env.get_template("metka.j2")


    # Словарь с доп. блоками
    extra_templates = {}

    if feature_flags.get("include_date_parsing"):
        extra_templates["utterance_date"] = env.get_template("utterance_date.j2").render()

    if feature_flags.get("include_time_parsing"):
        extra_templates["utterance_time"] = env.get_template("utterance_time.j2").render()

    all_units_code = []

    for unit_name, group in grouped_units:
        if pd.isna(unit_name):
            continue

        unit_code_blocks = []
        generated_func_code = ""

        for _, row in group.iterrows():
            got_status = row["Remark"]

            try:
                status_scheme = find_status(got_status)
                result_scheme = find_result(got_status)
            except Exception as e:
                print(f"Ошибка при обработке {unit_name}: {e}")
                continue

            generated_status_code = set_status_template.render(
                unit_name=unit_name, status_sheme=status_scheme, result_scheme=result_scheme
            )
            generated_func_code = func_status_template.render(
                unit_name=unit_name, status_sheme=status_scheme, result_scheme=result_scheme
            )

            entity_name = str(row["Entity"]).strip().split("=")
            cleaned_goto = clean_goto(str(row["GoTo"]).strip())

            test = False
            generated_tags_code = None

            # Логика обработки IF-условий
            if any(word in str(row['GoTo']) for word in ['if', 'IF', 'If', 'Если']):
                try:
                    metka_if = clean_goto_with_if(row['GoTo'])
                    if_part = clean_goto(row['GoTo'].replace('\n', '').replace('\r', '').replace('ELSE', 'else').replace('GOTO', 'goto').replace('else', '').split('goto')[1])
                    else_part = clean_goto(row['GoTo'].replace('\n', '').replace('\r', '').replace('GOTO', 'goto').replace('ELSE', 'else').replace('goto', '').split('else')[-1])
                    generated_tags_code = metka.render(entity=metka_if, goto=if_part)
                    test = True
                except Exception as e:
                    print(f"Ошибка в обработке if в {unit_name}: {e}")


            generated_code = conditions_template.render(
                goto=cleaned_goto,
                entity=entity_name,
                set_status=generated_status_code,
                test=test,
                template1=generated_tags_code,
                unit_name=unit_name,
            )

            unit_code_blocks.append(generated_code)

        speaker_code = speaker_template.render(unit_name=unit_name)
        final_unit_code = unit_template.render(
            unit_name=unit_name,
            generated_code="\n    ".join(unit_code_blocks),
        )

        all_units_code.append(generated_func_code)
        all_units_code.append(speaker_code)
        all_units_code.append(final_unit_code)

    # Формируем финальный скрипт
    final_script = "\n\n".join(all_units_code)
    
    # Передаем extra_templates в main_template
    return main_template.render(final_script=final_script, entities_lists=entities_lists, **extra_templates)


#До добавления  uttarance
"""def generate_script(file, include_date_parsing=False):
    grouped_units = parse_excel(file)

    entities_lists = process_excel(file)

    # Загружаем шаблоны
    unit_template = env.get_template("unit_template.j2")  #есть
    speaker_template = env.get_template("speaker_template.j2")  #есть
    func_status_template = env.get_template("func_status_template.j2")
    conditions_template = env.get_template("logic_template.j2")
    main_template = env.get_template("main_template.j2")
    set_status_template = env.get_template("status_tmp.j2")
    metka = env.get_template("metka.j2")

    utterance_date_template = env.get_template("utterance_date.j2") if include_date_parsing else None

    # Список для хранения сгенерированного кода всех юнитов
    all_units_code = []

    # Проходим по всем юнитам
    for unit_name, group in grouped_units:
        if pd.isna(unit_name):  # Пропускаем пустые значения
            continue

        unit_code_blocks = []
        generated_func_code = ""  # Инициализируем переменную по умолчанию

        for _, row in group.iterrows():
            got_status = row['Remark']
            try:
                status_scheme = find_status(got_status)
                result_scheme = find_result(got_status)

                print(status_scheme, 'status_scheme')
                print(result_scheme, 'result_scheme')
            except Exception as e:
                print(f"Ошибка при обработке {unit_name}: {e}")
                continue

            generated_status_code = set_status_template.render(unit_name=unit_name, status_sheme=status_scheme, result_scheme=result_scheme)
            generated_func_code = func_status_template.render(unit_name=unit_name, status_sheme=status_scheme, result_scheme=result_scheme)

            entity_name = str(row['Entity']).strip().replace('\n', '').replace('\r', '').split('=')
            goto_steps = str(row['GoTo']).strip().replace('\n', '').replace('\r', '').split('->')

            test = False
            generated_tags_code = None

            if any(word in str(row['GoTo']) for word in ['if', 'IF', 'If', 'Если']):
                try:
                    metka_if = clean_goto_with_if(row['GoTo'])
                    if_part = clean_goto(row['GoTo'].replace('\n', '').replace('\r', '').replace('ELSE', 'else').replace('GOTO', 'goto').replace('else', '').split('goto')[1])
                    else_part = clean_goto(row['GoTo'].replace('\n', '').replace('\r', '').replace('GOTO', 'goto').replace('ELSE', 'else').replace('goto', '').split('else')[-1])
                    generated_tags_code = metka.render(entity=metka_if, goto=if_part)
                    test = True
                except Exception as e:
                    print(f"Ошибка в обработке if в {unit_name}: {e}")

            cleaned_goto = clean_goto(str(row['GoTo']).replace('\n', '').replace('\r', ''))

            generated_code = conditions_template.render(goto=cleaned_goto, entity=entity_name, test=test, 
                                        template1 = generated_tags_code, set_status = generated_status_code)
            
            generated_code = conditions_template.render(
            goto=cleaned_goto, 
            entity=entity_name, 
            test=test, 
            template1=generated_tags_code, 
            set_status=generated_status_code
        )

            unit_code_blocks.append(generated_code)

        # Генерируем код спикера
        speaker_code = speaker_template.render(unit_name=unit_name)

        # Генерируем код юнита
        final_unit_code = unit_template.render(
            unit_name=unit_name,
            generated_code="\n    ".join(unit_code_blocks)  # Соединяем все регулярки для этого юнита
        )

        # Генерируем код uttarancce_date
        if include_date_parsing:
            all_units_code.append(utterance_date_template.render())
        
        
        # Добавляем код спикера и юнита в общий список
        all_units_code.append(generated_func_code)
        all_units_code.append(speaker_code)
        all_units_code.append(final_unit_code)


    # Формируем финальный скрипт
    final_script = "\n\n".join(all_units_code)
    return main_template.render(final_script=final_script, entities_lists=entities_lists)


    # all_units_code = []

    # for unit_name, group in grouped_units:
    #     if pd.isna(unit_name):
    #         continue
        
    #     unit_code_blocks = []
    #     for _, row in group.iterrows():
    #         got_status = row['Remark']
    #         try:
    #             status_scheme = find_status(got_status)
    #             result_scheme = find_result(got_status)
    #         except Exception as e:
    #             print(f"Ошибка при обработке {unit_name}: {e}")
    #             continue

    #         generated_func_code = func_status_template.render(
    #             unit_name=unit_name,
    #             status_scheme=status_scheme,
    #             result_scheme=result_scheme
    #         )

    #         entity_name = str(row['Entity']).strip().replace('\n', '').replace('\r', '').split('=')
    #         goto_steps = str(row['GoTo']).strip().replace('\n', '').replace('\r', '').split('->')

    #         test = False
    #         generated_tags_code = None

    #         if any(word in str(row['GoTo']) for word in ['if', 'IF', 'If', 'Если']):
    #             try:
    #                 metka_if = clean_goto_with_if(row['GoTo'])
    #                 if_part = clean_goto(row['GoTo'].split('goto')[1])
    #                 else_part = clean_goto(row['GoTo'].split('else')[-1])
    #                 generated_tags_code = conditions_template.render(entity=metka_if, goto=if_part)
    #                 test = True
    #             except Exception as e:
    #                 print(f"Ошибка в обработке if в {unit_name}: {e}")

    #         cleaned_goto = clean_goto(str(row['GoTo']).replace('\n', '').replace('\r', ''))

    #         generated_code = conditions_template.render(
    #             goto=cleaned_goto, 
    #             entity=entity_name, 
    #             test=test, 
    #             template1=generated_tags_code, 
    #             set_status=generated_func_code
    #         )

    #         unit_code_blocks.append(generated_code)

    #     speaker_code = speaker_template.render(unit_name=unit_name)

    #     final_unit_code = unit_template.render(
    #         unit_name=unit_name,
    #         generated_code="\n    ".join(unit_code_blocks)
    #     )

    #     all_units_code.append(generated_func_code)
    #     all_units_code.append(speaker_code)
    #     all_units_code.append(final_unit_code)

    # final_script = "\n\n".join(all_units_code)
    # return main_template.render(final_script=final_script)
"""





