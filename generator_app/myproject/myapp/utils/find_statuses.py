import re




# def find_status(status):
#     pattern = r'\b(status(?:_scheme)?)=\s*["\']?([^"\']+?)["\']?(?=\s|$)'
#     matches = re.findall(pattern, status)
#     return {match[0]: match[1] for match in matches}  # Возвращает словарь найденных значений

# def find_result(status):
#     pattern = r'\b((?:call_)?result(?:_scheme)?)=\s*["\']?([^"\']+?)["\']?(?=\s|$)'
#     matches = re.findall(pattern, status)
#     return {match[0]: match[1] for match in matches}  # Возвращает словарь найденных значений


def find_status(status):
    pattern = r'\b(status(?:_scheme)?)=\s*(?:"([^"]+)"|\'([^\']+)\'|(\S+))'
    matches = re.findall(pattern, status)
    return {match[0]: match[1] or match[2] or match[3] for match in matches}  # Берём непустое значение

def find_result(status):
    pattern = r'\b((?:call_)?result(?:_scheme)?)=\s*(?:"([^"]+)"|\'([^\']+)\'|(\S+))'
    matches = re.findall(pattern, status)
    return {match[0]: match[1] or match[2] or match[3] for match in matches} 


