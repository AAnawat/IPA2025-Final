import subprocess
import re
import os

def showrun():
    # read https://www.datacamp.com/tutorial/python-subprocess to learn more about subprocess
    command = [
        'ansible-playbook',
        '--extra-vars',
        f"router_ip={os.environ.get('ROUTER_HOST')}",
        './playbooks/copy_running_config.yml'
        ]
    result = subprocess.run(command, capture_output=True, text=True, cwd="./ansible")
    result = result.stdout

    if 'ok=4' in result:
        filename = re.findall('show_run_66070217_.*.txt', result)
        return ("ok", filename[0])
    else:
        return ("fail", None)

def config_motd(motd_message):
    command = [
        'ansible-playbook',
        '--extra-vars',
        f"router_ip={os.environ.get('ROUTER_HOST')} motd_message='{motd_message}'",
        './playbooks/config_motd.yml'
        ]
    result = subprocess.run(command, capture_output=True, text=True, cwd="./ansible")
    result = result.stdout

    if 'ok=1' in result:
        return "Ok: success"
    else:
        return "Fail: fail to configure motd"

if __name__ == "__main__":
    showrun()