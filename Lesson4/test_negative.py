import yaml

from ssh_checks import upload_files, ssh_checkout, ssh_negative_checkout

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestNegative:
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

    def test_negative_step1(self, make_files, make_folders, make_bad_file):
        assert ssh_negative_checkout(
            data["host"],
            data["user"],
            data["passwd"],
            f"cd {data['FOLDER_OUT']}; 7z e {make_bad_file}.{data['extension']} {data['FOLDER_EXTRACT']} -y",
            "ERROR"
        ), "test1 FAIL"

    def test_negative_step2(self, make_files, make_folders, make_bad_file):
        assert ssh_negative_checkout(
            data["host"],
            data["user"],
            data["passwd"],
            f"cd {data['FOLDER_OUT']}; 7z t {make_bad_file}.{data['extension']} -o{data['FOLDER_EXTRACT']} -y",
            "ERROR"
        ), "test2 FAIL"

    def test_step99(self):
        result = []
        result.append(
            ssh_checkout(
                data["host"],
                data["user"],
                data["passwd"],
                f"echo {data['passwd']} | sudo -S dpkg -r {data['package_name']}",
                "Removing"
            )
        )
        result.append(
            ssh_checkout(
                data["host"],
                data["user"],
                data["passwd"],
                f"echo {data['passwd']} | sudo -S dpkg -s p7zip-full",
                "Status: deinstall ok"
            )
        )
        assert all(result), "test99 FAIL"
