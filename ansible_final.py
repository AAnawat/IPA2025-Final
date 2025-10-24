import subprocess

def showrun():
    # read https://www.datacamp.com/tutorial/python-subprocess to learn more about subprocess
    command = ['ansible-playbook', './playbooks/copy_running_config.yml']
    result = subprocess.run(command, capture_output=True, text=True, cwd="./ansible")
    result = result.stdout

    if 'ok=2' in result:
        return "ok"
    else:
        return "fail"

if __name__ == "__main__":
    showrun()