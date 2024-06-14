import yaml

from checks import find_text, get_command_output

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:

    def test_step1(self):
        res1 = find_text(f"cd {data['FOLDER_IN']}; 7z a -t{data['extension']} {data['FOLDER_OUT']}/arx2",
                        "Everything is Ok")
        res2 = find_text(f"ls {data['FOLDER_OUT']}", f"arx2.{data['extension']}")
        assert res1 and res2, "test1 FAIL"

    def test_step2(self, make_files):
        result = []
        result.append(find_text(f"cd {data['FOLDER_IN']}; 7z a -t{data['extension']} {data['FOLDER_OUT']}/arx2",
                               "Everything is Ok"))
        result.append(find_text(f"cd {data['FOLDER_OUT']}; 7z e arx2.{data['extension']} -o{data['FOLDER_EXTRACT']} -y",
                               "Everything is Ok"))
        for item in make_files:
            result.append(find_text(f"ls {data['FOLDER_EXTRACT']}", item))
        assert all(result), "test2 FAIL"

    def test_step3(self):
        assert find_text(f"cd {data['FOLDER_OUT']}; 7z t arx2.{data['extension']}", "Everything is Ok"), "test3 FAIL"

    def test_step4(self):
        assert find_text(f"cd {data['FOLDER_OUT']}; 7z d arx2.7z", "Everything is Ok"), "test4 FAIL"

    def test_step5(self):
        assert find_text(f"cd {data['FOLDER_OUT']}; 7z u arx2.7z", "Everything is Ok"), "test5 FAIL"

    def test_step6(self, clear_folders, make_files):
        res = []
        res.append(find_text(f"cd {data['FOLDER_IN']}; 7z a -t{data['extension']} {data['FOLDER_OUT']}/arx2",
                            "Everything is Ok"))
        for item in make_files:
            res.append(find_text(f"cd {data['FOLDER_OUT']}; 7z l arx2.{data['extension']}", item))
        assert all(res), "test6 FAIL"

    def test_step7(self, clear_folders, make_files, make_subfolder):
        res = []
        res.append(find_text(f"cd {data['FOLDER_IN']}; 7z a -t{data['extension']} {data['FOLDER_OUT']}/arx",
                            "Everything is Ok"))
        res.append(find_text(f"cd {data['FOLDER_OUT']}; 7z x arx.{data['extension']} -o{data['FOLDER_EXTRACT2']} -y",
                            "Everything is Ok"))
        for item in make_files:
            res.append(find_text(f"ls {data['FOLDER_EXTRACT2']}", item))
        res.append(find_text(f"ls {data['FOLDER_EXTRACT2']}", make_subfolder[0]))
        res.append(find_text(f"ls {data['FOLDER_EXTRACT2']}/{make_subfolder[0]}", make_subfolder[1]))
        assert all(res), "test7 FAIL"

    def test_step8(self, clear_folders, make_files):
        res = []
        for item in make_files:
            hash = get_command_output(f"cd {data['FOLDER_OUT']}; crc32 {item}").upper()
            res.append(find_text(f"cd {data['FOLDER_IN']}; 7z h {item}", hash))
        assert all(res), "test8 FAIL"
