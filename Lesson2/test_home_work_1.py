import subprocess

FOLDER_IN = "/home/ubuntu/tst"
FOLDER_OUT = "/home/ubuntu/out"
FOLDER_EXTRACT = "/home/ubuntu/test_folder"


def find_text(command, text):
    command_result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if command_result.returncode:
        return False
    return text in command_result.stdout


def test_step1():
    res1 = find_text(f"cd {FOLDER_IN}; 7z a {FOLDER_OUT}/arx2", "Everything is Ok")
    res2 = find_text(f"cd {FOLDER_OUT}; 7z l arx2.7z", "test.txt")
    assert res1 and res2, "test1 FAIL"


def test_step2():
    res1 = find_text(f"cd {FOLDER_OUT}; 7z x arx2.7z -o{FOLDER_EXTRACT} -y", "Everything is Ok")
    res2 = find_text(f"ls {FOLDER_EXTRACT}", "tst_2")
    res3 = find_text(f"ls {FOLDER_EXTRACT}/tst_2", "test.txt")
    assert res1 and res2 and res3, "test2 FAIL"

