import subprocess

FOLDER_OUT = "/home/ubuntu/out"


def uppercase_result(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    return result.stdout.upper()


def test_step1():
    first_command_result = uppercase_result(f"crc32 {FOLDER_OUT}/arx2.7z")
    second_command_result = uppercase_result(f"7z h {FOLDER_OUT}/arx2.7z")
    assert first_command_result in second_command_result, "test1 FAIL"
