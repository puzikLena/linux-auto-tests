import yaml

from checks import getout
from ssh_checks import ssh_checkout, upload_files

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:

    @staticmethod
    def save_log(start_time, file_name):
        with open(file_name, 'w') as f:
            f.write(getout(f"journalctl --since '{start_time}'"))

    def test_step0(self):
        res = []
        upload_files(
            data["host"],
            data["user"],
            data["passwd"],
            data["local_path"],
            data["remote_path"]
        )
        res.append(
            ssh_checkout(
                data["host"],
                data["user"],
                data["passwd"],
                f"echo {data['passwd']} | sudo -S dpkg -i {data['remote_path']}",
                "Setting up"
            )
        )
        res.append(
            ssh_checkout(
                data["host"],
                data["user"],
                data["passwd"],
                f"echo {data['passwd']} | sudo -S dpkg -s p7zip-full",
                "Status: install ok installed"
            )
        )
        assert all(res), "test0 FAIL"

    def test_step1(self, make_folders, clear_folders, make_files, start_time):
        res1 = ssh_checkout(data["host"], data["user"], data["passwd"],
                            f"cd {data['FOLDER_IN']}; 7z a -t{data['extension']} "
                            f"{data['FOLDER_OUT']}/arx2", "Everything is Ok")
        res2 = ssh_checkout(data["host"], data["user"], data["passwd"], f"ls {data['FOLDER_OUT']}",
                            f"arx2.{data['extension']}")
        self.save_log(start_time, 'log1.txt')
        assert res1 and res2, "test1 FAIL"

    def test_step2(self, clear_folders, make_files, start_time):
        result = [
            ssh_checkout(
                data["host"],
                data["user"],
                data["passwd"],
                f"cd {data['FOLDER_IN']}; 7z a -t{data['extension']} {data['FOLDER_OUT']}/arx2",
                "Everything is Ok"
            ),
            ssh_checkout(
                data["host"],
                data["user"],
                data["passwd"],
                f"cd {data['FOLDER_OUT']}; 7z e arx2.{data['extension']} -o{data['FOLDER_EXTRACT']} -y",
                "Everything is Ok"
            )
        ]
        for item in make_files:
            result.append(
                ssh_checkout(
                    data["host"],
                    data["user"],
                    data["passwd"],
                    f"ls {data['FOLDER_EXTRACT']}",
                    item
                )
            )
        self.save_log(start_time, 'log2.txt')
        assert all(result), "test2 FAIL"

    def test_step3(self, start_time):
        self.save_log(start_time, 'log3.txt')
        assert ssh_checkout(
            data["host"],
            data["user"],
            data["passwd"],
            f"cd {data['FOLDER_OUT']}; 7z t arx2.{data['extension']}",
            "Everything is Ok"
        ), "test3 FAIL"

    def test_step4(self, start_time):
        self.save_log(start_time, 'log4.txt')
        assert ssh_checkout(
            data["host"],
            data["user"],
            data["passwd"],
            f"cd {data['FOLDER_OUT']}; 7z d arx2.7z",
            "Everything is Ok"
        ), "test4 FAIL"

    def test_step5(self, start_time):
        self.save_log(start_time, 'log5.txt')
        assert ssh_checkout(
            data["host"],
            data["user"],
            data["passwd"],
            f"cd {data['FOLDER_OUT']}; 7z u arx2.7z",
            "Everything is Ok"
        ), "test5 FAIL"

    def test_step6(self, clear_folders, make_files, start_time):
        res = [ssh_checkout(
            data["host"],
            data["user"],
            data["passwd"],
            f"cd {data['FOLDER_IN']}; 7z a -t{data['extension']} {data['FOLDER_OUT']}/arx2",
            "Everything is Ok"
        )]
        for item in make_files:
            res.append(
                ssh_checkout(
                    data["host"],
                    data["user"],
                    data["passwd"],
                    f"cd {data['FOLDER_OUT']}; 7z l arx2.{data['extension']}",
                    item
                )
            )
        self.save_log(start_time, 'log6.txt')
        assert all(res), "test6 FAIL"

    def test_step7(self, clear_folders, make_files, make_subfolder, start_time):
        res = [ssh_checkout(
            data["host"],
            data["user"],
            data["passwd"],
            f"cd {data['FOLDER_IN']}; 7z a -t{data['extension']} {data['FOLDER_OUT']}/arx",
            "Everything is Ok"
        ), ssh_checkout(
            data["host"],
            data["user"],
            data["passwd"],
            f"cd {data['FOLDER_OUT']}; 7z x arx.{data['extension']} -o{data['FOLDER_EXTRACT2']} -y",
            "Everything is Ok"
        )]
        for item in make_files:
            res.append(
                ssh_checkout(
                    data["host"],
                    data["user"],
                    data["passwd"],
                    f"ls {data['FOLDER_EXTRACT2']}",
                    item
                )
            )
        res.append(
            ssh_checkout(
                data["host"],
                data["user"],
                data["passwd"],
                f"ls {data['FOLDER_EXTRACT2']}",
                make_subfolder[0]
            )
        )
        res.append(
            ssh_checkout(
                data["host"],
                data["user"],
                data["passwd"],
                f"ls {data['FOLDER_EXTRACT2']}/{make_subfolder[0]}",
                make_subfolder[1]
            )
        )
        self.save_log(start_time, 'log7.txt')
        assert all(res), "test7 FAIL"

    def test_step8(self, clear_folders, make_files, start_time):
        res = []
        for item in make_files:
            hash = getout(f"cd {data['FOLDER_OUT']}; crc32 {item}").upper()
            res.append(
                ssh_checkout(
                    data["host"],
                    data["user"],
                    data["passwd"],
                    f"cd {data['FOLDER_IN']}; 7z h {item}",
                    hash
                )
            )
        self.save_log(start_time, 'log8.txt')
        assert all(res), "test8 FAIL"

    def test_step9(self):
        res = [ssh_checkout(
            data["host"],
            data["user"],
            data["passwd"],
            f"echo {data['passwd']} | sudo -S dpkg -r {data['package_name']}",
            "Removing"
        ), ssh_checkout(
            data["host"],
            data["user"],
            data["passwd"],
            f"echo {data['passwd']} | sudo -S dpkg -s p7zip-full",
            "Status: deinstall ok"
        )]
        assert all(res), "test99 FAIL"
