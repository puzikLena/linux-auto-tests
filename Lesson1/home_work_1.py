# Написать функцию на Python, которой передаются в качестве параметров команда и текст.
# Функция должна возвращать True, если команда успешно выполнена и текст найден в её выводе и False в противном случае.
# Передаваться должна только одна строка, разбиение вывода использовать не нужно.

import subprocess


def find_text(command, text):
    command_result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if command_result.returncode:
        return False
    return text in command_result.stdout
