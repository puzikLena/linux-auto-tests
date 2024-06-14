import pytest
from checks import find_text, get_command_output
import random, string
import yaml
from datetime import datetime

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folders():
    return find_text(
        f"mkdir {data['FOLDER_IN']} {data['FOLDER_OUT']} {data['FOLDER_EXTRACT']} {data['FOLDER_EXTRACT2']}", "")


@pytest.fixture()
def clear_folders():
    return find_text(
        f"rm -rf {data['FOLDER_IN']}/* {data['FOLDER_OUT']}/* {data['FOLDER_EXTRACT']}/* {data['FOLDER_EXTRACT2']}/*",
        "")


@pytest.fixture()
def make_files():
    files_list = []
    for i in range(data['count']):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if find_text(f"cd {data['FOLDER_IN']}; dd if=/dev/urandom of={filename} bs={data['size']} count=1 iflag=fullblock", ""):
            files_list.append(filename)
    return files_list


@pytest.fixture()
def make_subfolder():
    test_filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfolder_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not find_text(f"cd {data['FOLDER_IN']}; mkdir {subfolder_name}", ""):
        return None, None
    if not find_text(
            f"cd {data['FOLDER_IN']}/{subfolder_name}; dd if=/dev/urandom of={test_filename} bs={data['size']} count=1 iflag=fullblock",
            ""):
        return subfolder_name, None
    else:
        return subfolder_name, test_filename


@pytest.fixture(autouse=True)
def print_time():
    print(f'Start: {datetime.now().strftime("%H:%M:%S.%f")}')
    yield
    print(f'Stop: {datetime.now().strftime("%H:%M:%S.%f")}')


@pytest.fixture()
def make_bad_file():
    if find_text(f"cd {data['FOLDER_IN']}; 7z a {data['FOLDER_OUT']}/arx2_bad", "") and \
            find_text(f"truncate -s 1 {data['FOLDER_OUT']}/arx2_bad.7z", ""):
        return 'arx2_bad'
    return None


@pytest.fixture(autouse=True)
def write_stat():
    yield
    with open('stat.txt', 'a', encoding='utf-8') as file:
        file.write(f"{datetime.now().strftime('%H:%M:%S.%f')},   total files: {data['count']},  size: {data['size']},   "
                   f"proc load: {get_command_output('cat /proc/loadavg')}")
