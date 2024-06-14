# Доработать функцию из предыдущего задания таким образом, чтобы у неё появился дополнительный режим работы,
# в котором вывод разбивается на слова с удалением всех знаков пунктуации
# (их можно взять из списка string.punctuation модуля string). В этом режиме должно проверяться наличие слова в выводе.
import re
import string
import subprocess


def find_text(command, text):
    command_result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if command_result.returncode:
        return False
    return text in command_result.stdout


def split_text_by_words(value):
    for char in value:
        if char in string.punctuation:
            value = value.replace(char, ' ')
    split_data = re.split('[ \\n]', value)
    result = []
    for element in split_data:
        if element != '':
            result.append(element)
    return result
