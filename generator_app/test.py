import re

def find_status(status, name):
    pattern = r'\b(name(?:_scheme)?)=\s*(?:"([^"]+)"|\'([^\']+)\'|(\S+))'
    matches = re.findall(pattern, status)
    return {match[0]: match[1] or match[2] or match[3] for match in matches}  # Берём непустое значение

def find_result(status):
    pattern = r'\b((?:call_)?result(?:_scheme)?)=\s*(?:"([^"]+)"|\'([^\']+)\'|(\S+))'
    matches = re.findall(pattern, status)
    return {match[0]: match[1] or match[2] or match[3] for match in matches} 



def find_key_value_pairs(text, key):
    pattern = rf'\b{key}=\s*(?:"([^"]+)"|\'([^\']+)\'|([^\s]+(?:\s+[^\s=]+)*))'
    matches = re.findall(pattern, text)
    return {key: match[0] or match[1] or match[2].strip() for match in matches}

name = ['to_operator', 'result']

a = find_key_value_pairs(text="endpoint_mark=""Автоответчик"" call_result=""Обрыв соединения""person_type=""Третье лицо""", key=name)
print(a)
text='SET result=Сброс звонка только на второй счетчик:SET result=Перевод на оператораSET to_operator=Допвопросы'
b = [find_key_value_pairs(text, key) for key in name]

print(b)

c = find_result(text)
print(c)

