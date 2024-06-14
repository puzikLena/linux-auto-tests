import subprocess


def find_text(command, text):
    command_result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if not command_result.returncode and text in command_result.stdout:
        return True
    else:
        return False


def get_command_output(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    return result.stdout


def negative_checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    if result.returncode and (text in result.stdout or text in result.stderr):
        return True
    else:
        return False
