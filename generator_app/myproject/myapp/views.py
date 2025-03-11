import os
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from jinja2 import Template
from .utils.parser_entities import process_excel
from .utils.generator import generate_script
import json
import subprocess
from django.http import JsonResponse

def editor_view(request):
    """ Отображает страницу с Monaco Editor """
    return render(request, "editor.html")




def check_python_syntax(script_code):
    """
    Проверяет код Python на ошибки с помощью pylint.
    """
    try:
        # Запускаем pylint с нужными параметрами
        result = subprocess.run(
            ["pylint", "--from-stdin", "--output-format=json"],
            input=script_code,
            text=True,
            capture_output=True
        )

        errors = []
        if result.stdout:
            pylint_errors = json.loads(result.stdout)
            for err in pylint_errors:
                errors.append({
                    "lineNumber": err.get("line", 1),
                    "column": err.get("column", 1),
                    "message": f"{err.get('message')} ({err.get('symbol')})"
                })
        return errors
    except Exception as e:
        return [{"lineNumber": 1, "column": 1, "message": f"Ошибка анализа: {str(e)}"}]

def process_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        excel_file = request.FILES['file']
        # include_date_parsing = request.POST.get('include_date_parsing') == 'true'  # Читаем флаг
        
        #Собираем флаги
        feature_flags = {
            "include_date_parsing": request.POST.get('include_date_parsing') == 'true',
            "include_time_parsing": request.POST.get('include_time_parsing') == 'true',
            "include_extra_feature": request.POST.get('include_extra_feature') == 'true',
        }


        # Генерация кода (твой метод)
        script_code = generate_script(excel_file, feature_flags)

        # Проверяем код на ошибки
        errors = check_python_syntax(script_code)

        return JsonResponse({"output": script_code, "errors": errors})

    return JsonResponse({"error": "Файл не загружен"}, status=400)







# def check_python_syntax(script_code):
#     """
#     Проверяет код Python на ошибки с помощью pyflakes и возвращает список ошибок.
#     """
#     try:
#         result = subprocess.run(
#             ["python", "-m", "pyflakes", "-"],
#             input=script_code,
#             text=True,
#             capture_output=True
#         )

#         errors = []
#         if result.stderr:
#             for line in result.stderr.strip().split("\n"):
#                 parts = line.split(":")
#                 if len(parts) >= 3:
#                     errors.append({
#                         "lineNumber": int(parts[1]),
#                         "column": 1,
#                         "message": parts[2].strip()
#                     })
#         return errors
#     except Exception as e:
#         return [{"lineNumber": 1, "column": 1, "message": f"Ошибка анализа: {str(e)}"}]

# def process_file(request):
#     if request.method == 'POST' and request.FILES.get('file'):
#         excel_file = request.FILES['file']

#         # Функция генерации кода
#         script_code = generate_script(excel_file)

#         # Проверяем код на ошибки
#         errors = check_python_syntax(script_code)

#         return JsonResponse({"output": script_code, "errors": errors})

#     return JsonResponse({"error": "Файл не загружен"}, status=400)



# def process_file(request):
#     if request.method == "POST" and request.FILES.get("file"):
#         excel_file = request.FILES["file"]
#         file_path = f"temp_{excel_file.name}"

#         # Сохраняем временный файл
#         with open(file_path, "wb") as f:
#             for chunk in excel_file.chunks():
#                 f.write(chunk)

#         # Обрабатываем файл
#         try:
#             output = process_excel(file_path)
#         finally:
#             os.remove(file_path)  # Удаляем временный файл

#         return JsonResponse({"output": output})

#     return JsonResponse({"error": "Файл не загружен"}, status=400)