import yaml

from checks import negative_checkout

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestNegative:
    def test_negative_step1(self, make_files, make_folders, make_bad_file):
        assert negative_checkout(
            f"cd {data['FOLDER_OUT']}; 7z e {make_bad_file}.{data['extension']} {data['FOLDER_EXTRACT']} -y",
            "ERROR"), "test1 FAIL"

    def test_negative_step2(self, make_files, make_folders, make_bad_file):
        assert negative_checkout(
            f"cd {data['FOLDER_OUT']}; 7z t {make_bad_file}.{data['extension']} -o{data['FOLDER_EXTRACT']} -y",
            "ERROR"), "test2 FAIL"
