import random
import string
from datetime import datetime

import pytest
import yaml

from checks import getout
from ssh_checks import ssh_checkout

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def create_folders():
    return ssh_checkout(data["host"], data["user"], data["passwd"],
                        f"mkdir {data['FOLDER_IN']} {data['FOLDER_OUT']} {data['FOLDER_EXTRACT']} {data['FOLDER_EXTRACT2']}",
                        "")


@pytest.fixture()
def clear_folders():
    return ssh_checkout(data["host"], data["user"], data["passwd"],
                        f"rm -rf {data['FOLDER_IN']}/* {data['FOLDER_OUT']}/* {data['FOLDER_EXTRACT']}/* "
                        f"{data['FOLDER_EXTRACT2']}/*", "")


@pytest.fixture()
def create_files():
    list_of_files = []
    for i in range(data['count']):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout(data["host"], data["user"], data["passwd"],
                        f"cd {data['FOLDER_IN']}; dd if=/dev/urandom of={filename} bs={data['size']} count=1 iflag=fullblock",
                        ""):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def create_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not ssh_checkout(data["host"], data["user"], data["passwd"], f"cd {data['FOLDER_IN']}; mkdir {subfoldername}",
                        ""):
        return None, None
    if not ssh_checkout(data["host"], data["user"], data["passwd"], f"cd {data['FOLDER_IN']}/{subfoldername}; "
                                                                    f"dd if=/dev/urandom of={testfilename} bs={data['size']} count=1 iflag=fullblock",
                        ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture(autouse=True)
def print_execution_time():
    print(f'Start: {datetime.now().strftime("%H:%M:%S.%f")}')
    yield
    print(f'Stop: {datetime.now().strftime("%H:%M:%S.%f")}')


@pytest.fixture()
def create_bad_file():
    if ssh_checkout(data["host"], data["user"], data["passwd"],
                    f"cd {data['FOLDER_IN']}; 7z a {data['FOLDER_OUT']}/arx2_bad", "") and \
            ssh_checkout(
                data["host"],
                data["user"],
                data["passwd"],
                f"truncate -s 1 {data['FOLDER_OUT']}/arx2_bad.7z",
                ""
            ):
        return 'arx2_bad'
    return None


@pytest.fixture(autouse=True)
def write_stat():
    yield
    with open('stat.txt', 'a', encoding='utf-8') as file:
        file.write(
            f"{datetime.now().strftime('%H:%M:%S.%f')},   total files: {data['count']},  size: {data['size']},   "
            f"proc load: {getout('cat /proc/loadavg')}")


@pytest.fixture(autouse=True)
def start_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
