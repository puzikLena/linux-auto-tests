from ssh_checks import ssh_checkout, upload_files


def deploy():
    res = []
    upload_files("0.0.0.0", "username", "qqq", "tests/p7zip-full.deb",
                 "/home/username/p7zip-full.deb")
    res.append(ssh_checkout("0.0.0.0", "username", "qqq", "echo 'qqq' | sudo -S dpkg -i /home/username/p7zip-full.deb",
                            "Setting up"))
    res.append(ssh_checkout("0.0.0.0", "username", "qqq", "echo 'qqq' | sudo -S dpkg -s p7zip-full",
                            "Status: install ok installed"))
    return all(res)


if deploy():
    print("Deploy Ok")
else:
    print("Error by deploying")
